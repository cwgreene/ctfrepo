from skyfield.api import Topos, load, utc

import datetime

stations = {station.name:station for station in load.tle_file("./active.txt")}
station = stations["PERUSAT 1"]
ts = load.timescale()

lat = 52.5341
lon = 85.18
groundstation = Topos(lat, lon)

def az_degrees_to_pwm(degrees):
    print(degrees)
    return int(2457 + (7372 - 2457)*(degrees/360))

def elevation_degrees_to_pwm(degrees):
    print(degrees)
    return int(2457 + (7372 - 2457)*(degrees/180))

starttime = 1586789933.820023
for i in range(720):
    time = starttime + i
    t = ts.utc(datetime.datetime.fromtimestamp(time).replace(tzinfo=utc))
    distance = station - groundstation
    alt, az, distance = distance.at(t).altaz()
    print(time,elevation_degrees_to_pwm(alt.degrees),az_degrees_to_pwm(az.degrees))
