import json;
import urllib.request;

def RunModule(name):
	try:
		# Pull page text
		req = urllib.request.Request("https://medium.com/@" + name, headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'    })
		pageData = urllib.request.urlopen(req).read().decode("utf8")
		# Hack to get the name
		name = pageData.split("<title data-rh=\"true\">")[1].split("</title>")[0]
		if ("–" in name):
			name = name.split("–")[0]
			return "Real Name: " + name;
	except:
		return "Error - Please investigate";
