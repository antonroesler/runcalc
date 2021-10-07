# runcalc
## A Command-Line Pace Calculator
runcalc is a super simple and minimalistic tool for all runners which replaces an online pace calculator. 
The tool converts between:
- distance 
- time
- pace

Two of the three values must be specified, the third is calculated by the tool. 

The uses are extremely simple, here is an example to warm up. Let's say I want to run 15 kilometers in one hour and 20 minutes and I want to know what pace I need to run. The command is:
```bash 
$ runcalc -d 15 -t 1:20:0
5m 20s
```
The output shows me that I have to run with a pace of 5 minutes per kilometer.

Similar, i can specify a pace toghether with a distance or time: 
```bash
$ runcalc -p 5:15 -d 15
1h 18m 45s
```

## Options
The following options are allowed:
- ```-d``` to set the distance 
- ```-p``` to set the pace
- ```-t``` to set the time
- ```-du``` to set the unit of distance [miles, km, m]
- ```-l``` to get a full output with more data
- ```-o``` to set the output unit, e.g. ```miles```to get a pace / mile

## Race Distances
The Tool also supports race standarts as distances: 
```bash
$ runcalc -d half -p 4:35
1h 36m 41s
```
The option ```-d half``` stands for a half marathon, ```-p 4:35``` for a pace of 4:35 per kilometer. As output I get my time of 1 hour and 36 minutes. 

### Allowed Distances
- ```marathon``` or ```full```: 42194.988 meters
- ```half``` or ```half-marathon```: 21097.494 meters
- ```10K```: 10.000 meters
- ```5K``` 5.000 meters
- ```10M```: 10 miles
- ```1M```: 1 mile

## Full Output
The option -l allows for a full output: 
```bash
$ runcalc -d half -p 4:35 -l
===== RUN =====
DISTANCE: 21.1 KM
DISTANCE: 13.1 Miles
TIME: 1h 36m 41s
PACE: 4m 35s per KM
PACE: 7m 22s per Mile
```

## Distance Unit
As I am Geman and I have no idea if anyone besides me will ever use that tool the standart unit of distance is kilometers. Feel free to contact me or create a pull request if you want (or want me) to  implement a global config to set all units to miles as default. 

As of right now it is possible to input a distance in miles as follows: 
```bash
$ runcalc -d 10 -du miles -t 1::
3m 43s
```
The result however is still a pace per Kilometer. (```-t 1::``` is short for 1 hour 0 min 0 sec)

To get a resulting pace in time per mile, the ```-o``` option has to be set to miles:
```bash
$ runcalc -d marathon -t 3:29:59 -o miles
8m 0s
```


# Installation
```Only tested on mac```

- Clone the repo
- cd inside the cloned folder and run ```pip install --editable .```


# Feedback and Contribution 
I'd be more than happy to hear from you either with a comment on the Project or if you are intrested in contributing, everyone is welcome. 
