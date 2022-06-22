import requests
import json
import sys
from bs4 import BeautifulSoup
import re

class Steaming:
    def __init__(self):
        self.template = {
            "miniid": "",
            "name": "",
            "aliases": [],
            "friends": [],
            "groups": [],
            "country": ""
        }
        self.profile = self.template
        self.friend_profiles = []

        #self.groups_todo = []
        self.friends_todo = []

        self.username = ""
        #print("usr", self.username)

    def do_work(self, username):
        self.username = username
        self.profile['aliases'] = self.get_aliases(username)
        self.profile['friends'] = self.get_friends(username)
        self.profile['groups'] = self.get_groups(username)
        self.profile['miniid'] = self.get_id(username)
        self.profile['name'] = self.get_name(username)

        return self.profile



    def Make_POST(self,url, headers):
        r = requests.post(url, headers=headers)

        return r.text

    def Make_GET(self, url):
        r = requests.get(url)
        return r

    def get_id(self, username):
        url_ID = "https://steamcommunity.com/id/{}/".format(username)

        print("Getting users ID")
        results = re.search("miniprofile=\"(.*)\"", self.Make_GET(url_ID).text)
        # self.profile['miniid'] = results[1]
        return results[1]

    def get_friend_usernames(self, username):
        url_ID = "https://steamcommunity.com/id/{}/friends/".format(username)

        print("Getting users ID")
        d = self.Make_GET(url_ID).text
        #print(d)
        results = re.findall("<a class=\"selectable_overlay\" data-container=\"#[a-z]+_(\d*)\" href=\"https://steamcommunity.com/id/(.*)\">", d)
        #print(results)
        #print(results[:])
        return results[:]

    def get_name(self, username):
        print("Getting name")
        url_ID = "https://steamcommunity.com/id/{}/".format(username)

        results = re.search("<title>Steam Community :: (.*)\<", self.Make_GET(url_ID).text)
        #self.profile['name'] = results[1]
        return results[1]

    def get_aliases(self, username):
        url_alias = "https://steamcommunity.com/id/{}/ajaxaliases/".format(username)
        print(url_alias)
        headers = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Accept': 'text/plain'}

        alias = []

        ##Parsing json data
        print("Getting Aliases")
        p = self.Make_POST(url_alias, headers)
        #print(p)
        for a in json.loads(p):
            alias.append(a['newname'])
        # print(a['newname'])

        #self.profile['aliases'] = alias
        return alias

    def get_groups(self, username):
        url_group = "https://steamcommunity.com/id/{}/groups/".format(username)

        soup = BeautifulSoup(self.Make_GET(url_group).text, 'html.parser')

        groups = []

        print("All the users groups:")
        for a in soup.find_all("a", class_='linkTitle'):
            groups.append(a.get_text())
        # print (a.get_text())

        #self.profile['groups'] = groups
        return groups

    def get_friends(self, username):
        # Getting friends
        url_FR = "https://steamcommunity.com/id/{}/friends".format(username)

        print("Getting friends")
        results = re.findall("miniprofile=\"(.*)\"", self.Make_GET(url_FR).text)
        #self.profile['friends'] = results
        return results
        # print(profile)