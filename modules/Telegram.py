import json;
import urllib.request;

def RunModule(name):
	try:
		# Pull page text
		pageData = urllib.request.urlopen("https://t.me/" + name).read().decode("utf8")
		# Hack to get the name
		name = pageData.split("og:title\" content=\"")[1].split("\"")[0]
		return "Real Name: " + name;
	except:
		return "Error - Please investigate";
#pageData = pageData.replace("]", "").replace("[", "")
#	gitlab_dict = json.loads(pageData)
#	if (gitlab_dict['name'] is not None):
#		return("Full Name: " + gitlab_dict['name'])
