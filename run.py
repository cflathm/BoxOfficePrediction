import wikiscrap
import pickle
import json

data = wikiscrap.main()

with open('data.p', 'wb') as fp:
    pickle.dump(data, fp, protocol=pickle.HIGHEST_PROTOCOL)
with open('data.p', 'rb') as fp:
    data = pickle.load(fp)

with open('data.json', 'w') as fp:
    json.dump(data, fp)
with open('data.json', 'r') as fp:
    data = json.load(fp)

