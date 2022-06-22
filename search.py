#!/usr/bin/env python3

import os;
import time;
import json;
import sys;

def merge_JsonFiles(filename):
    result = list()
    for f1 in filename:
        with open(f1, 'r') as infile:
            result.extend(json.load(infile))

    with open('output.json', 'w') as output_file:
        json.dump(result, output_file)

# Make sure params are good
if (len(sys.argv) != 2):
	print("Usage: ./search.py names.txt")
	quit()

name = sys.argv[1]

# Docker check (Outside of threading)
print("Verifying docker image")
os.system("docker run theyahya/sherlock >/dev/null")
print("Verified")

# Make sute the names file exists
if not os.path.exists(name):
	print("The name file " + name + " does not exist :(")
	quit()

names = open(name, "r").readlines()
for thename in names:
	thename = thename.strip()
	print("Processing " + thename);
	# Some
	# os.system("sudo docker run theyahya/sherlock " + thename + " --site GitHub --site LinkedIn --site HackerOne --site GitLab --site Telegram --site Keybase --timeout=1 > " + thename + ".txt && python3 parse.py " + thename + ".txt &")
	# All
	os.system("docker run theyahya/sherlock " + thename + " --timeout=1 > " + thename + ".txt && python3 parse.py " + thename + ".txt &")
isrunning = "true"
while (isrunning == "true"):
	ps = os.popen('ps -aux | grep parse.py').read()
	if ("python3 parse.py" in ps):
		print("Running...")
		time.sleep(2)
	else:
		print("Done")
		break;

# Iterate over each json file and combine them into one
alljson = [];
for thename in names:
	thename = thename.strip()
	f = open(thename + ".json")
	data = json.load(f)
	alljson += data
	os.remove(thename + ".json")

# Save the final result for neo4j
with open("result.json", "w") as file:
	json.dump(alljson, file)

print("Done!")
