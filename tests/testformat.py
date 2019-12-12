'''
Created on Mar 15, 2018

@author: abelit
'''

import os

print("hello {0}".format("baby"))

print(os.path.basename(__file__))


print('%(asctime)s - %({0})s - %(levelname)s - %(message)s'.format('hello'))