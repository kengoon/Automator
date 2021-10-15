from __future__ import absolute_import, print_function, unicode_literals

# standard library
import logging, threading, os, json, uuid
from time import sleep
from pkg_resources import Requirement, resource_filename

from datab.env_vars import DATABASE

class database():
    keys = {}
    returnv = False
    pause = False
    dynamic_key_stop = False
    PATH = 'datab\\database.json' 

    if not os.path.isdir('datab'):
        os.makedirs('datab')
        with open(PATH, 'w', encoding='utf-8') as f:
            f.write(DATABASE)
            f.close()
    
    def __init__(self, platform=None): 
        if platform == None:
            try:
                database.PLATFORM
                database.PATH
            except AttributeError:
                raise ChildProcessError('Variabile PLATFORM not found')
      
        else:
            database.PLATFORM = platform
            database.PATH = 'datab\\database.json' 
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
        base_path = 'datab\\graphic'
        if self.PLATFORM == 'linux':
            logo = os.path.join(base_path, 'Kivy_logo.png')
            os.system('notify-send -i "{}" "{}" "{}"'.format(logo, title, msg))
        else:
            logo = os.path.join(base_path, 'Kivy_logo.ico')
            Notifier().show_toast(title, msg, icon_path=logo, threaded=True)
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
        
    def get_langauge(self):
        return self.get_settings()['langs'][self.get_settings()['lang']]  
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
            json.dump(kwargs.get('data'), f, indent=6, ensure_ascii=False)
            f.close()
        
        try:
            if kwargs.get('close') != True:
                database().__init__(self.PLATFORM)
        except ValueError:
            pass

#class for send notify on win 10
from win32api import GetModuleHandle, PostQuitMessage
from win32con import CW_USEDEFAULT, IDI_APPLICATION, IMAGE_ICON, LR_DEFAULTSIZE, LR_LOADFROMFILE, WM_DESTROY, WM_USER, WS_OVERLAPPED, WS_SYSMENU
from win32gui import *

class Notifier(object):
    """
    code from win10toast
    """

    def __init__(self):
        self._thread = None

    def _show_toast(self, title, msg,
                    icon_path, duration):

        message_map = {WM_DESTROY: self.on_destroy, }

        # Register the window class.
        self.wc = WNDCLASS()
        self.hinst = self.wc.hInstance = GetModuleHandle(None)
        self.wc.lpszClassName = str(f"PythonTaskbar {uuid.uuid4()}")  # must be a string
        self.wc.lpfnWndProc = message_map  # could also specify a wndproc.
        try:
            self.classAtom = RegisterClass(self.wc)
        except Exception as e:
            print(e)

        style = WS_OVERLAPPED | WS_SYSMENU
        self.hwnd = CreateWindow(self.classAtom, "Taskbar", style,
                                 0, 0, CW_USEDEFAULT,
                                 CW_USEDEFAULT,
                                 0, 0, self.hinst, None)
        UpdateWindow(self.hwnd)

        # icon
        if icon_path is not None:
            icon_path = os.path.realpath(icon_path)
        else:
            icon_path =  resource_filename(Requirement.parse("win10toast"), "win10toast/data/python.ico")
        icon_flags = LR_LOADFROMFILE | LR_DEFAULTSIZE
        try:
            hicon = LoadImage(self.hinst, icon_path,
                              IMAGE_ICON, 0, 0, icon_flags)
        except Exception as e:
            logging.error("Some trouble with the icon ({}): {}"
                          .format(icon_path, e))
            hicon = LoadIcon(0, IDI_APPLICATION)

        # Taskbar icon
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd, 0, flags, WM_USER + 20, hicon, "Automator")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, (self.hwnd, 0, NIF_INFO,
                                      WM_USER + 20,
                                      hicon, "Balloon Tooltip", msg, 200,
                                      title))

        sleep(duration)
        DestroyWindow(self.hwnd)
        UnregisterClass(self.wc.lpszClassName, None)
        return None

    def show_toast(self, title="Notification", msg="Here comes the message",
                    icon_path=None, duration=5, threaded=False):

        if not threaded:
            self._show_toast(title, msg, icon_path, duration)
        else:
            if self.notification_active():
                # We have an active notification, let is finish so we don't spam them
                return False

            self._thread = threading.Thread(target=self._show_toast, args=(title, msg, icon_path, duration))
            self._thread.start()
        return True

    def notification_active(self):
        """See if we have an active notification showing"""
        if self._thread != None and self._thread.is_alive():
            # We have an active notification, let is finish we don't spam them
            return True
        return False

    def on_destroy(self, hwnd, msg, wparam, lparam):
        """Clean after notification ended.

        :hwnd:
        :msg:
        :wparam:
        :lparam:
        """
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0)

        return None
