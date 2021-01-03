import pprint
import json
from urllib.request import urlopen
import urllib
import time
from montydb import MontyClient
import backup
import schedule
import threading


SECRET = ""
pp = pprint.PrettyPrinter()

with open('hypixel_secret.json') as json_file:
	data = json.load(json_file)
	SECRET = data['SECRET']


client = MontyClient("database")
db = client['xp_database']
collection = db['farming_xp']

profile = "b876ec32e396476ba1158438d83c67d4"
# techno b876ec32e396476ba1158438d83c67d4


def plot_graph():
	pass


def send_url_command(profile):
	global SECRET
	url = f'https://api.hypixel.net/skyblock/profile?key={SECRET}&profile={profile}'
	url_command = url
	url_result = urlopen(url_command)
	raw_data = url_result.read()
	json_data = json.loads(raw_data)
	return json_data['profile']['members'][profile]


def main():
	global profile
	while True:
		try:
			current_xp = 0
			current_time = time.time_ns()
			xp = send_url_command(profile)
			current_xp = xp['experience_skill_farming']
			data_val = {'timestamp': current_time, 'xp': current_xp}
			print(round(current_xp))
			print(data_val)
			collection.insert_one(data_val)
		except urllib.error.HTTPError as httper:
			print(httper)
			continue
		except ConnectionResetError as cre:
			print(cre)
			continue
		except urllib.error.URLError as urlerror:
			print(urlerror)   
			continue


schedule.every(60).seconds.do(run_threaded, main).tag('check_task', 'Main')
schedule.every(120).seconds.do(run_threaded, plot_graph).tag('check_task', 'plot')


while True:
    try:
        schedule.run_pending()
        time.sleep(0.1)
    except Exception:
	schedule.clear("check_task")
	sys.exit(0)
