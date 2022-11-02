# Python 3
import http.client, urllib.parse
import pandas as pd
import ast


geo = pd.read_csv("./pp_wlocs.csv", encoding= 'unicode_escape')
geo = geo.drop_duplicates(subset = ["CODIGO"])
geo['REGION_x'] = geo['REGION_x'].str.lower()
geo['DISTRITO'] = geo['DISTRITO'].str.lower()
print(geo.head(5))
print(geo.shape)


lats, lngs, codes = [], [], []

conn = http.client.HTTPConnection('api.positionstack.com')

for col, row in geo.iterrows():

    try:

        print(row.NOMBRE_x, row.REGION_x, row.DISTRITO)

        params = urllib.parse.urlencode({
            'access_key': '29bd1f83e2a927e469d0fcf48d5c2645',
            'query': row.NOMBRE_x,
            'country': 'CR',
            'region': row.REGION_x,
            'neighbourhood': row.DISTRITO,
            'limit': 1
            })

        conn.request('GET', '/v1/forward?{}'.format(params))

        res = conn.getresponse()
        data = res.read()

        data = data.decode('utf-8')

        # print(data)

        data = data.replace("null", '"null"')

        data = eval(data)

        # print(type(data))

        lat = data['data'][0]['latitude']
        lng = data['data'][0]['longitude']

        lats.append(lat)
        lngs.append(lng)
        codes.append(row.CODIGO)

    except:

        pass


df = pd.DataFrame()
df['school_id'] = codes
df['latitude'] = lats
df['longitude'] = lngs


print(df)


df.to_csv("./cri_goecoded.csv", index = False)

# test = '{"data":[{"latitude":9.925755,"longitude":-84.079417,"type":"venue","name":"Consejo de Transporte P\u00fablico","number":"null","postal_code":"null","street":"Calle Jos\u00e9 Mar\u00eda Ca\u00f1as","confidence":1,"region":"San Jos\u00e9","region_code":"SJ","county":"San Jose","locality":"San Jos\u00e9","administrative_area":"null","neighbourhood":"null","country":"Costa Rica","country_code":"CRI","continent":"North America","label":"Consejo de Transporte P\u00fablico, San Jos\u00e9, Costa Rica"}]}'

# print(ast.literal_eval(test))

# # print(test.split())

# # lat = test['data'][0]['latitude']
# # lng = test['data'][0]['longitude']

# # print(lat, lng)