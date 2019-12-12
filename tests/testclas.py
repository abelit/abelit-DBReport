'''
Created on Mar 15, 2018

@author: abelit
'''


class Animal:
    def __init__(self,name,age):
        self.name = name
        self.age = age
        
    def do(self):
        print('Animal')
    
    def get_name(self):
        print(self.name)
        

class Cat(Animal):
    def __init__(self,action, **kwargs):
        Animal.__init__(self, **kwargs)
        self.action = action
    
    def get_age(self):
        print(self.age)
        
    def ido(self):
        print(self.action)
        
    if __name__ == '__main__':
        print(Cat)
        
        
if __name__ == '__main__':
    cat = Cat(action='i eat fish',name='huahua',age=12)
    
    cat.get_age()
    cat.ido()