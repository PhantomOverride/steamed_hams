import json;
import urllib.request;

def RunModule(name):
	try:
		# Pull page text
		pageData = urllib.request.urlopen("https://" + name + ".wordpress.com/").read().decode("utf8")
		# Hack to get the name
		name = pageData.split("<title>")[1].split("</title>")[0]
		if ("|" in name):
			name = name.split(" |")[0]
			return "Real Name: " + name;
	except:
		return "Error - Please investigate";
#pageData = pageData.replace("]", "").replace("[", "")
#	gitlab_dict = json.loads(pageData)
#	if (gitlab_dict['name'] is not None):
#		return("Full Name: " + gitlab_dict['name'])
