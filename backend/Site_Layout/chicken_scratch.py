class temp:

    def __init__(self,pizza,computer):
        print pizza
        print computer
        self.pizza=pizza

args={'computer':2}

temp(pizza=1,**args)