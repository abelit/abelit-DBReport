'''
Created on Mar 14, 2018

@author: abelit
'''

class Animal:
    def __init__(self, action):
        self.action = action
        
    def run(self):
        print('I can go!')

class Cat(Animal):
    def __init__(self,name):
        self.name = name
        self.action = ''
        
    def cat_print(self):
        self.run()
        print(self.name)

class Demo:
    def __init__(self,file,func):
        self.file = file
        self.func = func
        
    
    def demo_print(self):
        print(self.file)
        
    def run(self):
        self.func
        
def hell0_fun():
    print('hello function')
    
    
if __name__ == '__main__':
    cat = Cat('I am a cat!')
    demo = Demo('./hehe.json',cat.cat_print())
    
    demo.run()