from p1 import Human
class man(Human):
    def __init__(self,name,sex = 'man'):
        
        super(man,self).__init__(name,sex)
        # Human.__init__(self,name,sex)

roy = man('roy','man')
sophia = man('sophia','woman')
roy.dead()