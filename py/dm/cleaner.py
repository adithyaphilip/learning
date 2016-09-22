import json
input()
input()
j = json.loads(input())
for i in range(len(j["cards"])):
    j["cards"][i]["dbid"] = i + 1
    j["cards"][i]["img_name"] = j["cards"][i]["img_name"][:-4]
    for key,val in j["cards"][i].items():
        print(key,":",val)
    print("X")
with open("dmjson.txt", "w") as f:
    json.dump(j, f)

