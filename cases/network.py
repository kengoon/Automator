import time, os
from cases import process

def get_connected_ssid():
    ret = process.execpowershellprocess('(get-netconnectionProfile).Name')
    ret = ret.replace('\n', '')
    ret = ret.replace('\r', '')
    return ret

def connect(parms, ret=None):
    network = parms

    out = process.execshproc('netsh wlan show networks', array=True, sep='\n')
    for i in out:
        if network in i:
            os.system('netsh wlan disconnect')
            time.sleep(1)
            os.system('netsh wlan connect name={}'.format(network))
            return ret
    
    print('rete {} non trovata, esco.'.format(network))
    exit()

def main(is5gz):
 all = process.getallprocs()
 disconnect = False
 programs = ['EpicGamesLauncher.exe', 'Battle.net.exe', 'EAConnect_microsoft.exe', 'EADesktop.exe', 'chrome.exe']
 games = ['Fortnite.exe', 'ForzaHorizon4.exe']
 priority = ['GameBar.exe', 'Discord.exe']
 for i in all:
    for g in games:
        if g in i:
            if is5gz:
                if process.forpriority(priority, all):
                    connect('2gz')
            return False

 for i in all:
    for p in programs:
        if p in i:
            if is5gz != True:
                if process.forpriority(priority, all):
                    connect('5gz')
            return True
                       
    if i is all[-1]:
        disconnect = True
            
 if is5gz == True & disconnect == True:
    if process.forpriority(priority, all):
        connect('2gz')
    return False

'''def bootstrap():
        while True:
          if database.pause != False:  
            is5gz = main(False)
            time.sleep(10)
            while is5gz == True:
              if database.pause != False:
                is5gz = main(is5gz)
                time.sleep(10)
              else:
                time.sleep(10)
          else:
            time.sleep(10)'''