import json
def cache(func):
    def wrapper():
         func.__name__
         func()
    return wrapper
