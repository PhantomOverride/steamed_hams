import json;
import urllib.request;

def RunModule(name):
	pageData = urllib.request.urlopen("https://gitlab.com/api/v4/users?username=" + name).read().decode("utf8")
	pageData = pageData.replace("]", "").replace("[", "")
	gitlab_dict = json.loads(pageData)
	if (gitlab_dict['name'] is not None):
		return("Full Name: " + gitlab_dict['name'])
