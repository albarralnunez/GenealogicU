from neomodel import (StructuredNode, StringProperty, IntegerProperty,
    RelationshipTo, RelationshipFrom, Relationship, One, DateProperty,
    db, JSONProperty)
from geocode_service import Client
import os

try:
	GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
except:
	raise EnvironmentError('GOOGLE_API_KEY envrioment variable not found')


class ComponentType(StructuredNode):
	name = StringProperty(unique_index=True)


class AddressComponent(StructuredNode):
	id = StringProperty(unique_index=True, required=True)
	components = JSONProperty()
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)
	belongs = RelationshipFrom('AddressComponent', 'SUBSECTION')
	subsection = RelationshipTo('AddressComponent', 'SUBSECTION')
	types = RelationshipTo(ComponentType, 'TYPE')

class Location:
	
	def __init__(self, *args, **kwargs):
		if 'address_components' in kwargs:
			self.address_components = kwargs['address_components']
	
	@staticmethod
	def __make_id(components):
		return '|'.join([component['types'][0] + ':' + component['short_name']
            for component in components]).replace(" ", "")
	
	def save(self):

		address_components = self.address_components

		#Ensure valid location
		client_geocode = Client.Instance()
		response = client_geocode.request_component(self.address_components)
		#If not valid throw exception
		if response['status'] == 'ZERO_RESULTS':
			raise ValueError('Invalid component')

		last_component = None
		act_component = None
		#Start creating nodes for each component
		for _ in self.address_components:
			id = self.__make_id(address_components)

			act_component = list(AddressComponent.nodes.filter(id=id))

			if not act_component:
				act_component = AddressComponent(
					id=self.__make_id(address_components),
					components=address_components,
					long_name=address_components[0]['long_name'],
					short_name=address_components[0]['short_name']
				).save()

				for component_type in address_components[0]['types']:
					type_node = list(ComponentType.nodes.filter(name=component_type))
					if type_node:
						act_component.types.connect(type_node[0])
					else:
						type_node = ComponentType(name=component_type).save()
						act_component.types.connect(type_node)
			else:
				act_component = act_component[0]
			
			if last_component:
				act_component.subsection.connect(last_component)
			
			last_component = act_component
			address_components = address_components[1:]
		return act_component

	def get(self, address_components):
		id = self.__make_id(address_components)
		return AddressComponent.nodes.filter(id=id)
