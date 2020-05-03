import json
import pickle

f = open("description_yoga_json.json", "rb")
descriptions = json.load(f)
f.close()

pose_names = []
for pose in descriptions:
    pose_names.append(pose)
print(pose_names)

f = open("pose_names.json", "wb")
pickle.dump(pose_names, f)
f.close()
