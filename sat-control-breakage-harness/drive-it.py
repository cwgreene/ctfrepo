""" Really simple program to launch the matlab sat sim
and wire its stdin/stdout up to an adversary of your choice
"""

import subprocess
from sys import argv

controller_command = "controller.py"
# controller_command = "controller_passthru.py"

sim_commands = ["/usr/bin/octave", "challenge.m"]
controller_flags = []

if "live" in argv:
    controller_flags = ["live"]
    sim_commands = ["/bin/nc", "filter.satellitesabove.me", "5014"]

p_sim = subprocess.Popen(sim_commands,
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         universal_newlines=True)

p_controller = subprocess.Popen(["/usr/bin/python3", controller_command] + controller_flags,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                universal_newlines=True)

while True:
    p_sim.stdout.flush()
    last_sim_read = p_sim.stdout.readline()
    print(" :: " + str(last_sim_read))
    if last_sim_read.find("Ticket") < 0:
        nums = [float(x) for x in last_sim_read.strip().split()]
        if len(nums) < 4:
            exit()
        p_controller.stdin.write(last_sim_read)
        p_controller.stdin.flush()
    p_controller.stdout.flush()
    last_controller_read = p_controller.stdout.readline()
    print(" :controller answers: " + str(last_controller_read))
    p_sim.stdin.write(last_controller_read)
    p_sim.stdin.flush()

