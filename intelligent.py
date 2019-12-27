import numpy as np
import agent as ag
import environment as se
import csv

f = open("Sensor Data - Intelligent/waitingtime-intelligent.csv", "w+")
f_num_of_vehicle = open("Sensor Data - Intelligent/totalvehicles-intelligent.csv","w+")
f_trafficDensity = open("Sensor Data - Intelligent/density-intelligent.csv" , "w+")
fnames =["step_num", '-gneE0', '-gneE1','-gneE2', '-gneE3'] 
writer = csv.DictWriter(f, fieldnames=fnames)   
writer_number_of_vehicle = csv.DictWriter(f_num_of_vehicle,fieldnames=fnames)
writer_traffic_density = csv.DictWriter(f_trafficDensity,fieldnames=fnames)
writer.writeheader()  
writer_number_of_vehicle.writeheader()
writer_traffic_density.writeheader()

env_train = se.Environment(gui_f=False)
env_test = se.Environment(gui_f=True,writer_accumWaitingTime=  writer , writer_numOfVehicles= writer_number_of_vehicle, writer_trafficDensity= writer_traffic_density, fnames = fnames)
agent = ag.Agent()

cycle = 20

for ieps in range(cycle): # cycle number
    for i in range(20): # each cycle includes 20 iteration 
        state = env_train.reset()
        done = False # if done is true, then finish the iteration
        # done represents limit of number of vehicles in simulation at time step
        # if number of vehicle is greater than specified limit, then the iteration is done
        # Every lanes, edges or intersections has maximum limit of vehicle which can carry
        while not done:
            action = agent.policy(state)
            next_state, reward, done, rewards = env_train.step_d(action)

            agent.train(state, action, reward, 0.001, [1, 1, done, 1, 1])

            state = next_state
        env_train.close()

    state = env_test.reset() # After algorithm learned, time to apply trained result on the simulation
    done = False
    while not done:
        action = agent.policy(state)
        next_state, reward, done, rewards = env_test.step_d(action)

        state = next_state
    print(ieps , ". step is done!")
    env_test.close()

f.close();
f_num_of_vehicle.close()
f_trafficDensity.close()
