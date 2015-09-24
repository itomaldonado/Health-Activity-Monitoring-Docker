import pyowm
import sys

owm = pyowm.OWM('80c233e546bdab004385a95fd8f98eee')

def get_newname(name):
	return name.replace(":", " ")



if __name__ == '__main__':


	name = sys.argv[1]
	newname = get_newname(name)
	print newname

	
	observation = owm.weather_at_place(newname)
	w = observation.get_weather()
	
	winfo = []
	winfo.append(newname)
	winfo.append(w.get_temperature(unit='fahrenheit')['temp'])
	winfo.append(w.get_status())
	winfo.append(w.get_wind()['speed'])
	winfo.append(w.get_humidity())
	winfo.append(w.get_pressure()['press'])
	
	print(winfo[1])
	print(winfo[2])
	print(winfo[3])
	print(winfo[4])
	print(winfo[5])
