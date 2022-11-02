import http.client, urllib.parse
import pandas as pd

df = pd.read_csv("./chl_pp.csv")
df = df[df["COD_ENSE2"] == 2]
df["NOM_COM_RBD"] = df["NOM_COM_RBD"].str.lower()
df["NOM_DEPROV_RBD"] = df["NOM_DEPROV_RBD"].str.lower()
print(df.head())

lats, lngs, codes = [], [], []

conn = http.client.HTTPConnection('api.positionstack.com')

count = 0
for col, row in df.iterrows():

    try:

        # print(row.NOM_RBD, row.NOM_COM_RBD, row.NOM_DEPROV_RBD)

        params = urllib.parse.urlencode({
            'access_key': '29bd1f83e2a927e469d0fcf48d5c2645',
            'query': row.NOM_RBD,
            'country': 'CL',
            'region': row.NOM_COM_RBD,
            'neighbourhood': row.NOM_DEPROV_RBD,
            'limit': 1
            })

        conn.request('GET', '/v1/forward?{}'.format(params))
        res = conn.getresponse()

        data = res.read()
        data = data.decode('utf-8')
        data = data.replace("null", '"null"')
        data = eval(data)

        # print(data)

        lat = data['data'][0]['latitude']
        lng = data['data'][0]['longitude']

        lats.append(lat)
        lngs.append(lng)
        codes.append(row.RBD)       

        print(count, " out of ", len(df), end = "\r")

    except:

        pass


df = pd.DataFrame()
df['school_id'] = codes
df['latitude'] = lats
df['longitude'] = lngs


print(df)

df.to_csv("./chl_geocoded.csv", index = False)