#!/usr/bin/env python
from neomodel import db
from .geneU.geneTree.models import Person


person = Person.nodes.get(id='1a9445da-4494-45ab-b0c2-d04ab41262e7')

query = '''
        START a=node({person}) MATCH a<-[:MEMBER]-(b) RETURN b")
        '''

results, meta = db.cypher_query(query, person=person)
people = [Person.inflate(row[0]) for row in results]
