class ObjectSerializer(serializers.BaseSerializer):
    """
    A read-only serializer that coerces arbitrary complex objects
    into primitive representations.
    """
    def to_representation(self, obj):
        for attribute_name in dir(obj):
            attribute = getattr(obj, attribute_name)
            if attribute_name('_'):
                # Ignore private attributes.
                pass
            elif hasattr(attribute, '__call__'):
                # Ignore methods and other callables.
                pass
            elif isinstance(attribute, (str, int, bool, float, type(None))):
                # Primitive types can be passed through unmodified.
                output[attribute_name] = attribute
            elif isinstance(attribute, list):
                # Recursively deal with items in lists.
                output[attribute_name] = [
                    self.to_representation(item) for item in attribute
                ]
            elif isinstance(attribute, dict):
                # Recursively deal with items in dictionaries.
                output[attribute_name] = {
                    str(key): self.to_representation(value)
                    for key, value in attribute.items()
                }
            else:
                # Force anything else to its string representation.
                output[attribute_name] = str(attribute)
