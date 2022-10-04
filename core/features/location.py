import requests
from pprint import pprint
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('--ip', type=str, help='Enter a IP address or list of IP addresses separated by ","',required=True)
args = parser.parse_args()

ip_list = args.ip.split(",")
url = "http://ip-api.com/batch?fields=query,status,message,country,countryCode,regionName,city"
data = json.dumps(ip_list)
r = requests.post(url,data = data)

for i in range(len(r.json())):
	print("\n"+str(i+1)+". Location lookup for "+r.json()[i]['query']+": ")
	for key,val in r.json()[i].items():
		print("   "+key+": "+val)
