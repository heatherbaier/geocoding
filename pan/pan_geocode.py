import http.client, urllib.parse
import pandas as pd


df = pd.read_csv("./pan_primary_pp.csv")
print(df.shape)

df = df.drop_duplicates(subset = ["COD. COLEGIO"])
print(df.shape)
print(df.columns)
df = df[['COD. COLEGIO', ' REGIONAL', ' PROVINCIA', ' DISTRITO', ' CORREGIMIENTO', ' NOMBRE COLEGIO']]
df = df.rename(columns = {"COD. COLEGIO": "school_id", ' NOMBRE COLEGIO': "school_name", ' REGIONAL': 'region', ' CORREGIMIENTO': 'CORREGIMIENTO'})
# df = df[['Clave_primaria','Clave_periodo','Periodo','Zona','Provincia','Canton','Parroquia','Nombre_Institucion']]
print(df.head(10))

lats, lngs, codes = [], [], []

conn = http.client.HTTPConnection('api.positionstack.com')

count = 0
for col, row in df.iterrows():

    try:

        # print(row.NOM_RBD, row.NOM_COM_RBD, row.NOM_DEPROV_RBD)

        params = urllib.parse.urlencode({
            'access_key': '29bd1f83e2a927e469d0fcf48d5c2645',
            'query': row.school_name,
            'country': 'PA',
            'region': row.region,
            'neighbourhood': row.CORREGIMIENTO,
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
        codes.append(row.school_id)       

        count += 1

        print(count, " out of ", len(df), end = "\r")

    except:

        pass


df = pd.DataFrame()
df['school_id'] = codes
df['latitude'] = lats
df['longitude'] = lngs


print(df)

df.to_csv("./pan_geocoded.csv", index = False)