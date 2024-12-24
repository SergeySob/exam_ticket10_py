
import json
import pickle
import requests
import datetime

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

bld = Gtk.Builder()
bld.add_from_file('ui.glade')

wnd = bld.get_object('wnd')

token = 'dd3858fc9dd84660ac553814240912'

history = []

mdl = bld.get_object('mdl')
txt_city = bld.get_object('txt_city')
lab_t = bld.get_object('lab_t')
lab_h = bld.get_object('lab_h')
lab_p = bld.get_object('lab_p')

def perform_query(wgt):
	location = txt_city.get_text()
	response = requests.get(f'https://api.weatherapi.com/v1/current.json?key={token}&q={location}')
	result = json.loads(response.content)

	now = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')

	weather = dict()
	weather['now'] = now
	weather['location'] = location
	weather['temp_c'] = result['current']['temp_c']
	weather['humidity'] = result['current']['humidity']
	weather['pressure_mb'] = result['current']['pressure_mb']
	history.append(weather)

	lab_t.set_text(str(weather['temp_c']))
	lab_h.set_text(str(weather['humidity']))
	lab_p.set_text(str(weather['pressure_mb'] * 3 / 4))

	itr = mdl.append()
	mdl[itr] = [ now, location ]

def exit_app(wgt):
	f = open('history.pkl', 'wb')
	pickle.dump(history, f)
	f.close()
	Gtk.main_quit()

tab = {
	'on_btn_query_clicked': perform_query,
	'on_wnd_destroy': exit_app
}
bld.connect_signals(tab)

try:
	f = open('history.pkl', 'rb')
	history = pickle.load(f)
	f.close()

except:
	pass

for item in history:
	itr = mdl.append()
	mdl[itr] = [ item['now'], item['location'] ]

wnd.show_all()

Gtk.main()