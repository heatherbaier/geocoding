import http.client, urllib.parse
import pandas as pd


df = pd.read_csv("./ecu_pp.csv")
df = df[['Clave_primaria','Clave_periodo','Periodo','Zona','Provincia','Canton','Parroquia','Nombre_Institucion']]
print(df.head(10))


# EC


conn = http.client.HTTPConnection('api.positionstack.com')

# count = 0
# for col, row in df.iterrows():

#     try:

        # print(row.NOM_RBD, row.NOM_COM_RBD, row.NOM_DEPROV_RBD)

params = urllib.parse.urlencode({
    'access_key': '29bd1f83e2a927e469d0fcf48d5c2645',
    'query': 'CENTRO EDUCATIVO ROUSSEAU',
    'country': 'EC',
    'region': 'Zona 6',
    'neighbourhood': 'CUENCA',
    'limit': 1
    })

conn.request('GET', '/v1/forward?{}'.format(params))
res = conn.getresponse()

data = res.read()
data = data.decode('utf-8')
data = data.replace("null", '"null"')
data = eval(data)

print(data)