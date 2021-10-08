import os, json
from main import Advises_Shower
from datab.database import database

class Errors():
    
    def Json_Error(self):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton

        lang = database().get_langauge()['Errors.Json_Error']

        self.dialog = MDDialog(
            title=lang['title'].encode('latin1').decode('utf-8'),
            text=lang['text'].encode('latin1').decode('utf-8'),
            buttons=[

            ]
        )


class Advises():

    def Deactivate_Adv(self, sw, sw_status=None, deactivate=False):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
        #, text_color=UI.theme_cls.primary_color

        switch = sw
        self.not_activate = False

        r = open(os.path.join(os.getcwd(), 'tmp', '.runtime'), 'r')
        js = json.loads(r.read())
        r.close()

        try:
            if js[switch.id] == False:
                js[switch.id] = True

                js = json.dumps(js)

                r = open(os.path.join(os.getcwd(), 'tmp', '.runtime'), 'w')
                r.write(js)
                r.close()
                return None
        except KeyError:
            pass


        if deactivate == True:
                switch.active = False
                self.not_activate = True

        else:
            if self.not_activate == False:

                text = database().get_langauge()['advises_shower.deactivate_adv.button']
                try:
                    hint_title = database().get_langauge()['advises_shower.deactivate_adv']['title'].encode('latin1').decode('utf-8')
                except UnicodeError:
                    hint_title = database().get_langauge()['advises_shower.deactivate_adv']['title']
                
                try:
                    hint_text = database().get_langauge()['advises_shower.deactivate_adv']['text'].encode('latin1').decode('utf-8')
                except UnicodeError:
                    hint_text = database().get_langauge()['advises_shower.deactivate_adv']['text']

                self.dialog = MDDialog(
                        title= hint_title,
                        text= hint_text,
                        buttons= [
                            MDFlatButton(
                                text=text[0],
                                on_release=lambda *args: Advises_Shower().close_dialog(self.dialog, switch, True,)),
                            MDFillRoundFlatButton(
                                text=text[1],
                                on_release=lambda *args: Advises_Shower().close_dialog(self.dialog, switch, False,))],
                        )

                self.dialog.bind(on_dismiss= lambda *args: Advises_Shower().close_dialog(dialog=self.dialog, sw=switch, _continue=False, _on_request=True))
                    
                if not os.path.isfile(os.path.join(os.getcwd(), 'tmp', '.switch_acting')):
                    Advises_Shower().open(self.dialog)
            else:
                self.not_activate = False