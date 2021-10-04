import os

class Execute():
    
    def __init__(self, actions: list, action_to_do: list) -> None:
        self.actions = actions
        Execute.do = action_to_do

        automatism = ['Battery', 'Network', 'Process', 'Startup', 'System']

        n = 0
        while n != len(self.actions):
            
            for i in self.actions[n]:
                if i == automatism[0]:
                    self.Battery().load(self.actions[n])
                elif i == automatism[1]:
                    self.Network().load(self.actions[n])
                elif i == automatism[2]:
                    self.Process().load(self.actions[n])
                elif i == automatism[3]:
                    Attuator(Execute.do)
                elif i == automatism[4]:
                    self.System().load(self.actions[n])

            n+=1

    class Battery():
        batter = ['level', 'plugged', 'not_plugged']

        def load(self, action: list):
            for i in Execute.Battery.batter:
                if action[1] == i:
                    if i == Execute.Battery.batter[0]:
                        self.lvl = action[2]
                        self.level()
                    elif i == Execute.Battery.batter[1]:
                        self.plugged = True
                        self.plug()
                    elif i == Execute.Battery.batter[2]:
                        self.plugged = False
                        self.plug()

        def level(self):
            from cases.battery import get_battery_info

            if int(get_battery_info()[0]) == int(self.lvl):
                Attuator(Execute.do)

        def plug(self):
            from cases.battery import get_battery_info
            if get_battery_info()[1] == self.plugged:
                Attuator(Execute.do)
            else:
                return False

    class Network():
        net = ['is_connected']
        def load(self, action: list):
            for i in Execute.Network.net:
                if action[1] == i:
                    if i == Execute.Network.net[0]:
                        self.ssid = action[2]
                        self.is_connect()

        def is_connect(self):
            from cases import network
        
            net = network.get_connected_ssid()

            if str(net) == str(self.ssid):
                print('stessa rete')
        

    class Process():
        proc = ['is_running']

        def load(self, action: list):

            for i in Execute.Process.proc:
                if action[1] == i:
                    if i == Execute.Process.proc[0]:
                        method = ['pid', 'name']
                        if action[2] == method[0]:
                            self.pid = action[3]
                            self.is_running()
                        else:
                            self.name = action[3]
                            self.is_running()


        def is_running(self):
            from cases import process
            try:
                for i in process.getallprocs():
                    if self.pid in i:
                        print('processo con pid {} trovato'.format(self.pid))
            except AttributeError:
                if '.exe' in self.name:
                    for i in process.getallprocs():
                        if self.name in i:
                            print('processo {} trovato'.format(self.name))


    class System():
        _sys = ['idle_timeout']

        def load(self, action: list):
            from cases.system import System
            for i in self._sys:
                if action[1] == i:
                    System().idle_timeout(action, Execute.do)



