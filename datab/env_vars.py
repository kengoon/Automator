DESIGN = '''#:kivy 2.0.0         
<Loading_Screen>:
    BoxLayout:
        orientation: 'vertical'
        id: container
        MDLabel:
            id: lbl
            text:'Loading'
            halign: 'center'

<Settings>:
    
    BoxLayout:
        orientation: "vertical"
        MDToolbar:
            title: "Impostazioni"
            left_action_items: [["menu", lambda x: app.callback(x)]]
        ScrollView:
            do_scroll_x: False
            do_scroll_y: True
            GridLayout:
                id: grid
                cols: 4
                padding: [10,10,10,10]
                row_default_height: 50
                MDLabel:
                    text: 'tema scuro'
                MDSwitch:
                    active:
                        app.active_switch()
                    on_active: app.change_theme_cls_theme_style()
                        
                
                MDLabel:
                    text: 'lang'
                MDTextButton:
                    text: 'chose'
                MDLabel:
                    text: 'prova'
                MDSwitch:
                MDLabel:
                    text: 'prova'
                MDSwitch:    
                MDLabel:
                    text: 'prova'
                MDSwitch:    
                MDLabel:
                    text: 'prova'
                MDSwitch:    
                MDLabel:
                    text: 'prova'
                MDSwitch:    
                
                MDLabel:
                    text: 'prova'
                
                MDSwitch:
                MDLabel:
                    text: 'prova'
                    
                MDSwitch:
'''

DATABASE = '''{
      "cards": {
            "default": {
                  "title": "Crea la tua prima automazione!",
                  "subtitle": "Guida alla creazione di automazioni",
                  "active": "True",
                  "added_propriety": {},
                  "actions": {
                        "automation": [
                              [
                                    "Startup"
                              ]
                        ],
                        "action_to_do": [
                              [
                                    "System",
                                    "send_notification",
                                    {
                                          "title": "prova",
                                          "msg": "prova notifica!"
                                    }
                              ]
                        ]
                  }
            }
      },
      "settings": {
            "theme_style": "Dark",
            "lang": "ita",
            "langs": {
                  "ita": {
                        "advises_shower.deactivate_adv": {
                              "title": "Attenzione!",
                              "text": "Se disattivata, l'automazione non verrà più eseguita! Potrai attivare nuovamente l'opzione in qualsiasi momento."
                        },
                        "advises_shower.deactivate_adv.button": [
                              "Continuare",
                              "Lasciare Attivo"
                        ],
                        "Errors.Json_Error": {
                              "title": "IMPOSSIBILE TROVARE IL FILE 'database.json'",
                              "text": "Il file 'database.json' è il file di configurazione del programma, senza esso non è possibile continuare. Vuoi scaricare ora una copia vuota del file?"
                        }
                  },
                  "engl": {
                        "advises_shower.deactivate_adv": {
                              "title": "Attention!",
                              "text": "If disabled, the automation will no longer run! You can re-activate the option at any time."
                        },
                        "advises_shower.deactivate_adv.button": [
                              "Continue",
                              "Stay active"
                        ],
                        "Errors.Json_Error": {
                              "title": "UNABLE TO FIND THE FILE 'database.json'",
                              "text": "The file 'database.json' is the configuration file, without that it's not possible to continue. Downolad now an empty copy of this file?"
                        }
                  }
            }
      }
}'''