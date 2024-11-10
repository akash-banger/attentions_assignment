from neo4j import GraphDatabase
from src.constants import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
import logging

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self):
        print(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    def close(self):
        self.driver.close()

    def store_preference(self, user_id: str, entity: str, relationship: str, value: str):
        with self.driver.session() as session:
            query = """
            MERGE (u:User {id: $user_id})
            MERGE (v:Value {name: $value})
            MERGE (u)-[r:PREFERS {type: $relationship}]->(v)
            """
            session.run(query, user_id=user_id, value=value, relationship=relationship)

    def get_preferences(self, user_id: str):
        with self.driver.session() as session:
            query = """
            MATCH (u:User {id: $user_id})-[r:PREFERS]->(v)
            RETURN r.type as relationship, v.name as value
            """
            result = session.run(query, user_id=user_id)
            return [(record["relationship"], record["value"]) for record in result]

    def store_triplet(self, user_id: str, subject: str, predicate: str, object: str):
        with self.driver.session() as session:
            query = """
            MERGE (u:User {id: $user_id})
            MERGE (s:Entity {name: $subject})
            MERGE (o:Entity {name: $object})
            MERGE (s)-[r:RELATION {type: $predicate, user_id: $user_id}]->(o)
            """
            session.run(query, user_id=user_id, subject=subject, predicate=predicate, object=object) 
            
    def create_user_if_not_exists(self, user_id: str):
        with self.driver.session() as session:
            query = """
            MERGE (u:User {id: $user_id})
            RETURN u
            """
            session.run(query, user_id=user_id)

    def store_preference(self, user_id: str, preference_data: dict):
        with self.driver.session() as session:
            query = """
            MATCH (u:User {id: $user_id})
            CREATE (p:Preference $preference_data)
            CREATE (u)-[r:PREFERS]->(p)
            RETURN p
            """
            session.run(query, user_id=user_id, preference_data=preference_data)