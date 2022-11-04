import http.client, urllib.parse
import pandas as pd

locs = pd.read_csv("./more_locs.csv")
# locs["id_centro"] = locs["id_centro"].astype(int)
print(locs.head())

with open("./pass_percents2.txt", "r") as f:
    pp = f.read().splitlines()
pp = pd.DataFrame([i.split(" ") for i in pp])
pp.columns = ["id", "pass_percent"]
print(pp)


with open("./id_refs.txt", "r") as f:
    ids = f.read().splitlines()
ids = pd.DataFrame([i.split(" ") for i in ids])
ids.columns = ["id", "Codigo"]
ids = pd.merge(ids, pp, on = "id")
ids = ids.drop_duplicates(subset = ["Codigo"])
ids["Codigo"] = ids["Codigo"].astype(float)#.astype(int)


df = pd.merge(ids, locs, on = "Codigo")
df = df.drop_duplicates(subset = ["Codigo"])
df = df[['Centro', 'Departamento', 'Municipio', 'Aldea', 'Caserio']]
print(df)

print(df.columns)



conn = http.client.HTTPConnection('api.positionstack.com')

# count = 0
# for col, row in df.iterrows():

#     try:

# print(row.NOM_RBD, row.NOM_COM_RBD, row.NOM_DEPROV_RBD)

params = urllib.parse.urlencode({
    'access_key': '29bd1f83e2a927e469d0fcf48d5c2645',
    'query': "JUAN RAMON MIRALDA",
    'country': 'HN',
    'region': 'Olancho',
    'neighbourhood': "Froylan Turcios",
    'limit': 1
    })

conn.request('GET', '/v1/forward?{}'.format(params))
res = conn.getresponse()

data = res.read()
data = data.decode('utf-8')
data = data.replace("null", '"null"')
data = eval(data)

print(data)