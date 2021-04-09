import os
import torch
import numpy as np

# a = inf[7].split()
# print('+'+(a[1]).split()+'+')
# for i in a:
#   print(i)
#   print('===7===\n')

# b = inf[8].split('|')
# for i in b:
#   print(i)
#   print('===8===\n')
# a = b[2].split('/')
# a = [int(i.replace('MiB','')) for i in a]
# print(a)

def prep():
  cmd = 'nvidia-smi'
  d = os.popen(cmd)
  inf = d.readlines()
  leng = len(inf)
  j = 0
  ind = 0
  gpu_num = 0
  for i in inf:
    #print(ind,i)
    ind = ind+1
    if ('Processes' in i):
      gpu_num = int((j - 9) / 3)
      #print(gpu_num)
      break
    else:
      j = j + 1
  return gpu_num,inf

def runing(cmd1,s_use):
  n = 10
  while(n):
    gpu_num,info = prep()
    gpu_id, gpu_assi, gpu_can = gpu_use(gpu_num,s_use,info)
    print(gpu_id, gpu_assi, gpu_can)
    if not len(gpu_can)>=s_use:
      n = n-1
      continue
    else:
      break
  os.system(cmd1)


#=============GPU use==============
def gpu_use(gpu_num,s_use,inf):
  lis = []
  for i in range(gpu_num):
    lis.append(7+3*i)
    lis.append(8 + 3 * i)
  #print(lis)
  lis1 = []
  for i in lis:
    if (i-8)%3==0:
      b = inf[i].split('|')
      a = b[2].split('/')
      cs = [int(i.replace('MiB', '')) for i in a]
      cs = (1.0*cs[0]/cs[1])*100
      cs = float(format(cs, '.2f'))
    else:
      a = inf[i].split()
      c = (a[1]).split()
      cs = "".join(c)
      cs = int(cs)
    lis1.append(cs)
  print(lis1)#GPU ID ;use percent
  #can_use = lis1.count(0.00)
  lis3 = []
  for i in range(1,len(lis1)+1,2):
    lis3.append(lis1[i])
  print(lis3)
  lis2 = np.array(lis3)
  can_id = np.where(lis2 == 0.00)
  print(can_id)
  can_assi = np.where(lis2 < 70.00)
  for i in can_id:
    can_id = i.tolist()
  for i in can_assi:
    can_assi = i.tolist()
  if len(can_id) >= s_use or (len(can_id) == (s_use-1) and len(can_assi) > (s_use-1)):
    gpu_id_av = list(set(can_id+can_assi))
  else:
    can_assi = None
    gpu_id_av = can_id
  return can_id,can_assi,gpu_id_av
#=============GPU Fan==============
# lis = [7,8,10,11,13,14,16,17]
def gpu_fan(lis,inf):
  lis1 = []
  for i in lis:
    a = inf[i].split()
    c = (a[1]).split()
    cs = "".join(c)
    if (i-8)%3==0:
      cs = cs.replace('%','')
      cs = int(cs)
    else:
      cs = int(cs)
    lis1.append(cs)
  print(lis1)
#==========GPU  available==========
# gpu = '0'
# seed = 1
# os.environ["CUDA_VISIBLE_DEVICES"] = gpu
# use_gpu = torch.cuda.is_available()
# if use_gpu:
#   print("Currently using GPU {}".format(gpu))
#   torch.cuda.manual_seed_all(seed)
# else:
#   print("Currently GPU is not available")
if __name__ == '__main__':
  s_use = 1#should use gpu num
  cmd = 'lspci | grep -i nvidia'
  runing(cmd,s_use)
