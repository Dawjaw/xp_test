import pprint
import json
from urllib.request import urlopen
import urllib
import time
from montydb import MontyClient
import backup


global SECRET
pp = pprint.PrettyPrinter()

with open('hypixel_secret.json') as json_file:
	data = json.load(json_file)
	SECRET = data['SECRET']


client = MontyClient("database")
db = client['xp_database']
collection = db['pet_xp_db']

profiles = ["b876ec32e396476ba1158438d83c67d4"]

# techno b876ec32e396476ba1158438d83c67d4


def send_url_command(profile):
	global SECRET
	url = f'https://api.hypixel.net/skyblock/profile?key={SECRET}&profile={profile}'
	url_command = url
	url_result = urlopen(url_command)
	raw_data = url_result.read()
	json_data = json.loads(raw_data)
	return json_data['profile']['members'][profile]


def main():

	current_i = 0
	xp_list = []
	while True:
		try:
			prof = profiles[0]
			if prof == "b876ec32e396476ba1158438d83c67d4":
				current_xp = 0
				current_time = time.time_ns()
				xp = send_url_command(prof)
				for i in range(0, len(xp['pets'])):
					if xp['pets'][i]['type'] == 'ELEPHANT':
						current_xp = xp['pets'][i]['exp']
				data_val = {'timestamp': current_time, 'xp': current_xp}
				print(round(current_xp))
				print(data_val)
				collection.insert_one(data_val)
				current_i+=1
				if current_i == 60:
					backup.main()
					current_i = 0
				time.sleep(60)
		except urllib.error.HTTPError:
			time.sleep(5)
			continue
		except ConnectionResetError:
			time.sleep(60)
			continue
		except urllib.error.URLError:
			time.sleep(60)
			continue

main()
