from cases import process
import os

def set_on():
    path = os.path.join(os.getcwd(), 'scripts', 'bluetooth.ps1')
    path = path + ' -BluetoothStatus On'
    return process.execpowershellprocess(path)

def set_off():
    path = os.path.join(os.getcwd(), 'scripts', 'bluetooth.ps1')
    path = path + ' -BluetoothStatus Off'
    return process.execpowershellprocess(path)
