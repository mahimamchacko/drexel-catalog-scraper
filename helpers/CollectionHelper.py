import config
import pymongo

class CollectionHelper():
    """
    Help update the collection in the databse
    """
    
    def __init__(self, database: str, collection: str) -> None:
        self.client = pymongo.MongoClient(config.MONGODB_LINK)
        
        if database not in self.client.list_database_names():
            raise AttributeError(f"Client has no database '{database}'.")
        self.database = self.client[database]
        
        if collection not in self.database.list_collection_names():
            raise AttributeError(f"Database has no collection '{collection}'.")
        self.collection = self.database[collection]

    def publish(self, values: list):
        """
        Publish values to the collection (insert, update, delete)
        :param values: Values from the data
        :type values: list
        """

        obj_type = type(values[0]) if len(values) > 0 else None
        curr_values = self.__create_dictionary(obj_type)
        
        insert_values = []
        update_values = []
        for object in values:
            key = object.get_key()
            value = object.toDictionary()
            if key in curr_values:
                if not(obj_type.equals(curr_values[key], value)):
                    update_values.append(value)
                curr_values.pop(key)
            else:
                insert_values.append(value)
        delete_values = list(curr_values.values())
        
        self.__check_insert_many(insert_values)
        self.__check_update_many(obj_type, update_values)
        self.__check_delete_many(delete_values)

    def __create_dictionary(self, type: type) -> dict:
        """
        Create a dictionary of the values in the collection
        :param type: Type of object
        :type type: type
        :rtype: dict
        """

        old_values = {}
        for value in self.collection.find():
            old_values[type.get_json_key(value)] = value
        return old_values

    def __check_insert_many(self, values: list):
        """
        Validate and insert values into the collection
        :param values: List of values to insert
        :type values: list
        """
        
        if len(values) > 0:
            self.collection.insert_many(values)
    
    def __check_update_many(self, type: type, values: list):
        """
        Validate and update values in the collection
        :param type: Type of object
        :type type: type
        :param values: List of values to update
        :type values: list
        """
        
        if len(values) > 0:
            for value in values:
                self.collection.update_one(type.get_dict_key(value), { "$set": value })
    
    def __check_delete_many(self, values: list):
        """
        Validate and delete values in the collection
        :param values: List of values to delete
        :type values: list
        """
        
        if len(values) > 0:
            for value in values:
                self.collection.delete_one(value)

    def __del__(self):
        self.client.close()