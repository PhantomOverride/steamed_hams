from neo4j import GraphDatabase

class Inserter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()


    @staticmethod
    def _create_and_return_profile(tx, profile):
        result = tx.run("CREATE (a:steamprofile) "
                        "SET a.miniid = $miniid "
                        "SET a.name = $name "
                        "SET a.aliases = $aliases "
                        "SET a.friends = $friends "
                        "SET a.groups = $groups "
                        "SET a.country = $country "
                        "RETURN a", miniid=profile["miniid"], name=profile["name"], aliases=profile["aliases"], friends=profile["friends"], groups=profile["groups"], country=profile["country"])
        return result.single()[0]

    @staticmethod
    def _create_and_return_group(tx, group):
        result = tx.run("CREATE (a:steamgroup) "
                        "SET a.miniid = $miniid "
                        "SET a.name = $name "
                        "SET a.members = $members "
                        "RETURN a", miniid=group["miniid"], name=group["name"], members=group["members"])
        return result.single()[0]

    @staticmethod
    def _create_and_return_detection(tx, detection):
        result = tx.run("CREATE (a:detection) "
                        "SET a.name = $name "
                        "SET a.network = $network "
                        "SET a.url = $url "
                        "SET a.info = $info "
                        "RETURN a", name=detection["name"], network=detection["network"],
                        url=detection["url"], info=detection["info"])
        return result.single()[0]

    def insert_profile(self, profile):
        print("[ Inserter ] [ insert_profile ]")
        with self.driver.session() as session:
            res = session.write_transaction(self._create_and_return_profile, profile)
            session.write_transaction(self._create_aliases, profile)
        self.close()
        return res

    def insert_group(self, group):
        print("[ Inserter ] [ insert_group ]")
        with self.driver.session() as session:
            res = session.write_transaction(self._create_and_return_group, group)
        self.close()
        return res

    def insert_detection(self, detection):
        print("[ Inserter ] [ insert_detection ]")
        with self.driver.session() as session:
            res = session.write_transaction(self._create_and_return_detection, detection)
        self.close()
        return res

    def burn_everything(self):
        print("[ Inserter ] [ burn_everything ]")
        with self.driver.session() as session:
            session.write_transaction(self._burn_everything)
        self.close()
        return

    @staticmethod
    def _merge_friends(tx):
        result = tx.run("MATCH (a:steamprofile), (b:steamprofile) "
            "WHERE any(x IN a.friends WHERE x = b.miniid) "
            "MERGE (a)-[:FRIENDS]->(b)")
        return

    @staticmethod
    def _burn_everything(tx):
        result = tx.run("MATCH (n1) DETACH DELETE n1")
        return

    @staticmethod
    def _merge_groups(tx):
        result = tx.run("MATCH (a:steamprofile), (b:steamgroup) "
                        "WHERE any(x IN a.groups WHERE x = b.miniid) "
                        "MERGE (a)-[:MEMBER]->(b)")
        result = tx.run("MATCH (a:steamgroup), (b:steamprofile) "
                        "WHERE any(x IN a.members WHERE x = b.miniid) "
                        "MERGE (a)-[:CONTAINS]->(b)")
        return

    @staticmethod
    def _merge_aliases(tx):
        result = tx.run("MATCH (a:steamprofile), (b:steamalias) "
                        "WHERE a.miniid = b.miniid "
                        "MERGE (a)-[:ALIAS]->(b)")

        return

    @staticmethod
    def _merge_detections(tx):
        result = tx.run("MATCH (a:steamalias), (b:detection) "
                        "WHERE a.name = b.name "
                        "MERGE (a)-[:DETECTED]->(b)")
        return

    @staticmethod
    def _create_aliases(tx, profile):
        for al in profile["aliases"]:
            result = tx.run("CREATE (a:steamalias) "
                        "SET a.miniid = $miniid "
                        "SET a.name = $alias "
                        "RETURN a", miniid=profile["miniid"], alias=al)
        return

    def create_relationships(self):
        print("[ Inserter ] [ create_relationships ]")

        with self.driver.session() as session:
            res = session.write_transaction(self._merge_friends)
            res = session.write_transaction(self._merge_groups)
            res = session.write_transaction(self._merge_aliases)
            res = session.write_transaction(self._merge_detections)
        self.close()
        return

    @staticmethod
    def _find_all_aliases(tx):
        result = tx.run("MATCH (a:steamalias) RETURN (a.name)")
        return result

    def find_all_aliases(self):
        print("[ Inserter ] [ find_all_aliases ]")
        with self.driver.session() as session:
            res = session.run("MATCH (a:steamalias) RETURN (a.name)")
            r = []
            for row in res:
                r.append(row.get("(a.name)"))
        self.close()
        return r