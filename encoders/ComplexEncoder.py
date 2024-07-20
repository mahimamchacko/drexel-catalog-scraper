from json import JSONEncoder
from typing import Any

class ComplexEncoder(JSONEncoder):
    """
    Encode an object into its serializable format
    """

    def default(self, o: Any) -> Any:
        """
        Return a serializable object
        :param o: Object
        :type o: Any
        :rtype: Any
        """
        
        if (type(o).__module__ == object.__module__):
            return o.toJSON()
        return o.__dict__