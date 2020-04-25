from mpi4py import MPI
from random import random
import time

timeStartTotal = time.clock()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

#calculatin Pi Function
def calPi(n):
	inside = 0
	for i in range(n):
		x = random()
		y = random()
		if x**2 + y**2 <= 1:
			inside += 1
	return(inside)

#Master
if rank == 0:
	# Pi Calculation
	rangeNumber = 10**8
	# print('This is rank 0 sending %s as range to slaves for calculation' %(rangeNumber))
	comm.send(rangeNumber,dest=1,tag=11)
	comm.send(rangeNumber,dest=2,tag=11)
	inside1 = comm.recv(source=1, tag=11)
	inside2 = comm.recv(source=2, tag=11)
	print('# form rank 1:',inside1)
	print('# form rank 2:',inside2)
	pi = 4*(inside1+inside2)/(rangeNumber*2)
	print("Calculated Pi: ",pi)

	#Time Calculation
	timeEnd1 = comm.recv(source=1, tag=12)
	print('Time to proccess for rank1: ',timeEnd1)
	timeEnd2 = comm.recv(source=2, tag=12)
	print('Time to proccess for rank2:',timeEnd2)
	print('Average time for each proccess:',(timeEnd1+timeEnd2)/2)
	timeEndTotal = (time.clock() - timeStartTotal)
	print('Total time to proccess:',timeEndTotal)

#Slave 1
if rank == 1:
	timeStart1 = MPI.Wtime()
	data = comm.recv(source=0,tag=11)
	inside1 = calPi(data)
	comm.send(inside1, dest=0, tag=11)
	timeEnd1 = MPI.Wtime() - timeStart1
	print('1',timeEnd1)
	comm.send(timeEnd1, dest=0, tag=12)	
	# print('This is rank 1 & got this range to calculate Pi from rank 0: ', data)

#Slave 2
if rank == 2:
	timeStart2 = MPI.Wtime()
	data = comm.recv(source=0, tag=11)
	inside2 = calPi(data)
	comm.send(inside2, dest=0, tag=11)
	timeEnd2 = MPI.Wtime() - timeStart2
	print(timeEnd2)
	comm.send(timeEnd2, dest=0, tag=12)	
	# print('This is rank 2 & got this range to calculate Pi from rank 0: ', data)
