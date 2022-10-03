import requests
from pprint import pprint
import argparse
import json
from os.path import exists

base_url = "https://cve.circl.lu/api/"

# Returns a list of vendors or products of a specific vendor
def browse(vendor):
	browse = "browse/"
	r = requests.get(base_url+browse+vendor)
	if r.json():
		if vendor:
			print("[+] Vendor: "+vendor)
			print("[+] Products count: "+str(len(r.json()["product"])))
			choice = input("[+] Do you want to print them all (y/n)? ").strip()
			if choice == 'y' or choice == 'Y':
				print("[+] List of Products: ")
				i = 0
				while i < len(r.json()["product"]):
					print(str(i+1)+". "+r.json()["product"][i])
					i += 1
		else:
			print("[+] Vendors count: "+str(len(r.json()["vendor"])))
			choice = input("[+] Do you want to print them all (y/n)? ").strip()
			if choice == 'y' or choice == 'Y':
				print("[+] List of vendors: ")
				i = 0
				while i < len(r.json()["vendor"]):
					print(str(i+1)+". "+r.json()["vendor"][i])
					i += 1
		return r.json()
	else:
		print("[-] Vendor not found")
		return "[-] Vendor not found"

# Converts a CPE code to the CPE2.2 standard
def cpe22(cpe):
	cpe22 = "cpe2.2/"
	r = requests.get(base_url+cpe22+cpe)
	if "false" not in r.text:
		print("[+] Correspoding CPE 2.2 code: "+ r.text)
		return "CPE 2.2 code for "+"\""+cpe+"\" is: "+ r.text
	else:
		print("[-] Not a valid CPE code")
		return "[-] Not a valid CPE code"

# Converts a CPE code to the CPE2.3 standard
def cpe23(cpe):
	cpe23 = "cpe2.3/"
	r = requests.get(base_url+cpe23+cpe)
	if "false" not in r.text:
		print("[+] Correspoding CPE 2.3 code: "+ r.text)
		return "CPE 2.3 code for "+"\""+cpe+"\" is: "+ r.text
	else:
		print("[-] Not a valid CPE code")
		return "[-] Not a valid CPE code"

# Outputs all available information for the specified CVE
def cve(cveid):
	cve = "cve/"
	r = requests.get(base_url+cve+cveid)
	if r.text != "null":
		print("[+] Informaton for "+cveid+": ")
		pprint(r.json())
		return r.json()
	else:
		print("[-] Not a valid CVE")
		return "[-] Not a valid CVE"


# Outputs the last n amount of vulnerabilities
# default limit is 30
def last(limit):
	last = "last/"
	r = requests.get(base_url+last+limit)
	print("[+] Vulnerability count: "+limit)
	choice = input("[+] Do you want to print them all (y/n)? ").strip()
	if choice == 'y' or choice == 'Y':
		i = 0
		while i < len(r.json()):
			print(str(i+1)+". ")
			pprint(r.json()[i])
			i += 1
	return r.json()

# Returns the stats of the database
def dbInfo():
	dbInfo = "dbInfo"
	r = requests.get(base_url+dbInfo)
	pprint(r.json())
	return r.json()

parser = argparse.ArgumentParser()
parser.add_argument('--vendor', const=' ',nargs='?',type=str, help='Vendor name. If empty it returns the list of all vendors or it returns the product of a vendor')
parser.add_argument('--cpe22', type=str, help='CPE code which is to be converted to CPE 2.2')
parser.add_argument('--cpe23', type=str, help='CPE code which is to be converted to CPE 2.3')
parser.add_argument('--cveid', type=str, help='CVE Id. Get information for the CVE by using its Id')
parser.add_argument('--limit', const=' ', nargs='?', type=str, help='Limit. It returns the last n number of vulnerabilities. Default limit is 30')
parser.add_argument('--dbinfo', default=False, action="store_true",help='Returns the stats of the database')
parser.add_argument('--output', type=str, help='Save the results to a json file')
args = parser.parse_args()

output = 0
if args.output:
	output = 1
	filename = args.output

if args.vendor:
	if args.vendor == ' ':
		vendor = ''
	else:
		vendor = args.vendor
	data = browse(vendor)
	if output == 1 and data != "[-] Vendor not found":
		written = exists(filename)
		with open(filename,'a') as handle:
			if written:
				handle.write("\n\n")
			json_object = json.dumps(data, indent=4)
			handle.write(json_object)

if args.cpe22:
	data = cpe22(args.cpe22)
	if output == 1 and data != "[-] Not a valid CPE code":
		written = exists(filename)
		with open(filename,'a') as handle:
			if written:
				handle.write("\n\n")
			handle.write(data)

if args.cpe23:
	data = cpe23(args.cpe23)
	if output == 1 and data != "[-] Not a valid CPE code":
		written = exists(filename)
		with open(filename,'a') as handle:
			if written:
				handle.write("\n\n")
			handle.write(data)

if args.cveid:
	data = cve(args.cveid)
	if output == 1 and data != "[-] Not a valid CVE":
		written = exists(filename)
		with open(filename,'a') as handle:
			if written:
				handle.write("\n\n")
			handle.write("Information for "+args.cveid+": \n")
			json_object = json.dumps(data, indent=4)
			handle.write(json_object)

if args.limit:
	if args.limit == ' ':
		limit = ''
	else:
		limit = args.limit
	data = last(limit)
	written = exists(filename)
	with open(filename,'a') as handle:
		if written:
			handle.write("\n\n")
		json_object = json.dumps(data, indent=4)
		handle.write(json_object)

if args.dbInfo:
	data = dbInfo()
	written = exists(filename)
	with open(filename,'a') as handle:
		if written:
			handle.write("\n\n")
		handle.write("DB stats: \n")
		json_object = json.dumps(data, indent=4)
		handle.write(json_object)
