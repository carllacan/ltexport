# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 11:25:52 2019

@author: M0084800
"""

def multisplit(string, delimiters):
    # Splits a string using more than one delimiter
    substrings = [string]
    for delimiter in delimiters:
        newsubstrings = []
        for substring in substrings:
            newsubstrings.extend(substring.split(delimiter))
        substrings = newsubstrings
    return substrings

#a = multisplit(log, ["\n", ":", " ", "="])
    
log = input ("Paste LTspice log and press intro:\n")

lines = []
for l in log.split("\n"):
    if len(l) != 0:
        lines.append(l)


# Get steps value, if any
steps = {}
for l in lines:
    if l.startswith(".step "):
        stepname = l[5:].split("=")[0]
        stepvalue = l[5:].split("=")[1]
        if not stepname in steps.keys():
            steps[stepname] = []
        steps[stepname].append(stepvalue)
        
measurements = {}
if len(steps) == 0:
    # Just one step
    for l in lines:
        f = multisplit(l, (":", " ", "="))
        measname = f[0]
        measvalue = f[3]
        measurements[measname] = [measvalue ]
else: 
    # Multiple steps
    for i , l in enumerate(lines):
        if l.startswith("Measurement: "):
            measname = l.split(": ")[1]
            if not measname in measurements.keys():
                measurements[measname] = []
            for step in range(len(steps)+1):
                # Look forward to the next len(steps) lines
                measvalue = lines[i+2+step].split("\t")[1]
                measurements[measname].append(measvalue)
                
# Build the file


if len(steps) == 0:
    measnames = measurements.keys()
    d = "\t"
    header = d.join(measnames)
    
    output_lines = [header]
    measvalues = [measurements[meas][0] for meas in measnames]
    output_lines.append(d.join(measvalues))
else:
    stepnames = steps.keys()
    measnames = measurements.keys()
    d = "\t"
    header = d.join(stepnames) + d + d.join(measnames)
    
    output_lines = [header]
    for step in stepnames:
        for i, stepvalue in enumerate(steps[step]):
            # For each step value add all measurements
            measvalues = [measurements[meas][i] for meas in measnames]
            output_lines.append(d.join( [str(stepvalue)] + measvalues))
            
    
        
outputfile = open("output.txt", "w")
outputfile.writelines([l + '\n' for l in output_lines])
outputfile.close()