import json
 
# Data to be written
current = 'F4'

dictionary = current
 
# Serializing json
json_object = json.dumps(dictionary, indent=0)
 
# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)
