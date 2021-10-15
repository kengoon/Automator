import sys, os, argparse, time, win32gui, win32con

parser = argparse.ArgumentParser(description='Set of options for Automator Program')

parser.add_argument('-d', action='store_true', dest='debug',help='set logger to Debaug mode')

args = parser.parse_args()

#Base Exception 
class PythonVersionNotSUpported(BaseException):
    pass

#Python Version
P_VERSION = '{}.{}'.format(sys.version_info.major, sys.version_info.minor)

if not (3.6 <= float(P_VERSION) and float(P_VERSION) <= 3.9):
    raise PythonVersionNotSUpported(
        'Python version {} not supported. (interpreter at {})'.format(P_VERSION, sys.executable)
        )

#Setting kivy no args
os.environ['KIVY_NO_ARGS'] = '1'
#essential app
from kivy.logger import Logger

if args.debug:
    Logger.setLevel('DEBUG')
from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.metrics import dp
from kivy.config import Config
from kivy.core.window import Window
from kivymd.uix.button import MDRaisedButton, MDTextButton
from exceptions import Errors

#kivy screens
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition, FadeTransition

#kivymd widget
from kivy.uix.dropdown import DropDown
from kivymd.uix.selectioncontrol import MDSwitch
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDToolbar
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog

#other components
from threading import Thread
from datab.database import database
from cases import start
import os, json, threading
from datab.env_vars import *

#Classe di widget già formattati
class pakedWidget():
    def switch(self, *args):
        sw = MDSwitch(*args)
        sw.id = 'sw'
        sw.pos_hint = {'center_x': .80, 'center_y': .3}
        return sw

    def card(self, *args):
        mc = MDCard(*args)
        mc.orientation = 'vertical'
        mc.padding = '8dp'
        mc.size_hint = None, None
        mc.size = "240dp", "280dp"
        mc.elevation = 10
        mc.border_radius = 20
        mc.radius = [15]
        return mc

    def scrollview(self, *args):
        sv = ScrollView(*args)
        sv.do_scroll_x = False
        sv.do_scroll_y = True
        return sv

    def gridlayout(self, *args):
        gl = GridLayout(*args)
        gl.size_hint_max_y = None
        gl.cols = 3
        gl.padding = "20dp"
        gl.spacing = "20dp"
        return gl

    def boxlayout(self, *args):
        bl = BoxLayout(*args)
        bl.orientation = 'vertical'
        return bl

    def toolbar(self, title, *args):
        tb = MDToolbar(*args)
        tb.title = title
        tb.left_action_items = [['menu', lambda x: UI.callback(UI, x)]]
        return tb

