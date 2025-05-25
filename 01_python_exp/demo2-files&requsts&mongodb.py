import json
import requests
from pymongo import MongoClient

# Ex1
def find_persons_in_street(street):

    with open('./data.json') as f:
        data = json.load(f)

        return [
            {'Name': p['Name'], 'City': p['Address']['City'], 'Street': street}
            for p in data['persons']
            if p['Address']['Street']['Name'] == street
        ]


print(find_persons_in_street('Yirmiyahu'))

# # Ex2
id = input("Enter yout Id\n")
res = requests.get("https://jsonplaceholder.typicode.com/users/" + id)
if res.status_code == 200:
    user = res.json()
    print(user["name"] + " " + user["email"])
    if user["name"][0] == "E":
        res = requests.get("https://jsonplaceholder.typicode.com/todos?userId=" + id)
        if res.status_code == 200:
            user_todos = res.json()
            titles = list(map(lambda t: t["title"], user_todos))
            with open(f'todos_{id}.json', 'w') as f:
                json.dump(titles, f)

# Ex3
client = MongoClient(port=27017)
db = client["ai"]
shows_collection = db["shows"]

with open("./shows.json", encoding="utf8") as f:
    data = json.load(f)
    data_to_save = map(
        lambda s: {
            "_id": s["id"],
            "Name": s["name"],
            "Genres": s["genres"],
            "Average rating": s["rating"]["average"],
        },
        data[:10],
    )
    shows_collection.insert_many(data_to_save)

show = input("which movie to update?\n")
# check if show exist
newName = input("input new name\n")

shows_collection.update_one({"Name": show}, {"$set": {"Name": newName}})
