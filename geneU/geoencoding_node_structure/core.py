from neomodel import (StructuredNode, StringProperty, IntegerProperty,
    RelationshipTo, RelationshipFrom, Relationship, One, DateProperty,
    db)
from geonodes import *
import os

choices = (
	('street_address',1),
	('route',2),
	('intersection',3),
	('ponint_of_interest',4),
	('airport',5),
	('natural_feature',6),
	('country',7),
	('administrative_area_level_1',8),
	('administrative_area_level_2',9),
	('administrative_area_level_3',10),
	('administrative_area_level_4',11),
	('administrative_area_level_5',12),
	('locality',13),
	('sublocality_level_1',14),
	('sublocality_level_2',15),
	('sublocality_level_3',16),
	('sublocality_level_4',17),
	('sublocality_level_5',18)
)

try:
	GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
except:
	raise StandardError('GOOGLE_API_KEY envrioment variable not found')

class ComponentType(StructuredNode):
	name = StringProperty(index=True, choices=choices)

class AddressComponent(StructuredNode):
	id = StringProperty(unique_index=True, required=True)
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)
	belongs = RelationshipFrom('AddressComponent', 'HAS')
	has = RelationshipTo('AddressComponent', 'HAS')
	types = RelationshipTo(ComponentType, 'TYPE')

class Location(object):

	def __init__(self, address_components):
		self.address_components = address_components
		last_component = None
		for component in self.address_components:
			act_component = AddressComponent(
				long_name=component['long_name'],
				short_name=component['short_name']
			).save()
			#for component_type in component['types']:
