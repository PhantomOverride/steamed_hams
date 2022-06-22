import random

from steamed_hams.inserter import Inserter
from steamed_hams.steaming import Steaming
import os
import argparse
import names
import config
import json



def dummy_insert_profile():
    profile = {
        "miniid": "0000",
        "name": "Time Turkey",
        "aliases": ["Crunchy Bobby", "5H3PH3RD"],
        "friends": ["1111", "2222", "3333"],
        "groups": [],
        "country": "Sweden",
    }

    profile["miniid"] = random.randint(1001, 9999)
    profile["name"] = names.get_last_name()
    profile["aliases"][0] = names.get_last_name()
    profile["aliases"][1] = names.get_last_name()
    profile["friends"][0] = str(random.randint(1001, 9999))
    profile["friends"][1] = str(random.randint(1001, 9999))
    profile["groups"][0] = str(random.randint(1001, 9999))
    profile["groups"][1] = str(random.randint(1001, 9999))
    profile["country"] = "Unknown"

    i = Inserter(config.hams_server, config.hams_username, config.hams_password)
    i.insert_profile(profile)

def dummy_insert_data():
    profiles = []
    profiles.append({
        "miniid": "0001",
        "name": "Alice",
        "aliases": ["alice1", "alice2"],
        "friends": ["0002", "0003", "0005"],
        "groups": ["1000"],
        "country": "Sweden",
    })
    profiles.append({
        "miniid": "0002",
        "name": "Bob",
        "aliases": ["bob1", "bob2"],
        "friends": ["0001"],
        "groups": ["1000"],
        "country": "Sweden",
    })
    profiles.append({
        "miniid": "0003",
        "name": "Charlie",
        "aliases": ["charlie1", "charlie2"],
        "friends": ["0001", "0004"],
        "groups": ["1001"],
        "country": "Sweden",
    })
    profiles.append({
        "miniid": "0004",
        "name": "Dennis",
        "aliases": ["dennis1", "dennis2"],
        "friends": ["0003", "0005"],
        "groups": [],
        "country": "Sweden",
    })
    profiles.append({
        "miniid": "0005",
        "name": "Elisabeth",
        "aliases": ["elisabeth1", "elisabeth2"],
        "friends": ["0004", "0001"],
        "groups": [],
        "country": "Sweden",
    })

    i = Inserter(config.hams_server, config.hams_username, config.hams_password)
    for profile in profiles:
        i.insert_profile(profile)

    groups = []
    groups.append({
        "miniid": "1000",
        "name": "cool people group",
        "members": ["0001", "0002"]
    })
    groups.append({
        "miniid": "1001",
        "name": "forever alone group",
        "members": ["0003"]
    })

    for group in groups:
        i.insert_group(group)

    detections = []
    detections.append({
        "name": "elisabeth2",
        "network": "Twitter",
        "url": "http://example.com/",
        "info": "some data"
    })
    detections.append({
        "name": "bob1",
        "network": "Github",
        "url": "http://example.com/",
        "info": "some data"
    })

    for detection in detections:
        i.insert_detection(detection)

def make_relations():
    i = Inserter(config.hams_server, config.hams_username, config.hams_password)
    i.create_relationships()

def reset():
    i = Inserter(config.hams_server, config.hams_username, config.hams_password)
    i.burn_everything()

def retrieve_all_aliases(savefile):
    i = Inserter(config.hams_server, config.hams_username, config.hams_password)
    results = i.find_all_aliases()
    with open(savefile, "w") as f:
        for row in results:
            f.write(row + "\n")

def parse_args():
    parser = argparse.ArgumentParser(description="Steamed Hams for Gaben!")

    parser.add_argument("-u", "--upload", help="Upload data", action="store_true")
    parser.add_argument("-x", "--reset", help="Reset db", action="store_true")
    parser.add_argument("-p", "--profiles", help="Upload Steam Profiles")
    parser.add_argument("-g", "--groups", help="Upload Steam Groups")
    parser.add_argument("-d", "--detections", help="Upload Detections")
    parser.add_argument("-v", "--debug", help="Debug output", action="store_true")
    parser.add_argument("-r", "--retrieve", help="Retrieve all Aliases")
    parser.add_argument("--random", help="????", action="store_true")
    parser.add_argument("-s", "--steam", help="Enumerate Steam User")

    return parser.parse_args()

def insert_detections(detections):
    print("[ Hams ] insert_detections")
    i = Inserter(config.hams_server, config.hams_username, config.hams_password)
    with open(detections, "r") as f:
        data = json.load(f)
        for obj in data:
            i.insert_detection(obj)
        i.create_relationships()

def insert_profiles(profiles):
    print("[ Hams ] insert_profiles")
    i = Inserter(config.hams_server, config.hams_username, config.hams_password)
    with open(profiles, "r") as f:
        data = json.load(f)
        for obj in data:
            i.insert_profile(obj)
        i.create_relationships()

def insert_profiles_internal(profiles):
    print("[ Hams ] insert_profiles")
    i = Inserter(config.hams_server, config.hams_username, config.hams_password)
    for profile in profiles:
        i.insert_profile(profile)
    i.create_relationships()

def insert_groups(groups):
    print("[ Hams ] insert_groups")
    i = Inserter(config.hams_server, config.hams_username, config.hams_password)
    with open(groups, "r") as f:
        data = json.load(f)
        for obj in data:
            i.insert_group(obj)
        i.create_relationships()

def steam(username):
    s = Steaming()
    main = s.do_work(username)
    friends = s.get_friend_usernames(username)
    friend_profile = []
    for friend in friends:
        #print(friend[1])
        s = Steaming()
        try:
            friend_profile.append( s.do_work(friend[1]) )
        except:
            print(".. Just ignoring some errors ...")

    print("Finished! Inserting...")
    insert_profiles_internal([main] + friend_profile)

    #print(main)
    #print(len(friend_profile))



    #result = s.get_friend_usernames(username)
    #print(result)

def main(args):
    print(config.hams_welcome)

    if args.reset:
        reset()

    if args.random:
        reset()
        dummy_insert_data()

    if args.steam:
        steam(args.steam)

    elif args.upload:
        if args.profiles is not None:
            if args.groups is not None:
                insert_profiles(args.profles)
                insert_groups(args.groups)

            else:
                print("[ Error ] Groups missing, exiting ...")

        elif args.detections is not None:
            insert_detections(args.detections)

        else:
            print("[ Error ] Profiles or Detections missing, exiting ...")

    elif args.retrieve is not None:
        retrieve_all_aliases(args.retrieve)

    #reset()
    #dummy_insert_data()
    #make_relations()

if __name__ == "__main__":
    args = parse_args()
    main(args)



