import logging, os, json

class database():
    keys = {}
    returnv = False
    pause = False
    dynamic_key_stop = False
    data = {}
    PATH = None
    
    def __init__(self, platform=None): 

        if platform == None:
            try:
                database.PLATFORM
                database.PATH
            except AttributeError:
                raise ChildProcessError('Variabile PLATFORM not found')
      
        else:
            database.PLATFORM = platform
            database.PATH = os.path.join(os.getcwd(), 'datab','database.json')

        if not 'data' in os.getcwd():
            os.chdir(os.path.join(os.getcwd(), 'data'))  

        logging.basicConfig(format='[%(levelname)-8s] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)
        if os.path.isfile(self.PATH):
            with open(self.PATH) as f:
                js = json.load(f)
                database.data = js
        
            f.close()
        else:

          pass
          
    
    def send_notification(self, title, msg):
        if self.PLATFORM == 'linux':
            base_path = os.path.dirname(__file__)
            logo = os.path.join(base_path, 'Kivy_logo.png')
            os.system('notify-send -i "{}" "{}" "{}"'.format(logo, title, msg))
        else:
            from win10toast import ToastNotifier   
            ToastNotifier().show_toast(title, msg, threaded=True)

    def get_value(self, value):
        with open(self.PATH,'r') as f:
            js = json.load(f)
            f.close()

            if value == 'keys':
                try: 
                    return list(js['cards'].keys())
                except AttributeError or ValueError or KeyError:
                    return None

            try:
                return js[value]
            except AttributeError or ValueError or KeyError:
                return None
        

    def baseconfig():
        data = {'cards':{},'settings':{}}
        return data       

    def reset(value='') -> str:
        if value == 'keys':
            database.keys = {}
        elif value == 'returnv':
            database.returnv = False
        elif value == 'pause':
            database.pause = False
        elif value == 'dynamic_stop':
            database.dynamic_key_stop = False
        elif value == '':
            database.returnv = False
            database.pause = False
            database.keys = {}
            database.dynamic_key_stop = False

    def get_data(self) -> dict:
        if self.data == {}:
            if os.path.isfile(self.PATH):
                with open(self.PATH,'r') as f:
                    js = json.load(f)
                    database.data = js
                    f.close()
                    return js['cards']
        else:
            return database.data['cards']
    
    def set(self, key, value):
        if database.data == {}:
            database().get_data()
        set = database.data
        set['settings'][key] = value
        database().save_data(data=set)

    def get_settings(self):
        if database.data == {}:
            database().get_data()
        return database.data['settings']

    def save_data(self, **kwargs):
        with open(self.PATH, 'w') as f:
            json.dump(kwargs.get('data'), f, indent=6)
            f.close()
        
        try:
            if kwargs.get('close') != True:
                database().__init__(self.PLATFORM)
        except ValueError:
            pass

class logger():
    def info(msg):
            if msg == 'inizio main loop':
                print(msg)
            else:    
                pass
    def warning(msg):
            pass
    def debug(msg):
            pass
    def critical(msg):
            pass