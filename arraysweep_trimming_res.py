import numpy as np
import random
import math
import sys


def get_gamma_block_delta():
    gammaval=np.random.gamma(19.28,(1/1.61))
    #while gammaval > 15.576: #limit potential gamma distribution values at 90th percentile
    #    gammaval=np.random.gamma(19.28,(1/1.61))
    gammaval = math.exp(gammaval) #get value in seconds
    gammaval /= 120 #get value in blocks
    gammaval = int(gammaval)
    if gammaval < 10: #apply 7821, jberman
        gammaval = random.randint(10, 61)
    return gammaval


#block_count=input("How many blocks to generate? ")
#tx_count=input("How many transactions in each block? ")
#decoy_count=input("How many decoys for each transaction? ")

block_count = 720 #target of 100,000
tx_count = 100 #target of 100
decoy_count = 15
#intree = 0
checkingtx = np.zeros((tx_count))

#4d array block x tx x decoys x 2(block and tx of decoy selected)
blockchain=np.zeros((block_count,tx_count, decoy_count, 2)) 

for block in range(block_count - 1):
    for tx in range(tx_count):
        for decoy in range(decoy_count):
            #generate decoy and store information : block in [0], tx in [1]
            newVal = get_gamma_block_delta()
            blockchain[block,tx,decoy,0] = block + newVal
            blockchain[block,tx,decoy,1] = np.random.randint(0, tx_count) 
            if block + newVal >= block_count: #if generated decoy is outside of range being evaluated
                blockchain[block,tx,decoy,0] = -1 #enter block as -1
                blockchain[block,tx,decoy,1] = -1 #enter tx as -1
            

'''
print(blockchain[block_count - 1,tx_count - 1,decoy_count - 1])
thing = blockchain[block_count - 1,tx_count - 1,decoy_count - 1]
print(thing)
print(thing[0])
#lets grab the decoys of that decoy
consider=blockchain[int(thing[0]),int(thing[1])]
print(consider)
'''
#load checker with all tx decoys
checker = [] # checker[0] is tx being traced, [1] is the block of the decoy, [2] is the tx of the decoy



#want to check, what percent of tx in block 0 include tx 0 of block 100?
#recursion technique too much, do sequential sweeps.

#while there are decoys in check list
#check decoys
#add decoys of decoys to list, so long as they are in range being considered
#remove decoys branched from any confirmed tx trees
#repeat


for tx in range(tx_count):
    #one tx at a time
    checker = []
    #get all decoys for a given tx
    for decoy in range(decoy_count):
        if blockchain[0,tx,decoy,0] != -1:
            txtagged=[tx,blockchain[0,tx,decoy,0],blockchain[0,tx,decoy,1]]
            checker.append(txtagged)
    print(checker)
    print('Decoy tier: ', 0, 'with: ',len(checker), 'valid decoys: ')

    #check all decoys for a given tx
    for circle in range(17):

        #add next set of decoys
        for x in range(0,len(checker)):
            for decoy in range(decoy_count):
                if blockchain[int(checker[x][1]),int(checker[x][2]),decoy,0] != -1:    
                    nextdecoys=(int(checker[x][0]),blockchain[int(checker[x][1]),int(checker[x][2]),decoy,0],blockchain[int(checker[x][1]),int(checker[x][2]),decoy,1])
                    checker.append(nextdecoys)

        print('Decoy tier: ', circle + 1, 'with: ',len(checker), 'valid decoys: ')

        #prune decoy set for duplicates
        checker = np.unique(checker,axis=0)
        checker = np.ndarray.tolist(checker)

        
        #Check if specific decoys are in set. If so, record this and TODO: trim entries
        for tx in range(tx_count):
            #print(len(checker))
            for x in range(0,len(checker)):
                if checker[x][1] == (block_count - 5) and checker[x][2] == 8:
                #found the decoy we wanted, record tx as linked
                #print('checker val', checker[x])
                #print('tx linked ', checker[x][0])
                    checkingtx[int(checker[x][0])] = 1
                    print('tx ', checker[x][0], ' detected')
                    checker = []
                    break

#print(checker)

#print(checker[0][0])
#checker is now loaded with all valid direct decoys. sweep through array, appending decoys each time until finished
'''
for circle in range(6):
    #add next set of decoys
    for x in range(0,len(checker)):
        for decoy in range(decoy_count):
            if blockchain[int(checker[x][1]),int(checker[x][2]),decoy,0] != -1:    
                nextdecoys=(int(checker[x][0]),blockchain[int(checker[x][1]),int(checker[x][2]),decoy,0],blockchain[int(checker[x][1]),int(checker[x][2]),decoy,1])
                checker.append(nextdecoys)
    print(len(checker))
    #Check if specific decoys are in set. If so, recorcd this and TODO: remove relevant entries
    for tx in range(tx_count):
        #print(len(checker))
        for x in range(0,len(checker)):
            if checker[x][1] == (block_count - 50) and checker[x][2] == 1:
                #found the decoy we wanted, record tx as linked
                #print('checker val', checker[x])
                #print('tx linked ', checker[x][0])
                checkingtx[checker[x][0]] = 1
    #remove all parts of detected transactions from checker array
    for x in range(0,len(checker[x])):
        print('checker[x][0]', checker[x][0])
        if checkingtx[checker[x][0]] == 1:
            del checker[x]
            #checker.remove(checker
'''
 
#print(checker)
'''
for tx in range(tx_count):
    #check all tx decoys
    for decoy in range(decoy_count):
        if blockchain[0,tx,decoy,0] == 10000 and blockchain[0,tx,decoy,1] == 0:
            intree += 1
            checkingtx[tx] = 1
print("number of tx in block 0 that reference tx 0 of block 100 directly: ", sum(checkingtx))
'''





#print('done')
print(checkingtx)
print("number of tx in block 0 that reference tx 8 in a block ~5 from the end: ", sum(checkingtx))

#separate array for references?? Don't track for now
#reference_record=np.zeros((block_count,tx_count,reference_count))
#


'''
class Reference:
    block = 0
    tx = 0
class Transaction:
    decoys=np.array(decoy_count)
    references=np.array(reference_count)
'''
