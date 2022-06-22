#!/usr/bin/env python3

import sys;
import json;

sys.path.append("./modules/")
name = ""

class socials:
	def __init__(self, name, network, url, info):
		self.name = name;
		self.network = network;
		self.url = url;
		self.info = info;
	def toJson(self):
		return json.dumps(self.__dict__)
list = []
def save_output(line):
	with open(name + ".json", "a") as out:
		out.write(line + '\n')

def input_data(name, sitename, siteurl):
	print("Name: " + name + " - Site: " + sitename + " - Profile URL: " + siteurl);
	info = "";
	try:
		module = __import__(sitename)
		output = getattr(module, "RunModule")(name)
		if (output is not None):
			print(output)
			info = output;
	except:
		pass;
	# TODO: Convert to proper JSON....
	list.append(socials(name, sitename, siteurl, info))
	save_output("	{\n" +
		    "		\"name\": \"" + name +"\",\n" +
		    "		\"network\": \"" + sitename + "\",\n" +
		    "		\"url\": \"" + siteurl + "\",\n" +
		    "		\"info\": \"" + info + "\"\n" +
		    "	},")


filename = sys.argv[1]
name = filename.split(".")[0]
isfirstitem = "true";
with open(filename, 'r') as fileobj:
	for row in fileobj:
		item = row.rstrip('\n')
		if ("[+]" in item):
			if (isfirstitem == "true"):
				save_output("[");
				isfirstitem = "false";
			item = item[4:]
			sitename = item.split(":")[0].strip()
			siteurl = item[len(sitename) + 2:]
			input_data(name, sitename, siteurl)
	save_output("]")

# Clean Up Output File due to suoer hacky JSON implementation
# Read in the file
with open(name + ".json", 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace("},\n]", "}\n]")

# Write the file out again
with open(name + ".json", 'w') as file:
  file.write(filedata)

# For testing purposes
# print("Test List Output: " + json.dumps([ob.__dict__ for ob in list]))
with open (name + ".json", "w") as file:
	json.dump([ob.__dict__ for ob in list], file)
