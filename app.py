import pymongo
client = pymongo.MongoClient("mongodb+srv://bodyaskripnik:789258789Lp@cluster.s1u7z.mongodb.net/?retryWrites=true&w=majority")
db = client.my_base#Если у нас нет такой базы то мы ее создаем 
collection = db.my_Collection#Если у нас нет такой колекции то мы ее создаем 


collection.insert_one({
    "_id": 2,
    "name":"Oleg"
})


