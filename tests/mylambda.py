'''
Created on Mar 8, 2018

@author: abelit
'''


def mysum(a,b):
    return a+b


def mytime(a,b):
    return a*b

def myminus(a,b):
    return a-b



a,b = 5,6

def mylambda(var,a,b):
    return {
            'mysum': lambda a,b : mysum(a,b),
            'mytime': lambda a,b : mytime(a,b),
            'myminus': lambda a,b : myminus(a,b), 
    }[var](a,b)
    
    
print(mylambda('mysum',5,6))


