import numpy as np
from tqdm import tqdm
import time
from goMultiprocessing import Multiprocessthis_appendsave
import pickle


a1 = np.random.uniform(size=(100,300,300))
a2 = np.random.uniform(size=(100,300,300))

###### doing it sequentially ###############
b = []
c = []

t = time.time()
bfile = open('b.pkl', 'wb')
cfile = open('c.pkl', 'wb')
for i in tqdm(range(len(a1))):
	for jj in range(100):
		jedi = np.array(a1[i]**2*a2[i]**2)
	jarjar = np.mean([np.array(a1[i]**2*a2[i]**2) for j in range(100)], axis=None)
	binks = a1[i]+ a2[i]
	b.append(jarjar)
	c.append(binks)
	pickle.dump(jarjar, bfile)
	pickle.dump(binks, cfile)
bfile.close()
cfile.close()
print(time.time()-t)

# print(b)
# print(c)



############################################

# ######### doing it parallelly #######################
b_par = []
c_par = []
def ourfunc(i):
	'''
		Just copy pase whatever is under the for loop. Except for whaterver is being appended or saved in a file.
		Return those (whatever is being saved or dumped into file) instead in order. First the outputs that has to be appended, then the outputs that have to be saved
	'''
	for jj in range(100):
		jedi = np.array(a1[i]**2*a2[i]**2)
	jarjar = np.mean([np.array(a1[i]**2*a2[i]**2) for j in range(100)], axis=None)
	binks = a1[i]+ a2[i]
	# jarjar=2
	# binks=[12,3,4]
	return [jarjar, binks, jarjar, binks]

t = time.time()
## first arguemnt is the function that was just written
## second argument is the inputs to the function. This will be whatere is in the 'for' line of the loop
## third argement is either the lists you want to append the results to. can be []
## fourth arguemnet is list of files where you want to store your results. can be []
## fifth arguemnt is seed. If ourfunc has any random number generation, the different processes can generate the same random number because they are being called at the same time. Thus, we use this seed and based on this have separate seeds for each child process
b_par,c_par = Multiprocessthis_appendsave(ourfunc, range(len(a1)), [b_par,c_par], ['b_par.pkl','c_par.pkl'], seed=123)
print(time.time()-t)


############################################

# ######### doing it parallelly. Only save to file #######################
# b_par = []
# c_par = []
def ourfunc(i):
	'''
		Just copy pase whatever is under the for loop. Except for whaterver is being appended or saved in a file.
		Return those (whatever is being saved or dumped into file) instead in order. First the outputs that has to be appended, then the outputs that have to be saved
	'''
	for jj in range(100):
		jedi = np.array(a1[i]**2*a2[i]**2)
	jarjar = np.mean([np.array(a1[i]**2*a2[i]**2) for j in range(100)], axis=None)
	binks = a1[i]+ a2[i]
	# jarjar=2
	# binks=[12,3,4]
	return [jarjar]

t = time.time()
## first arguemnt is the function that was just written
## second argument is the inputs to the function. This will be whatere is in the 'for' line of the loop
## third argement is either the lists you want to append the results to. can be []
## fourth arguemnet is list of files where you want to store your results. can be []
## fifth arguemnt is seed. If ourfunc has any random number generation, the different processes can generate the same random number because they are being called at the same time. Thus, we use this seed and based on this have separate seeds for each child process
Multiprocessthis_appendsave(ourfunc, range(len(a1)), [], ['b_par.pkl'], seed=123)
print(time.time()-t)


############################################

