import pymongo

client = pymongo.MongoClient("mongodb://devman:mari2Ana23sem@34.170.242.62:27017?authSource=admin")
db = client["salesfy"]


def find_one(collection, query):
    return db[collection].find_one(query)


def find_many(collection, query):
    return db[collection].find(query)


def insert_one(collection, data):
    return db[collection].insert_one(data)


def insert_many(collection, data):
    return db[collection].insert_many(data)


def update_one(collection, query, data):
    return db[collection].update_one(query, {'$set': data}, True)


def update_many(collection, query, data):
    return db[collection].update_many(query, {'$set': data}, True)


def delete_one(collection, query):
    return db[collection].delete_one(query)


def delete_many(collection, query):
    return db[collection].delete_many(query)
