from main import Advises_Shower

class Errors():
    
    class Json_Error():
        pass


class Advises():

    def Deactivate_Adv(self, *args):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton, MDFillRoundFlatButton
        #, text_color=UI.theme_cls.primary_color

        self.dialog = MDDialog(
                title='Attenzione',
                text='Attenzione!',
                buttons= [
                    MDFlatButton(
                        text="Continuare",
                        on_release=lambda *args: Advises_Shower().close_dialog(self.dialog, True,)),
                    MDFillRoundFlatButton(
                        text="Lasciare Attivo",
                        on_release=lambda *args: Advises_Shower().close_dialog(self.dialog, False,))],
                )
            
            
        Advises_Shower().open(self.dialog)