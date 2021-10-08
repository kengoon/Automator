import time, os, sys
from cases.process import *

def get_connected_ssid():
    if sys.platform == 'linux':
        ret = execshproc('/sbin/iwconfig wlan0 | grep ESSID')
        print(ret)
    else:
        ret = execpowershellprocess('(get-netconnectionProfile).Name')
        ret = ret.replace('\n', '')
        ret = ret.replace('\r', '')
        return ret

def connect(parms, ret=None):
    network = parms

    out = execshproc('netsh wlan show networks', array=True, sep='\n')
    for i in out:
        if network in i:
            os.system('netsh wlan disconnect')
            time.sleep(1)
            os.system('netsh wlan connect name={}'.format(network))
            return ret
    
    print('rete {} non trovata, esco.'.format(network))
    exit()

def main(is5gz):
 all = getallprocs()
 disconnect = False
 programs = ['EpicGamesLauncher.exe', 'Battle.net.exe', 'EAConnect_microsoft.exe', 'EADesktop.exe', 'chrome.exe']
 games = ['Fortnite.exe', 'ForzaHorizon4.exe']
 priority = ['GameBar.exe', 'Discord.exe']
 for i in all:
    for g in games:
        if g in i:
            if is5gz:
                if forpriority(priority, all):
                    connect('2gz')
            return False

 for i in all:
    for p in programs:
        if p in i:
            if is5gz != True:
                if forpriority(priority, all):
                    connect('5gz')
            return True
                       
    if i is all[-1]:
        disconnect = True
            
 if is5gz == True & disconnect == True:
    if forpriority(priority, all):
        connect('2gz')
    return False

if __name__ == '__main__':
    get_connected_ssid()