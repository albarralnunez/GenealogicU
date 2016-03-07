#!/usr/bin/env python

import subprocess

GOOGLE_API_KEY = \
    'GOOGLE_API_KEY=AIzaSyCGvJsgeaPy5xQlIPjLrDSDB5QSrBfEqYE'
NEO4J_REST_URL = \
    'NEO4J_REST_URL=http://neo4j:neo4j@localhost:7474/db/data/'

subprocess.call(["export", GOOGLE_API_KEY])
subprocess.call(["export", NEO4J_REST_URL])
