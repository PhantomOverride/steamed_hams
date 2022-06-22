import random

from steamed_hams.inserter import Inserter
import os
import argparse
import names
import config



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

    i = Inserter("bolt://192.168.27.144:7687", "neo4j", "security")
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

    i = Inserter("bolt://192.168.27.144:7687", "neo4j", "security")
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
    i = Inserter("bolt://192.168.27.144:7687", "neo4j", "security")
    i.create_relationships()

def reset():
    i = Inserter("bolt://192.168.27.144:7687", "neo4j", "security")
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
    parser.add_argument("-p", "--profiles", help="Upload Steam Profiles")
    parser.add_argument("-g", "--groups", help="Upload Steam Groups")
    parser.add_argument("-d", "--detections", help="Upload Detections")
    parser.add_argument("-v", "--debug", help="Debug output", action="store_true")
    parser.add_argument("-r", "--retrieve", help="Retrieve all Aliases")
    parser.add_argument("--random", help="????", action="store_true")

    return parser.parse_args()

def main(args):
    print(config.hams_welcome)

    if args.random:
        reset()
        dummy_insert_data()

    elif args.upload:
        if args.profiles is not None:
            if args.groups is not None:
                if args.detections is not None:
                    pass # do work
                else:
                    print("[ Error ] Detections missing, exiting ...")
            else:
                print("[ Error ] Groups missing, exiting ...")
        else:
            print("[ Error ] Profiles missing, exiting ...")

    elif args.retrieve is not None:
        retrieve_all_aliases(args.retrieve)

    #reset()
    #dummy_insert_data()
    #make_relations()

if __name__ == "__main__":
    args = parse_args()
    main(args)



