from pymongo import MongoClient

class VKRemoteMDB:

    def __init__(self, collection_name):
        cluster = MongoClient(
            "mongodb+srv://admin:admin0000@cluster0.ueseg.mongodb.net/AutomationViewerBackend?retryWrites=true&w=majority")
        db = cluster['AutomationViewer']
        self.collection = db[str(collection_name)]  # это коллекция

    def get_all(self):
        return [el for el in self.collection.find({})]

    def insert(self, posts):
        self.collection.insert_many(posts)

    def find(self, query):
        return [el for el in self.collection.find(query)]

    def update_one(self, query, new_value):
        self.collection.update_many(query, {"$set": new_value})