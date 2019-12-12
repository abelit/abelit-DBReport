'''
Created on Mar 8, 2018

@author: abelit
'''


class MySetting:
    age = 20
    
    def get_age(self):
        return self.age


class MyDemo:
    
    def __init__(self, age, name={'first':'chen','last':'ying'}):
        name = name
        ms = MySetting()
        self.firstname = name['first']
        self.lastname = name['last']
        
        self.name = name
        self.age = age.get_age()
        
    def printDemo(self):
        global love
        
        love = 'love' + self.firstname
        print(self.age)
        
        

if __name__ == '__main__':
    
    age = MySetting()
    d = MyDemo(age)
    
    d.printDemo()
    
    print(love)