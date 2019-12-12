'''
Created on Mar 30, 2018

@author: abelit
'''
class BaseDemo(object):
    def __init__(self, name, *args, **kwargs):
        pass


class Demo(BaseDemo):
    def __init__(self, func,  *args):
        BaseDemo.__init__(self, args)
        self.func = func
    
    def myprint(self):
        print('in class')
        print(self.func())
        
        

def demoprint():
    print('hello')
    
    return 'world'



if __name__ == '__main__':
    d = Demo(demoprint)
    c = Demo
    print(d)
    print(c)
    #d.myprint()