import pandas as pd
import urllib, os
import os
import urllib.request
import json

geo = pd.read_csv("./pp_wlocs.csv", encoding= 'unicode_escape')
print(geo.head(5))



def GetGoogleStatic(name, state, munic, school_id):
	# try:
    base = "https://maps.googleapis.com/maps/api/geocode/json?address="   
    url = base + name.replace(" ", "+") + '&components=sublocality:' + munic.replace(" ", "+") + '|country:CR&type=school|university|primary_school|secondary_school&country=BR&key=AIzaSyCZBofNx706aAsG5_BzXzXE9cdy-Du2PdE'
    # url = base + name.replace(" ", "+") + '&components=locality:' + state.replace(" ", "+") +'|sublocality:' + munic.replace(" ", "+") + '|country:CR&type=school|university|primary_school|secondary_school&country=BR&key=AIzaSyCZBofNx706aAsG5_BzXzXE9cdy-Du2PdE'
    file = "./jsons4/" + str(school_id) + ".json"
    urllib.request.urlretrieve(url, file)
	# except:
	# 	print("Couldn't save file: " + str(school_id))


# count = 0

# for index, row in geo[0:3].iterrows():
# 	msg = "File #" + str(count)
# 	print(msg)
# 	GetGoogleStatic(row['NOMBRE_x'], row['CANTON'], row['POBLADO'], int(row['CODIGO']))
# 	count += 1

	