from geocode_service import Client
from neomodel import (
    StructuredNode, StringProperty, JSONProperty,
    RelationshipTo, RelationshipFrom)


class RootLocation(StructuredNode):
    name = StringProperty(unique_index=True, default='root_location')
    location = RelationshipTo('AddressComponent', 'ROOT_LOCATION')


class ComponentType(StructuredNode):
    name = StringProperty(unique_index=True)


class AddressComponent(StructuredNode):
    id = StringProperty(unique_index=True)
    address = JSONProperty()
    place_id = StringProperty()
    formatted_address = StringProperty(index=True)
    belongs = RelationshipFrom('AddressComponent', 'SUBSECTION')
    subsection = RelationshipTo('AddressComponent', 'SUBSECTION')
    types = RelationshipTo(ComponentType, 'TYPE')

    def __init__(self, address, **args):

        def __make_id(components):
            return '/'.join(
                    [component['long_name'] for component in components]
                ).replace(" ", "")

        def __format_address(components):
            return ', '.join(
                [component['long_name'] for component in components]
            )

        super(AddressComponent, self).__init__(**args)

        self.__make_id = __make_id
        self.address = address
        self.id = __make_id(address)
        self.formatted_address = __format_address(address)

    @classmethod
    def get(self, components):
        id = '/'.join(
            [component['long_name'] for component in components]
            ).replace(" ", "")
        return self.nodes.filter(id=id)


class Location:

    def __init__(self, *args, **kwargs):
        self.client = Client.Instance()
        self.address_components = None
        self.place_id = None
        if 'address_components' in kwargs:
            self.address_components = filter(
                lambda x: 'postal_code' not in x['types'],
                kwargs['address_components'])
        if 'place_id' in kwargs:
            self.place_id = kwargs['place_id']

    def save(self):
        if self.address_components:
            response = self.client.request_component(self.address_components)
        if self.place_id:
            response = self.client.request_place_id(self.place_id)

        if response['status'] == 'ZERO_RESULTS':
            raise ValueError('Invalid address')

        address_components = response['results'][0]['address_components']
        address_components = filter(
                lambda x: 'postal_code' not in x['types'],
                address_components)

        last_component = None
        fst_node = None

        while address_components:

            act_component = list(AddressComponent.get(address_components))

            if not act_component:
                act_component = AddressComponent(
                    address=address_components,
                ).save()

                for component_type in address_components[0]['types']:
                    type_node = list(
                        ComponentType.nodes.filter(name=component_type)
                        )
                    if type_node:
                        act_component.types.connect(type_node[0])
                    else:
                        type_node = ComponentType(
                            name=component_type).save()
                        act_component.types.connect(type_node)
            else:
                act_component = act_component[0]

            if last_component:
                act_component.subsection.connect(last_component)
            last_component = act_component
            if not fst_node:
                fst_node = act_component
            address_components = address_components[1:]

        root = list(RootLocation.nodes.all())
        if not root:
            raise EnvironmentError('Execute ./manage.py setup_loc_environ')
        root[0].location.connect(last_component)

        return fst_node

    @classmethod
    def get(self, address_components):
        return AddressComponent.get(address_components)
