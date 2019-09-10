from pymongo import MongoClient
client = MongoClient('localhost', 27017)

db = client['LINE-USERS']
collection = db['user-collection']
users = collection.find()
if users.count():
    print('found')
else:
    print('not found')
cnt=0
thre=2000
upau=0
for i,user in enumerate(users):
    print(i, user)
    if(user['count'] > thre):
        cnt+=1;
    if(user['authority'] >= 1):
        upau+=1
print(f"{thre}回以上コマンドを実行した人は{cnt}人です。レベル1以上の権限保持者は{upau}人です。")

print('max count', collection.find_one(sort=[("count", -1)]))
