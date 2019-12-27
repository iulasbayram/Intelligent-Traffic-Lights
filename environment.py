import os
import sys


import traci
import numpy as np
import csv

class Environment:
    place_lenght = 7.5
    place_offset = 8.50
    lane_len = 10
    lane_ids = ['-gneE0_0', '-gneE0_1', '-gneE1_0', '-gneE1_1', '-gneE2_0', '-gneE2_1', '-gneE3_0', '-gneE3_1']
    
    def __init__(self, label='default', gui_f=False, writer_accumWaitingTime=None, writer_numOfVehicles = None, writer_trafficDensity = None, fnames = None):
        self.label = label
        self.wt_last = 0.
        self.number_of_cars = 0
        self.writer_accumWaitingTime = writer_accumWaitingTime
        self.writer_numOfVehicles = writer_numOfVehicles
        self.writer_numOfVehicles = writer_numOfVehicles
        self.writer_trafficDensity = writer_trafficDensity
        self.fnames = fnames
        self.step_number = 0

        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:
            sys.exit("please declare environment variable 'SUMO_HOME'")

        exe = 'sumo-gui' if gui_f else 'sumo'
        sumoBinary = os.path.join(os.environ['SUMO_HOME'], 'bin', exe)
        self.sumoCmd = [sumoBinary, '-c', 'Intersection/intersection.sumocfg']

        return

    def take_positions(self):
        state = np.zeros(self.lane_len * 8 + 4, dtype=np.float32)

        for ilane in range(0, 8):
            lane_id = self.lane_ids[ilane]
            number_of_cars = traci.lane.getLastStepVehicleNumber(lane_id)
            cars = traci.lane.getLastStepVehicleIDs(lane_id)
            for icar in cars:
                xcar, ycar = traci.vehicle.getPosition(icar)
                if ilane < 2:
                    pos = (ycar - self.place_offset) / self.place_lenght
                elif ilane < 4:
                    pos = (xcar - self.place_offset) / self.place_lenght
                elif ilane < 6:
                    pos = (-ycar - self.place_offset) / self.place_lenght
                else:
                    pos = (-xcar - self.place_offset) / self.place_lenght
                if pos > self.lane_len - 1.:
                    continue
                pos = np.clip(pos, 0., self.lane_len - 1. - 1e-6)
                ipos = int(pos)
                state[int(ilane * self.lane_len + ipos)] += 1. - pos + ipos
                state[int(ilane * self.lane_len + ipos + 1)] += pos - ipos
            state[self.lane_len * 8:self.lane_len * 8+4] = np.eye(4)[traci.trafficlight.getPhase('gneJ00')]

        return state

# -------------------------------------------------------------- WRITING DATA TO CSV FILE -------------------------------------------------------------- #
    def writeAccumulatedTimetoCSV(self):
        time_result = [None] * 4
        if self.writer_accumWaitingTime != None:
            for id in range(1,len(self.fnames)):
                time_result[id-1] = traci.edge.getWaitingTime(self.fnames[id])
            self.writer_accumWaitingTime.writerow({self.fnames[0]: self.step_number, self.fnames[1]: time_result[0], self.fnames[2]: time_result[1], self.fnames[3]: time_result[2], self.fnames[4]: time_result[3]})
    
    def writeNumOfVehicletoCSV(self):
        vehicle_result = [None] * 4 
        if self.writer_numOfVehicles != None:
            for id in range(1,len(self.fnames)):
                vehicle_result[id-1] = traci.edge.getLastStepVehicleNumber(self.fnames[id])
            self.writer_numOfVehicles.writerow({self.fnames[0]: self.step_number, self.fnames[1]: vehicle_result[0], self.fnames[2]: vehicle_result[1], self.fnames[3]: vehicle_result[2], self.fnames[4]: vehicle_result[3]})

    def writeTrafficDensitytoCSV(self):
        density_result = [None] * 4
        if self.writer_trafficDensity != None:
            for id in range(1,len(self.fnames)):
                numberOfVehicle = traci.edge.getLastStepVehicleNumber(self.fnames[id])
                density_result[id-1] = numberOfVehicle / traci.lane.getLength(self.fnames[id] + "_0")
            self.writer_trafficDensity.writerow({self.fnames[0]: self.step_number, self.fnames[1]: density_result[0], self.fnames[2]: density_result[1], self.fnames[3]: density_result[2], self.fnames[4]: density_result[3]})
# -------------------------------------------------------------- WRITING DATA TO CSV FILE -------------------------------------------------------------- #

    def step_d(self, action):
        done = False
        # traci.switch(self.label)
        
        action = np.squeeze(action)
        #print("action: " , action)
        traci.trafficlight.setPhase('gneJ00', action)

        traci.simulationStep()
        self.writeAccumulatedTimetoCSV()
        self.writeNumOfVehicletoCSV()
        self.writeTrafficDensitytoCSV()
        traci.simulationStep()
        self.step_number += 1
        self.writeAccumulatedTimetoCSV()
        self.writeNumOfVehicletoCSV()
        self.writeTrafficDensitytoCSV()
        self.number_of_cars += traci.simulation.getDepartedNumber()

        state = self.take_positions()

        wt = 0
        for ilane in range(0, 8):
            lane_id = self.lane_ids[ilane]
            wt += traci.lane.getWaitingTime(lane_id)
        reward = - (wt - self.wt_last)*0.004

        if self.number_of_cars > 250:
            done = True

        self.step_number += 1
        return state, reward, done, np.array([[reward]])

    def reset(self):
        self.wt_last = 0.
        self.number_of_cars = 0
        traci.start(self.sumoCmd, label=self.label)
        traci.trafficlight.setProgram('gneJ00', '0')
        traci.simulationStep()
        self.writeAccumulatedTimetoCSV()
        self.writeNumOfVehicletoCSV()
        self.writeTrafficDensitytoCSV()
        traci.simulationStep()
        self.step_number += 1
        return self.take_positions()

    def close(self):
        traci.close()
