import numpy as np
import random
import math
import sys

def get_gamma_block_delta():
    gammaval=np.random.gamma(19.28,(1/1.61))
    gammaval = math.exp(gammaval) #get value in seconds
    gammaval /= 3 #get value in transaction (3 tx per second)
    gammaval = int(gammaval)
    if gammaval < 10: #apply 7821, jberman
        gammaval = random.randint(10, 61)
    return gammaval

block_count = 3600
tx_per = 10
tx_count = block_count * tx_per
decoy_count = 30
checkingtx = [[0 for x in range(tx_per)] for y in range(tx_per)] # txin x txout. if value is 1, we found txout in tree of txin

#create blockchain as 2d array (tx x decoys)
blockchain=[[0 for x in range(decoy_count)] for y in range(tx_count)]

for tx in range(tx_count):
    for decoy in range(decoy_count):
        selected = get_gamma_block_delta()
        #print(tx)
        #print(decoy)
        #print(selected)
        blockchain[tx][decoy] = selected
        if selected >= tx_count:
            blockchain[tx][decoy] = -1



#get all decoys for a given txin in 1d list
checker = []
for txin in range(1): #run fast, 100% consistent from txin to txin
    checker = []
    print('next txin ', txin)
    for decoy in range(decoy_count):
        if blockchain[txin][decoy] != -1:
            checker.append(blockchain[txin][decoy])
    #print('Decoy tier: ', 0, 'with: ',len(checker), 'valid decoys: ')

    #check all decoys against txouts for a given txin
    for circle in range(10):

        #add next set of decoys
        for x in range(0,len(checker)):
            if checker[x] != -1:
                for decoy in range(decoy_count):
                    checker.append(blockchain[checker[x]][decoy])
        #remove duplicates
        checker = [*set(checker)]
        #print('Decoy tier: ', circle + 1, 'with: ',len(checker), 'valid decoys: ')

        #Check if txouts are in decoy set
        for x in checker:
            for txout in range(tx_per):
                if x == (tx_count - (txout+2)) and checkingtx[txin][txout] == 0:
                    checkingtx[txin][txout] = 1
                    #print('Decoy tier: ', circle + 1, 'with: ',len(checker), 'valid decoys: ')
                    print('txout ', txout, ' detected for txin ', txin)
                    
                if sum(checkingtx[txin]) == tx_per: #if found all txout for a given txin, move on
                    checker = []
                    break
        
print(checkingtx)
