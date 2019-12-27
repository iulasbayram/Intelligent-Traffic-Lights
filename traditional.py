from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import subprocess
import random
import csv

# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit(
        "please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci


def run():
    """execute the TraCI control loop"""
    file_accumWaitingTime = open("Sensor Data - Traditional/waitingtime-traditional.csv", "w+")
    file_numOfVehicles = open("Sensor Data - Traditional/totalvehicles-traditional.csv", "w+")
    file_trafficDensity = open("Sensor Data - Traditional/density-traditional.csv", "w+")
    file_names = ["step_num", '-gneE0', '-gneE1','-gneE2', '-gneE3']
    writer_accumWaitingTime = csv.DictWriter(file_accumWaitingTime, fieldnames=file_names)    
    writer_numOfVehicles = csv.DictWriter(file_numOfVehicles, fieldnames=file_names)   
    writer_trafficDensity = csv.DictWriter(file_trafficDensity, fieldnames=file_names)    
    writer_accumWaitingTime.writeheader()   
    writer_numOfVehicles.writeheader()
    writer_trafficDensity.writeheader()
    step = 0
    # we start with phase 2 where EW has green
    time_result = [None] * 4
    vehicle_result = [None] * 4
    density_result = [None] * 4
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        
        for id in range(1,len(file_names)):
            time_result[id-1] = traci.edge.getWaitingTime(file_names[id])
        writer_accumWaitingTime.writerow({file_names[0]: step, file_names[1]: time_result[0], file_names[2]: time_result[1], file_names[3]: time_result[2], file_names[4]: time_result[3]})

        for id in range(1,len(file_names)):
            vehicle_result[id-1] = traci.edge.getLastStepVehicleNumber(file_names[id])
        writer_numOfVehicles.writerow({file_names[0]: step, file_names[1]: vehicle_result[0], file_names[2]: vehicle_result[1], file_names[3]: vehicle_result[2], file_names[4]: vehicle_result[3]})
        
        for id in range(1,len(file_names)):
            numberOfVehicle = traci.edge.getLastStepVehicleNumber(file_names[id])
            density_result[id-1] = numberOfVehicle / traci.lane.getLength(file_names[id] + "_0")
        writer_trafficDensity.writerow({file_names[0]: step, file_names[1]: density_result[0], file_names[2]: density_result[1], file_names[3]: density_result[2], file_names[4]: density_result[3]})

        step += 1
    traci.close()
    sys.stdout.flush()
    file_accumWaitingTime.close()
    file_numOfVehicles.close()
    file_trafficDensity.close()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    # first, generate the route file for this simulation
    

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "Intersection/intersection.sumocfg"])
    traci.trafficlight.setProgram('gneJ00', '0')
    run()
