import csv

'''
    use class decorator to pass function as input, run through things.
'''

class tsp(object):
    def __init__(self, func):
        # specific file to read
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
        