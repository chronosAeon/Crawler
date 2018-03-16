# '''
# '''
# __all__ = ['a','b']
# a = 0
# b = 1
# c = 2
class Human():
    sum = 0
    def __init__(self,name,sex):
        self.__name = name
        self.__sex = sex
        Human.sum+=1
        print(Human.sum)
    def dead(self):
        Human.sum-=1
        print(Human.sum)
    