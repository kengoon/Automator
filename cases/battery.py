import sys
import psutil

def get_battery_info():
    if sys.platform == 'linux':
        try:
            charge_state = open("/sys/class/power_supply/BAT1/status","r").readline().strip()
        except FileNotFoundError:
            try:
                charge_state = open("/sys/class/power_supply/BAT0/status","r").readline().strip()
            except FileNotFoundError:
                charge_state = None
        
        try:
            capacity = open("/sys/class/power_supply/BAT1/capacity","r").readline().strip()
        except FileNotFoundError:
            try:
                capacity = open("/sys/class/power_supply/BAT0/capacity","r").readline().strip()
            except FileNotFoundError:
                capacity = None
        
        return[capacity, charge_state]

    else:
        return [psutil.sensors_battery().percent, psutil.sensors_battery().power_plugged]