class Attuator():
    def __init__(self, attuator: list)-> None:
        self.attuator = attuator

        attuatori = ['Network', 'Bluetooth', 'Process', 'System']

        for i in self.attuator:
          n = 0
          while n != len(self.attuator):
            
            for i in self.attuator[n]:
                if i == attuatori[0]:
                    self.Network().load(self.attuator[n])
                elif i == attuatori[1]:
                    self.Bluetooth().load(self.attuator[n])
                elif i == attuatori[2]:
                    self.Process().load(self.attuator[n])
                elif i == attuatori[3]:
                    self.System().load(self.attuator[n])

            n+=1

    class Network():
        def load(self, attuators: list):

            self.attuators = attuators
            
            net = ['connect', 'disconnect', 'send_email']

            for i in net:
                if attuators[1] == i:
                    if i == 'connect':
                        import network
                        network.connect(attuators[2])
                    if i == 'disconnect':
                        from os import system
                        system('netsh wlan disconnect')
                    if i == 'send_email':
                        self.send_email()

        def send_email(self):
            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.application import MIMEApplication

            if isinstance(self.attuators[2], dict):
                self.data = self.attuators[2]

                msg = MIMEMultipart()
                msg['Subject'] = self.data['Subject']
                msgText = MIMEText('<b>%s</b>' % (msg['Subject']), 'html')
                msg.attach(msgText)

                try:
                    data = MIMEApplication(open(self.data['added_file']).read())
                    data.add_header('Content-Disposition', 'attachment', filename=self.data['added_file'])
                    msg.attach(data)
                except KeyError:
                    pass


                smtps = {'gmail': ['smtp.gmail.com', 587], 'outlook': ['smtp.live.com',587], 'office365': ['smtp.office365.com',587], 'yahoo mail': ['smtp.mail.yahoo.com',465], 'hotmail': ['smtp.live.com',465]}
                for i in list(smtps.keys()):
                  if i in self.data['user']:  
                    smtp, port = smtps[i]

                with smtplib.SMTP(smtp, port) as smtpObj:
                        smtpObj.ehlo()
                        smtpObj.starttls()
                        smtpObj.login(self.data['user'], self.data['password'])
                        smtpObj.sendmail(self.data['user'], self.data['dest'], msg.as_string())
                        smtpObj.quit()


    class Bluetooth():
        def load(self, attuators: list):
            from cases import bluetooth
            bt = ['switch_on', 'switch_off']

            self.attuators = attuators

            for i in bt:
                if i in self.attuators[1]:
                    if i == bt[0]:
                        print(bluetooth.set_on())
                    else:
                        bluetooth.set_off()


    class Process():
        def load(self, attuators: list):
            proc = ['start', 'kill']

            self.attuators = attuators

            for i in proc:
                if i in attuators[1]:
                    if i == proc[0]:
                        self.start()
                    else:
                        self.kill()

        def start(self):
            os.startfile(self.attuators[2])
        
        def kill(self):
            from cases import process
            import psutil
            if self.attuators[2] == 'pid':
                psutil.Process(self.attuators[3]).kill()
            else:
                try:
                    process.execpowershellprocess('taskkill /IM '+self.attuators[3]+' /F')
                except UnicodeDecodeError:
                    pass

    class System():
        def load(self, attuators: list):
            from cases import process
            index = ['reboot', 'look', 'shotdown', 'logoff', 'personal_cmd', 'take_screenshot', 'send_notification']
            cmds = {'reboot': {'win32':'Restart-Computer', 'linux':'shutdown -r 0'}, 'look': {'win32':'rundll32.exe user32.dll,LockWorkStation', 'linux':'gnome-screensaver\ngnome-screensaver-command -l'}, 'logoff': {'win32':'shutdown.exe -l', 'linux':'logout'}, 'shotdown':{'win32':'Stop-Computer', 'linux':'shutdown -h 0'}}

            self.attuators = attuators

            for i in index:
                if i in attuators[1]:
                    if i == index[-2]:
                        import pyscreenshot as ImageGrab
                        im = ImageGrab.grab()
                        im.save(self.attuators[2])

                    elif i == index[-1]:
                        from datab.database import database                    
                        database().send_notification(self.attuators[2]['title'], self.attuators[2]['msg'])

                    else:
                        if self.force():
                            cmd = cmds[i] + ' -Force'
                            process.execpowershellprocess(cmd)
                        else:
                            process.execpowershellprocess(cmds[i])

        
        def force(self):
          try:  
            if self.attuators[2] == 'force':
                return True
            else:
                return False
          except IndexError:
              return False


mail_corpus = {
    'Subject':'prova',
    'msg':'prova', 
    'user':'davide.bera2021@gmail.com',
    'password':'dedegmail2',
    'dest':'davide.bera2021@gmail.com'
    }

#Execute([['Startup']], [['Network', 'send_email', mail_corpus]])

#, ['Network', 'is_connected', 'Vodafone-A38728582'], ['Process', 'is_running', 'name', 'Taskmgr.exe'], 