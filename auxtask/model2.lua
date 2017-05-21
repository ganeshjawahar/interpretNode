-- node1, node2 => <label>
require 'torch'
require 'io'
require 'nn'
require 'sys'
require 'os'
require 'xlua'
require 'lfs'
require 'pl.stringx'
require 'pl.file'
require 'optim'
tds = require('tds')

cmd = torch.CmdLine()
cmd:option('-train', 'data/author/edge_weight/train', '')
cmd:option('-dev', 'data/author/edge_weight/dev', '')
cmd:option('-test', 'data/author/edge_weight/test', '')
cmd:option('-rep', 'deepwalk/authorembeddings', '')
cmd:option('-lr', 0.01, '')
cmd:option('-batch_size', 256, '')
cmd:option('-num_epochs', 5, '')
cmd:option('-dropout_p', 0.8, '')
cmd:option('-sample', false, '')
cmd:option('-cuda', false, '')
cmd:option('-print', false, '')
params = cmd:parse(arg)
torch.manualSeed(123)

if params.cuda then
  require 'cunn'
  require 'cutorch'
end

function read_rep()
	params.rep_tensors = tds.Hash()
	local rep_ptr = io.open(params.rep, 'r')
	local first_line = stringx.split(rep_ptr:read())
	params.num_nodes, params.dim = tonumber(first_line[1]), tonumber(first_line[2])
	if params.print then
		print(string.format('num_nodes=%d\nndim=%d', params.num_nodes, params.dim))
	end
	for n = 1, params.num_nodes do
		local rep = rep_ptr:read()
		assert(rep~=nil)
		local content = stringx.split(rep)
		local node_id = content[1]
		assert((#content-1)==params.dim)
		local node_emb = torch.Tensor(params.dim)
		for i = 2, #content do
			node_emb[i-1] = tonumber(content[i])
		end
		assert(params.rep_tensors[node_id]==nil)
		params.rep_tensors[node_id] = node_emb
		if params.cuda then params.rep_tensors[node_id] = params.rep_tensors[node_id]:cuda() end
		if n==200 and params.sample then break end
	end
	io.close(rep_ptr)
end
read_rep()
params.label2index, params.index2label = {}, {}
params.train_nodes = tds.Hash()

function get_data(data_file, type)
	local dptr = io.open(data_file, 'r')
	local in1, in2, lab = tds.Hash(), tds.Hash(), tds.Hash() 
	while true do
		local dline = dptr:read()
		if dline == nil then
			break
		end
		local dcontent = stringx.split(dline, '\t')	
		assert(#dcontent==3)
		local label = dcontent[3]
		if params.label2index[label] == nil then
			params.label2index[label] = #params.index2label + 1
			params.index2label[#params.index2label + 1] = label
		end
		local node1, node2 = dcontent[1], dcontent[2]
		if params.rep_tensors[node1]~=nil and params.rep_tensors[node2]~=nil then
			if type=='train' then
			  if params.train_nodes[node1] == nil then params.train_nodes[node1]=1 end
			  if params.train_nodes[node2] == nil then params.train_nodes[node2]=1 end
			end
			--if params.train_nodes[node1]~=nil and params.train_nodes[node2]~=nil then
			  -- table.insert(tensors, {node1, node2, params.label2index[label]})
			  in1[#in1+1] = node1
			  in2[#in2+1] = node2
			  lab[#lab+1] = params.label2index[label]
			--end
		end
		if params.sample and #in1 == 200 then break end
	end
	io.close(dptr)
	return in1, in2, lab
end

params.train_in1, params.train_in2, params.train_lab = get_data(params.train, 'train')
params.dev_in1, params.dev_in2, params.dev_lab = get_data(params.dev, 'dev')
params.test_in1, params.test_in2, params.test_lab = get_data(params.test, 'test')
if params.print then
	print(string.format('#train=%d\n#dev=%d\n#test=%d', #params.train_in1, #params.dev_in1, #params.test_in1))	
end

params.model = nn.Sequential()
params.model:add(nn.ParallelTable())
params.model.modules[1]:add(nn.Identity())
params.model.modules[1]:add(nn.Identity())
params.model:add(nn.JoinTable(2))
params.model:add(nn.ReLU())
params.model:add(nn.Linear(2 * params.dim, #params.index2label))
params.model:add(nn.Dropout(params.dropout_p))
params.criterion = nn.CrossEntropyCriterion()
if params.cuda then
  params.model = params.model:cuda()
  params.criterion = params.criterion:cuda()
end
params.pp, params.gp = params.model:getParameters()
params.optim_state = {learningRate = params.lr}

function get_aemb(id)
	local res = params.rep_tensors[id]
	assert(res~=nil)
	--if params.cuda then res = res:cuda() end
	return res
end

if params.print then
  print('training...')
end
function train(states)
	params.model:training()
	local indices = torch.randperm(#params.train_in1)
	local epoch_loss = 0
  local cur_input_sent, cur_input_word, cur_target = torch.Tensor(params.batch_size, params.dim), torch.Tensor(params.batch_size, params.dim), torch.Tensor(params.batch_size, 1)
  if params.cuda then
  	cur_input_sent = cur_input_sent:cuda()
  	cur_input_word = cur_input_word:cuda()
  	cur_target = cur_target:cuda()
  end	
  if params.print then
	  xlua.progress(1, #params.train_in1)
	end
	for i = 1, #params.train_in1, params.batch_size do
		local cur_bsize = math.min(i + params.batch_size - 1, #params.train_in1) - i + 1
		if cur_bsize~=params.batch_size then
			cur_input_sent, cur_input_word, cur_target = torch.Tensor(cur_bsize, params.dim), torch.Tensor(cur_bsize, params.dim), torch.Tensor(cur_bsize, 1)
		  if params.cuda then
		  	cur_input_sent = cur_input_sent:cuda()
		  	cur_input_word = cur_input_word:cuda()
		  	cur_target = cur_target:cuda()
		  end
		end
		for j = 1, cur_bsize do
			local record = {params.train_in1[indices[i + j - 1]], params.train_in2[indices[i + j - 1]], params.train_lab[indices[i + j - 1]]}			
			cur_input_sent[j] = get_aemb(record[1])
			cur_input_word[j] = get_aemb(record[2])
			cur_target[j][1] = record[3]
		end
		local feval = function(x)
			params.pp:copy(x)
			params.gp:zero()
			local out = params.model:forward({cur_input_sent, cur_input_word})
			local loss = params.criterion:forward(out, cur_target)
			epoch_loss = epoch_loss + loss * cur_bsize
			local grads = params.criterion:backward(out, cur_target)
			params.model:backward({cur_input_sent, cur_input_word}, grads)
			return loss, params.gp
		end
		optim.adagrad(feval, params.pp, params.optim_state, states)		
		if params.print then
		  xlua.progress(i, #params.train_in1)
		end
	end
	if params.print then
	  xlua.progress(#params.train_in1, #params.train_in1)
	end
	return epoch_loss / #params.train_in1
end

params.soft_max = nn.SoftMax()
if params.cuda then params.soft_max = params.soft_max:cuda() end
function compute_performance(in1, in2, lab)
	params.model:evaluate()
	local tp, pred_as, gold_as = {}, {}, {}
	for i = 1, #params.index2label do
		tp[i] = 0
		pred_as[i] = 0
		gold_as[i] = 0
	end
	local cur_input_sent, cur_input_word, cur_target = torch.Tensor(params.batch_size, params.dim), torch.Tensor(params.batch_size, params.dim), {}
	if params.cuda then
    cur_input_sent = cur_input_sent:cuda()
    cur_input_word = cur_input_word:cuda()
	end
	for i = 1, #in1, params.batch_size do
		local cur_bsize = math.min(i + params.batch_size - 1, #in1) - i + 1
		if cur_bsize~=params.batch_size then
			cur_input_sent, cur_input_word = torch.Tensor(cur_bsize, params.dim), torch.Tensor(cur_bsize, params.dim)
			cur_target = {}
			if params.cuda then
				cur_input_sent = cur_input_sent:cuda()
				cur_input_word = cur_input_word:cuda()
			end
		end
		for j = 1, cur_bsize do
			local record = {in1[i + j - 1], in2[i + j - 1], lab[i + j - 1]}
			cur_input_sent[j] = get_aemb(record[1])
			cur_input_word[j] = get_aemb(record[2])
			table.insert(cur_target, record[3])
		end
		local out = params.model:forward({cur_input_sent, cur_input_word})
		local soft = params.soft_max:forward(out)
		_, ids = soft:max(2)
		for j = 1, cur_bsize do			
			if ids[j][1] == cur_target[j] then 
				tp[ids[j][1]] = tp[ids[j][1]] + 1 
			end
			pred_as[ids[j][1]] = pred_as[ids[j][1]] + 1
			gold_as[cur_target[j]] = gold_as[cur_target[j]] + 1
		end
	end	
	local tp_sum, prec_den, recall_den = 0, 0, 0
	for i = 1, #params.index2label do
		tp_sum = tp_sum + tp[i]
		prec_den = prec_den + pred_as[i]
		recall_den = recall_den + gold_as[i]
	end
	local micro_prec, micro_recall = (tp_sum / prec_den), (tp_sum / recall_den)
	return ((2 * micro_prec * micro_recall) / (micro_prec + micro_recall))
end

local start=sys.clock()
local states = {}
for epoch = 1, params.num_epochs do
	local loss = train(states)
	if params.print then print('Epoch ('..epoch..'/'..params.num_epochs..') Loss = '..loss) end
end
local dev_fscore = -1
if #params.dev_in1>0 then dev_fscore=compute_performance(params.dev_in1, params.dev_in2, params.dev_lab) end
local test_fscore = -1
if #params.test_in1>0 then test_fscore=compute_performance(params.test_in1, params.test_in2, params.test_lab) end
local now=(sys.clock()-start)/60
print(string.format('%s\t%.2f\t%.2f\t%.2f', params.rep, dev_fscore, test_fscore, now))
