import math
import random
import numpy as np
import json

#generate 2^N endpoints via a set of uniquely timed events.


def get_gamma():
    gammaval=np.random.gamma(19.28,(1/1.61))
    while gammaval > 15.576:
        gammaval=np.random.gamma(19.28,(1/1.61))
    gammaval = math.exp(gammaval)
    gammaval /= 120
    gammaval = int(gammaval)
    if gammaval < 10: #7821
        gammaval = random.randint(10, 61)
    return gammaval




address_set_exponent=input("Set value for address count=2^N (e.g. 8 will mean 2^8=256 addresses generated.) N=")




address_set_size=2**(address_set_exponent+2)
rampaddresses= 2**address_set_exponent
next_set = 2
#initial sender and receivers

#with open("S.txt", "r") as fp:
#    senders = json.load(fp)
#with open("R.txt", "r") as fp:
#    receivers = json.load(fp)
#with open("G.txt", "r") as fp:
#    generators = json.load(fp)
#with open("T.txt", "r") as fp:
#    timers = json.load(fp)

senders = [0]
receivers = [rampaddresses/2]
generators = [4]
timers = [5]
finished = []

print("Senders ", senders)
print("Receivers ", receivers)
print("Generators ", generators)
print("Timers ", timers)


while 1: 

    #simulate timer ticking
    for i in timers:
        if i != 0:
            working_index=itemindex = timers.index(i)#get index of timer
            timers[working_index]-=1
    
    #print("Receivers ", receivers)
    #print("Generators ", generators)
    #print("Timers ", timers)

    #check all timers
    for x in range(0,len(timers)):
        trigger_index=x#get index of timer being processed
        if (generators[trigger_index] >= address_set_size):
            if receivers[trigger_index] not in finished:
                finished.append(receivers[trigger_index])
                with open("F.txt", "w") as fp:
                    json.dump(senders, fp)
            #senders.pop[trigger_index]
            #receivers.pop[trigger_index]
            #generators.pop[trigger_index]
            #timers.pop[trigger_index]
        #if a timer has expires
        if (timers[trigger_index] == 0 and generators[trigger_index] < address_set_size):
            
            print(senders[trigger_index])
            
            

            
                        
            #add R[i] to S[end], copy G[i] to G[end]
            senders.append(receivers[trigger_index])
            generators.append(generators[trigger_index])
            #replace R[i] = S[i] + rampaddresses/G[i], R[end]=...
            receivers[trigger_index]=senders[trigger_index]+(rampaddresses/generators[trigger_index])
            new_receiver=senders[-1]+(rampaddresses/generators[-1])
            receivers.append(new_receiver)
            #update generators
            generators[trigger_index]*=2
            generators[-1]*=2
            #get new timers
            new_gamma_timer=get_gamma()
            timers[trigger_index]=int(new_gamma_timer)
            new_gamma_time=get_gamma()
            timers.append(int(new_gamma_time))
            print(timers)
        

    #when all timers have expired
    check=np.sum(timers)
    if check == 0:
        print("Senders ", senders)
        print("Receivers ", receivers)
        print("Generators ", generators)
        print("Timers ", timers)
        print("Finished ", finished)
        print(len(finished))
        with open("S.txt", "w") as fp:
            json.dump(senders, fp)
        with open("R.txt", "w") as fp:
            json.dump(receivers, fp)
        with open("G.txt", "w") as fp:
            json.dump(generators, fp)
        with open("T.txt", "w") as fp:
            json.dump(timers, fp)
        print("PROGRAM COMPLETE")
        quit()
