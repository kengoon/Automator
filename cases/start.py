from cases.execute import Execute
from datab.database import database
import time

class start:

    def __init__(self, **kwargs):
        
        if kwargs.get('coll_down_time'):
            self.coll_down = float(kwargs.get('coll_down_time'))
        else:
            self.coll_down = 5

        self.done = ''
        self.all = {}

        self.data = database().get_data()

        n = 0
        for i in self.data:
              
            self.action = self.data[i]['actions']

            self.automation = self.action['automation']

            self.action_to_do = self.action['action_to_do']

            self.all[n] = (self.automation, self.action_to_do)

        while True:
            for i in list(self.all.keys()):
                if i != self.done:
                    Execute(*self.all[i])
                    self.done = i
                else:
                    pass

            time.sleep(self.coll_down)
