from neomodel import (StructuredNode, StringProperty, IntegerProperty,
    RelationshipTo, RelationshipFrom, Relationship, One, DateProperty,
    db)

class StreetAddress(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class Route(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class Intersection(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class PointOfInterest(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class Airport(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class NaturalFeature(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class Country(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class AdministrativeAreaLevel1(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class AdministrativeAreaLevel2(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class AdministrativeAreaLevel3(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class AdministrativeAreaLevel4(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class AdministrativeAreaLevel5(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class Locality(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class SublocalityLevel1(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class SublocalityLevel2(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class SublocalityLevel3(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class SublocalityLevel4(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)

class SublocalityLevel5(StructuredNode):
	long_name = StringProperty(index=True, required=True)
	short_name = StringProperty(index=True)
