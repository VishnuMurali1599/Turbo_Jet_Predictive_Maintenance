from pymongo.mongo_client import MongoClient

class new_Data_storage:
    
    def __init__(self,dbname:str,collectionanme:str):
        self.__password = "Vishnu8748803252"
        self.dbname = dbname
        self.collection_name = collectionanme
        
    def conection(self):
        uri = "mongodb+srv://vishnumurali835:{}@vishnumurali.gan12f1.mongodb.net/?retryWrites=true&w=majority".format(self.__password)
        # Create a new client and connect to the server
        client = MongoClient(uri)
        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

        database=client[self.dbname]
        collection = database[self.collection_name]
        data = {"cycle": self.cycle,"op1": self.op1,"op2": self.op2,"sensor2":self.sensor2,
                "sensor3": self.sensor3,"sensor4":self.sensor4,"sensor5": self.sensor5,
                "sensor6":self.sensor6,"sensor7": self.sensor7,"sensor8":self.sensor8,
                "sensor9": self.sensor9,"sensor10":self.sensor10,"sensor11": self.sensor11,
                "sensor12": self.sensor12,"sensor13":self.sensor13,"sensor14": self.sensor14,
                "sensor15":self.sensor15,"sensor16": self.sensor16,"sensor17":self.sensor17,
                "sensor20": self.sensor20,"sensor21":self.sensor21}
        collection.insert_one(data)
        
        record = collection.find()
        for i in record :
            print(i)