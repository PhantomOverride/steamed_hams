import json;
import urllib.request;

def RunModule(name):
	pageData = urllib.request.urlopen("https://keybase.io/_/api/1.0/user/lookup.json?usernames=" + name).read().decode("utf8")
	keybase_dict = json.loads(pageData)
	if (keybase_dict['them'] is not None):
		if (keybase_dict['them'][0] is not None):
			if (keybase_dict['them'][0]['profile'] is not None):
				if (keybase_dict['them'][0]['profile']['full_name'] is not None):
					return "Full Name: " + keybase_dict['them'][0]['profile']['full_name']
