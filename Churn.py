import json
import math
import time
import random
import numpy as np
import os
from subprocess import Popen, PIPE, STDOUT


default_avg_tx_delay=4294
completed_tx = 0


def get_gamma():
    gammaval=np.random.gamma(19.28,(1/1.61))
    while gammaval > 15.576: #limit potential gamma distribution values at 90th percentile
        gammaval=np.random.gamma(19.28,(1/1.61))
    gammaval = math.exp(gammaval) #get value in seconds
    gammaval /= 120 #get value in blocks
    gammaval = int(gammaval)
    if gammaval < 10: #apply 7821, jberman
        gammaval = random.randint(10, 61)
    return gammaval



print("This script attempts to match the timing of churning transactions to the decoy selection algorithm. It is programmed to capture 90% of the probability distribution.")
print("This requires that it performs transactions at an average interval of 6 days, and a maximum interval of 68 days.")
tx_count=input("How many churning transactions shall be performed? ")
days_expected = ((tx_count*default_avg_tx_delay)/720)
print("A rough estimate is %d days to complete your transactions. Times may vary significantly."%(days_expected))



#Generate timer value
gammatimer = get_gamma()


#send RPC command get_height
cmd_height = """curl http://127.0.0.1:18081/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"get_height"}' -H 'Content-Type:application/json' | jq '.result.height' """
heightread=os.popen(cmd_height).read()
height=int(heightread)

#calculate trigger height
triggerval = gammatimer + height

#send RPC command get_address
cmd_add = """curl http://127.0.0.1:18081/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"get_address","params":{"account_index":0,"address_index":[0]}}' -H 'Content-Type:application/json' | jq '.result.addresses' """
addressable=os.popen(cmd_add).read()
churning_address=addressable[22:117]

print("-----------------------------------------------------------------------------------")
print("Now churning address: %s"%(churning_address))
print("Current block height is   %d"%(height))
print("Next transaction at block %d"%(triggerval))
print("-----------------------------------------------------------------------------------")

while completed_tx < tx_count:
    
    time.sleep(60) #wait 1 minute
    
    #send RPC command get_height
    cmd_height = """curl http://127.0.0.1:18081/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"get_height"}' -H 'Content-Type:application/json' | jq '.result.height' """
    heightread=os.popen(cmd_height).read()
    height=int(heightread)
    
    #Update printed data
    print("-----------------------------------------------------------------------------------")
    print("%d out of %d transactions completed."%(completed_tx, tx_count))
    print("Current block height is   %d"%(height))
    print("Next transaction at block %d"%(triggerval))
    
    if height >= triggerval:
        #send RPC command sweep_all
        cmd_sweep = """curl http://localhost:18081/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"sweep_all","params":{"address":"%s","subaddr_indices":[0,1,2,3,4],"priority":1,"ring_size":11,"unlock_time":0,"get_tx_keys":true}}' -H 'Content-Type: application/json' | jq '.' """%(churning_address)
        os.system(cmd_sweep)

        completed_tx += 1
        
        #Generate new timer value
        gammatimer = get_gamma()

        #calculate new trigger height
        triggerval = gammatimer + height

done


