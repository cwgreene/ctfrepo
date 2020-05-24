from skyfield.api import Topos, load, utc

import datetime

stations = {station.name:station for station in load.tle_file("./active.txt")}
station = stations["PERUSAT 1"]
ts = load.timescale()

lat = 52.5341
lon = 85.18
groundstation = Topos(lat, lon)

sep = ", "

def az_degrees_to_pwm(degrees):
    # print(degrees)
    return int(2457 + (7372 - 2457)*(degrees/360))

def elevation_degrees_to_pwm(degrees):
    # print(degrees)
    return int(2457 + (7372 - 2457)*(degrees/180))

def make_az_el_pair_valid(az_in, el_in):
    """takes both inputs in degrees, sorry"""
    az = az_in
    el = el_in
    if el < 0.0:
        el = 0.0 # clamp to horizon
    if el > 180.0:
        el = 180.0 # clamp to horizon
    while az > 360:
        az = az - 360
    while az < 0:
        az = az + 360
    if az > 180: # > or >= ?
        (az, el) = (az - 180, 180 - el)
    return (az, el)

starttime = 1586789933.820023
for i in range(720):
    time = starttime + i
    t = ts.utc(datetime.datetime.utcfromtimestamp(time).replace(tzinfo=utc))
    distance = station - groundstation
    alt, az, distance = distance.at(t).altaz()
    (az_deg, el_deg) = make_az_el_pair_valid(az.degrees, alt.degrees)
    print(sep.join([str(x) for x in [time,elevation_degrees_to_pwm(az_deg),elevation_degrees_to_pwm(el_deg)]]))