#Main class
class UI(MDApp):

    def build(self, *args):

        try:
            os.makedirs('tmp')
        except FileExistsError:
            pass

        r = open('tmp\\.runtime', 'w')
        r.write('{}')
        r.close()
        r = open('tmp\\.startup', 'w')
        r.close()

        Logger.info('[GL          ] Attivo on_request_close e on_resize')
        Window.bind(on_request_close=self.on_request_close)
        Window.bind(on_resize=self._on_resize)
        Window.bind(on_minimize=self.on_request_close)

        Logger.info('[GL          ] carico design.kv')
        Builder.load_string(DESIGN)

        Logger.info('[GL          ] creo UI.sm')
        UI.sm = ScreenManager(transition=FadeTransition())

        Logger.info('[GL          ] aggiungo titolo e imposto i colori')
        self.title = "Automator"
        self.theme_cls.theme_style = database().get_settings()['theme_style']
        self.theme_cls.primary_palette = "Blue"

        Logger.info('[GL          ] creo main screen')
        main_screen = Screen(name='main')
        main_screen.add_widget(widget=Screens.Main().build())

        '''Logger.info('[GL          ] creo settings screen')
        settings_screen = Screen(name='settings')
        settings_screen.add_widget(widget=Screens.Settings().build())'''

        Logger.info('[GL          ] creo create_screen')
        create_screen = Screen(name='create_screen')
        create_screen.add_widget(widget=Screens.Create_Screen().build())

        Logger.info('[GL          ] aggiungo tutti gli schermi a UI.sm')
        self.sm.add_widget(Screens.Loading_Screen(name='Loading_Screen'))
        self.sm.add_widget(main_screen)
        #self.sm.add_widget(settings_screen)
        self.sm.add_widget(Screens.Settings(name='settings'))
        self.sm.add_widget(create_screen)

        Logger.info('[GL          ] creo menu per create_screen')
        self.build_menu(0, True)

        Logger.info('[GL          ] mostro UI')

        threading.Timer(1, self.stop_loading).start()
        self.sm.current = 'Loading_Screen'

        Logger.info('[GL          ] imposto transizione')
        self.sm.transition = SlideTransition()

        os.remove('tmp\\.startup')

        return self.sm

    def stop_loading(self, *args):
        UI.sm.current= 'main'
    
    def active_switch(self, *args):
        try:
            if self.theme_style == 'Dark':
                return True
            else:
                return False
        except AttributeError:
            self.theme_style = self.theme_cls.theme_style
            
            if self.theme_style == 'Dark':
                return True
            else:
                return False
            
    def change_theme_cls_theme_style(self, *args):
        
        if self.theme_style == 'Light':
            self.theme_style = 'Dark'
            snack_text = 'tema scuro attivato'
        else:
            self.theme_style = 'Light'
            snack_text = 'tema scuro disattivato'

        self.send_snackbar(text=snack_text)

    def send_snackbar(self, **kwargs):
        self.snackbar = Snackbar(
        text=kwargs.get('text'),
        snackbar_x="10dp",
        snackbar_y="10dp",
        )
        self.snackbar.size_hint_x = (
            Window.width - (self.snackbar.snackbar_x * 2)
        ) / Window.width

        try:
            self.snackbar.buttons = kwargs.get('buttons')
            '''[
            MDFlatButton(
                text="UPDATE",
                text_color=(1, 1, 1, 1),
                on_release=snackbar.dismiss,
            ),
            MDFlatButton(
                text="CANCEL",
                text_color=(1, 1, 1, 1),
                on_release=snackbar.dismiss,
            ),
            ]'''
        except ValueError:
            self.snackbar.buttons = []

        try:
            self.snackbar.dismiss()
            self.snackbar.open()
        except AttributeError:
            self.snackbar.open()
    
    def on_request_close(self, *args):
        Window.close()
        try:
            os.remove('tmp\\.switch_acting')
        except FileNotFoundError:
            pass

        database().get_data()
        data = database.data
        database().save_data(data=dict(data))
        try:
            os.remove('tmp\\.runtime')
        except FileNotFoundError:
            pass
        try:
            os.removedirs('tmp')
        except FileNotFoundError:
            pass

    def callback(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_save(self, *args):
        database().set('theme_style', self.theme_style)
        self.theme_cls.theme_style = self.theme_style
        self.build_menu(*args)

    def not_save(self, *args):
        self.theme_cls.theme_style = self.theme_style_bakup
        self.build_menu(*args)

    def build_menu(self, *args):

        try:
            self.menu.dismiss()
        except AttributeError:
            pass

        menu_items = [
        #menu 0, main
        [
            {
                "viewclass": "OneLineListItem",
                "text": f"vai a Impostazioni",
                "height": dp(56),
                "on_release": lambda x=f"settings": self.build_menu(x, True),
            }
        ],
        #menu 1, settings
        [
            {
                "viewclass": "OneLineListItem",
                "text": f"Esci senza salvare",
                "height": dp(56),
                "on_release": lambda x=f"main": self.not_save(x, True),
             },
             {
                "viewclass": "OneLineListItem",
                "text": f"Salva ed esci",
                "height": dp(56),
                "on_release": lambda x=f"main": self.menu_save(x, True),
             }
        ],
        #menu 2, create_screen
        [
            {
                "viewclass": "OneLineListItem",
                "text": f"Esci senza salvare",
                "height": dp(56),
                "on_release": lambda x=f"main": self.not_save(x, True),
             },
             {
                "viewclass": "OneLineListItem",
                "text": f"Salva ed esci",
                "height": dp(56),
                "on_release": lambda: Screens.Create_Screen().confirm(),
             }
        ],
        ]

        if isinstance(args[0], str):
            screens = ['main','settings','create_screen']
            itm = screens.index(args[0])
        elif isinstance(args[0], int):
            itm = args[0]
        else:
            raise ValueError('Unricognizet type')        

        UI.menu = MDDropdownMenu(
            items=menu_items[itm],
            width_mult=4,
        )

        if args[1] != False:
          if isinstance(args[0], str):
            self.sm.current = args[0]
          elif isinstance(args[0], int):
            screens = ['main','setting', 'create_screen']
            self.sm.current = screens[args[0]]
          else:
            raise ValueError('Unricognized type')

        self.theme_style = self.theme_cls.theme_style
        self.theme_style_bakup = self.theme_style

        self.theme_cls.theme_style = database().get_settings()['theme_style']

        if self.sm.current == 'settings':
            self.theme_cls.theme_style = 'Dark'

        Logger.info('[GL          ] theme_style set on {}'.format(self.theme_cls.theme_style))

        return self.menu

    def build_cards(self):

        keys = database().get_value('keys')

        sv = pakedWidget().scrollview()
        cr = pakedWidget().card()
        gl = pakedWidget().gridlayout()

        if keys == None:

            lbl = MDLabel()
            lbl.text = '+'
            lbl.halign = 'center'
            lbl.font_style = 'H2'

            cr.bind(active=lambda *args:print('worked'))
            cr.add_widget(lbl)
            gl.add_widget(cr)
            sv.add_widget(gl)

            return sv
        else:
            data = database().get_data()
        
        for i in keys:
            sw = pakedWidget().switch()
            sw.id = i
            sw.bind(active=lambda *args: Errors.Advises().Deactivate_Adv(*args))

            if data[i]['active'] == 'True':  
                sw.active = True
            else:
                sw.active = False

            cr.add_widget(sw)    

            try:
                title = data[i]['title']
                subtitle = data[i]['subtitle']
            except KeyError:
                print('card must have title and a subtitle')
                exit(0)

            for v in data[i]['added_propriety']:
                try:
                    if v == 'text_color':
                        text_color = data[i][v]
                    elif v == 'text_style':
                        text_style = data[i][v]
                    elif v == 'bg_color':
                        bg_color = data[i][v]
                    else:
                        pass
                except KeyError or AttributeError:
                    pass

            lbl = MDLabel(text=title, font_style='H5')
            lbl.halign = 'center'
            lbl.valign = 'top'
            cr.add_widget(lbl)

            lbl = MDLabel(text=subtitle, text_size='10dp')
            lbl.halign = 'center'
            lbl.valign = 'center'
            
            cr.add_widget(lbl)
            
            gl.add_widget(cr)
            cr = pakedWidget().card()

        lbl = MDLabel()
        lbl.text = '+'
        lbl.halign = 'center'
        lbl.font_style = 'H2'

        cr.bind(on_release=lambda *args: UI().create_new(2, True))
        cr.add_widget(lbl)
        gl.add_widget(cr)
        sv.add_widget(gl)

        return sv

    def _on_resize(self, *args):
        Window.size = (800, 600)

    def eleve(self):
        if database().get_settings()['theme_style'] == 'Light':
            Window.raise_window()
        else:
            win32gui.MessageBox(0, 'Caanot Raise_window because dark theme is active', 'THEME ERROR', win32con.MB_OK)

class SecondaryWindow(MDApp):
    def build(self):
        return Builder.load_string('''
Label:
    text: 'prova'
        ''')

#Classe di schermi
class Screens:

    class Loading_Screen(Screen):
        pass

    class Main(Screen):

        def build(self):
            bx = pakedWidget().boxlayout()
            bx.add_widget(pakedWidget().toolbar('Automator'))
            sv = UI.build_cards(UI)
            bx.add_widget(sv)

            return bx        

    class Settings(Screen):
        
        def build(self):
            bx = pakedWidget().boxlayout()
            bx.add_widget(pakedWidget().toolbar('Impostazioni'))

            sv = pakedWidget().scrollview()
            gl = GridLayout(row_force_default=True, cols = 4, padding = [30,30,30,30], row_default_height =  100)

            lbl = MDLabel(text='tema scuro')
            gl.add_widget(lbl)
            switch = MDSwitch()
            switch.active = UI().active_switch()
            switch.bind(active=UI().change_theme_cls_theme_style)
            gl.add_widget(switch)

            lbl = MDLabel(text='language')
            gl.add_widget(lbl)
            drop = DropDown()
            ita = MDRaisedButton(text='ita', on_press=lambda *args: print('pressed ita'))
            drop.add_widget(ita)
            engl = MDRaisedButton(text='engl', on_press=lambda *args: print('pressed engl'))
            drop.add_widget(engl)
            main_button = MDTextButton(text='chose')
            main_button.bind(on_release=drop.open)
            gl.add_widget(main_button)

            for i in range(0,10):
                gl.add_widget(MDLabel(text='prova'))
                gl.add_widget(MDSwitch())

            sv.add_widget(gl)
            bx.add_widget(sv)

            return bx

    class Create_Screen(Screen):

        def build(self):
            from kivymd.uix.textfield import MDTextField
            from kivymd.uix.expansionpanel import MDExpansionPanelLabel

            bx = pakedWidget().boxlayout()
            tb = pakedWidget().toolbar('Create New Automation')
            bx.add_widget(tb)
            sv = pakedWidget().scrollview()
            gl = pakedWidget().gridlayout()

            TitleBox = MDTextField(hint_text='Titolo', required=True, mode='fill', helper_text_mode='on_error', helper_text= "Il campo è obbligatorio")
            DescriptionBox = MDTextField(mode='fill', hint_text= "Descrizione (opzionale)")

            gl.add_widget(TitleBox)
            gl.add_widget(DescriptionBox)
            sv.add_widget(gl)
            bx.add_widget(sv)

            return bx

        def confirm(self, *args):
            import uuid
            
            data = {'card {}'.format(uuid.uuid4()):
                    {'title':self.ids['title'].text,
                    'subtitle': self.ids['subtitle'].text,
                    'active': True,
                    "actions": {
                        "automation": [],
                        "action_to_do": []
                        }
                    }
                   }

            print(data)
            #print(database().get_data())
            
            #self.ids['title'].text

            UI().build_menu('main', True)

class StopApplication(BaseException):
    pass

#Classe adibita al mostrare avvisi
class Advises_Shower():
    done = False
    
    def file_not_fount(self):
        pass

    def critical_error(self):
        pass

    def systemerror(self):
        pass

    def json_error(self):
        from kivymd.uix.button import MDFlatButton
        #, text_color=UI.theme_cls.primary_color
        buttons = [
                    MDFlatButton(
                        text="EXIT"
                    ),
                    MDFlatButton(
                        text="REPAIR")
                ]
        try:
            self.dialog = MDDialog(
                    text='Errore',
                    buttons=buttons,
                )
            self.dialog.open()
        except AttributeError:
            pass

    def open(self, _dialog_build):
        try:
            if not os.path.isfile('tmp\\.startup'):
                self._dialog = _dialog_build
                self._dialog.open()
        except AttributeError:
            pass
        
    def close_dialog(self, dialog,  sw, _continue, _on_request=False):

        tmp = open('tmp\\.switch_acting', 'w')
        tmp.close()

        self._dialog = dialog
        self.sw = sw
        
        if _on_request != True:
            try:
                self._dialog.dismiss()
            except AttributeError:
                pass

            if _continue == True:
                Errors.Advises().Deactivate_Adv(self.sw, deactivate=True)
                self.close_tmp()
                self.done = True
                
            else:
                self.sw.active = True
                self.done = True
        
        else:
            if self.done != True:
                self.sw.active = True

        self.close_tmp()

    def close_tmp(self):
        try:
            os.remove('tmp\\.switch_acting')
        except FileNotFoundError:
            pass
        
        try:
            id = self.sw.id
            active = self.sw.active

            r = open('tmp\\.runtime', 'r')
            js = json.loads(r.read())
            r.close()

            js[id] = active

            js = json.dumps(js, ensure_ascii=True)

            r = open('tmp\\.runtime', 'w')
            r.write(js)
            r.close()
        except AttributeError:
            pass

        self.done = False

from infi.systray import SysTrayIcon
is_t_alive = True
class SysTray(SysTrayIcon):

    def t_on_quit(self, *args):
        os._exit(0)

    def __init__(self, icon='logo.ico', hover_text='Automator', menu_options=None, on_quit=t_on_quit, default_menu_index=None, window_class_name=None):      
        super().__init__(icon, hover_text, menu_options=menu_options, on_quit=on_quit, default_menu_index=default_menu_index, window_class_name=window_class_name)

    def run(self):
        self._message_loop_thread = Thread(target=self._message_loop_func, daemon=True)
        self._message_loop_thread.start()

def resume_window(*args):
    '''if os.path.isfile('tmp\\.runtime'):
        UI().eleve()
    else:
        win32gui.MessageBox(0, 'This function will be implemented soon', 'INFO', win32con.MB_OK)'''

    #such as kivi.core.window.windowbase suggest
    import kivy.core.gl

    Window.create_window()
    Window.register()
    Window.configure_keyboards()

    SecondaryWindow().run()


#metodo di boot              
def bootstrap():

    menu_options = (("Open Automator", None, resume_window),)
    systray = SysTray("logo.ico", "Automator", menu_options)
    systray.run()

    if os.path.isfile('tmp\\.runtime') or os.path.isfile('tmp\\.switch_acting'):
        try:
            os.remove('tmp\\.runtime')
        except FileNotFoundError:
            pass

        try:
            os.remove('tmp\\.switch_acting')
        except FileNotFoundError:
            pass

    import kivy
    
    kivy.require('2.0.0')
    Config.set('kivy', 'keyboard_mode', 'systemandmulti')

    if sys.platform == 'linux':
        PLATFORM = 'linux'
        BATTERY_INFO = '/sys/class/power_supply/BAT0'
    else:
        PLATFORM = 'win32'

    database(PLATFORM)
    th = Thread(target=start.start)
    th.setDaemon(True)
    th.start()
    UI().run()

#Entry point
if __name__ =='__main__':
    PLATFORM = None
    try:
        bootstrap()

        database().send_notification('Automator', 'il programma è ancora in esecuzione')

        try:
            while is_t_alive != False:
                time.sleep(15)
        except StopApplication:
            sys.exit(1)

    except (KeyboardInterrupt):
        Logger.warning('Keyboard interrupt detected, abort')

        try:
            os.remove(os.path.join(os.path.dirname(__file__), 'tmp', '.runtime'))
        except FileNotFoundError:
            pass

        try:
            os.removedirs(os.path.join(os.getcwd(), 'tmp'))
        except FileNotFoundError:
            pass

    except ChildProcessError as e:
        Logger.warning(e)