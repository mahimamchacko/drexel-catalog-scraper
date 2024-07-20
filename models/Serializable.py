import json
from encoders.ComplexEncoder import ComplexEncoder

class Serializable:
    """
    Serialize an object
    """

    def toJSON(self):
        """
        Convert an object into a string with its JSON value
        :rtype: str
        """
        
        return json.dumps(self, indent=2, cls=ComplexEncoder)
    
    def toDictionary(self):
        """
        Convert an object into a dictionary
        :rtype: dict
        """
        
        dictionary = self.__dict__
        for key, value in dictionary.items():
            if isinstance(value, Serializable):
                dictionary[key] = value.toDictionary()
            elif (type(value) is list or type(value) is set) and any([isinstance(subvalue, Serializable) for subvalue in value]):
                sublist = []
                for subvalue in value:
                    if isinstance(subvalue, Serializable):
                        sublist.append(subvalue.toDictionary())
                    else:
                        sublist.append(subvalue)
                dictionary[key] = sublist
        return dictionary