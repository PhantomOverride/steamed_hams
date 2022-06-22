import json;
import urllib.request;

def RunModule(name):
	pageData = urllib.request.urlopen("https://api.github.com/users/" + name).read().decode("utf8")
	github_dict = json.loads(pageData)
	if (github_dict['name'] is not None):
		return("Full Name: " + github_dict['name'])
