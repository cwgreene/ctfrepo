"""First attempt at an adversary.
Does not reveal the flag.

But, doesn't cause the satellite error to get too large either
"""

from math import sin, cos, sqrt
from sys import argv

separator = " "

if "live" in argv:
    separator = ","
    lines = open("ticket.txt").readlines()
    print(lines[0].strip())

dt = 0.05
omega = -0.08660254

scale = 20.0
max_lie = 0.02

curr_time = 0.0 # time estimate

def perturb_by_euler(quat_in):
    from quaternions import Quaternion # put imports only in functions that need them
    q = Quaternion(quat_in[0], quat_in[1], quat_in[2], quat_in[3])
    euler = q.get_euler()
    euler[2] += max_lie * sin(omega * curr_time)
    q = Quaternion.from_euler(euler)
    return [q.w, q.x, q.y, q.z]


def perturb(quat_in):
    nums = [x for x in quat_in]
    nums[2] += max_lie * cos(omega * curr_time)
    nums[3] += max_lie * sin(omega * curr_time)
    if nums[0] < 0.0:
        nums[0] = -sqrt(min(1.0, 1.0 - nums[1]**2 - nums[2]**2 - nums[3]**2))
    else:
        nums[0] = sqrt(min(1.0, 1.0 - nums[1]**2 - nums[2]**2 - nums[3]**2))
    return nums

while True:
    data = input()
    nums = [float(x) for x in data.strip().split()]
    nums = perturb_by_euler(nums)
    data_out = separator.join([str(x) for x in nums])
    print(data_out)

    curr_time += dt
