#import sys
#
## sys.path tells where Python will be looking at for modules
#print(sys.path)
## sys.moduels to see all the modules imported
#print(sys.modules)

#from .lib import xx # relative import - not applicable to the main file
#from ..lib import xx # access the parent folder to look for functions/modules

### Errors
#class TooManyPagesError(ValueError):
#    pass
#
#class Book:
#    def __init__(self, name: str, page_count: int):
#        self.name = name
#        self.page_count = page_count
#        self.pages_read = 0
#    
#    def __repr__(self):
#        return (
#            f'<Book {self.name}, read {self.pages_read} pages out of {self.page_count}'
#        )
#    
#    def read(self, pages: int):
#        if self.pages_read + pages > self.page_count:
#            raise TooManyPagesError(
#                f'You tried to read {self.pages_read + pages} pages, but this book only has {self.page_count} pages.'
#            )
#        self.pages_read += pages
#        print(f'You have now read {self.pages_read} pages out of {self.page_count}.')
#
#python101 = Book('Python 101', 50)
#
#try:
#    python101.read(35)
#    python101.read(50)
#except TooManyPagesError as e:
#    print(e)



### First class functions
#def divide(dividend, divisor):
#    if divisor == 0:
#        raise ZeroDivisionError('Divisor cannot be 0.')
#    
#    return dividend / divisor
#
#def calculate(*values, operator):
#    return operator(*values)
#
#result = calculate(20, 4, operator=divide)
#
#print(result)
#
#
#def search(sequence, expected, finder):
#    for elem in sequence:
#        if finder(elem) == expected:
#            return elem
#    raise RuntimeError(f'Could not find an element with {expected}.')
#
#friends = [
#    {'name': 'Rolf Smith', 'age': 24},
#    {'name': 'Adam Wool', 'age': 30},
#    {'name': 'Anne Pun', 'age': 27},
#]
#
#def get_friend_name(friend):
#    return friend['name']
#
#from operator import itemgetter # seems quite the same as dict.get()
#
#print(search(friends, 'Rolf Smith', get_friend_name))
#print(search(friends, 'Rolf Smith', lambda friend: friend['name']))
#print(search(friends, 'Rolf Smith', itemgetter('name')))



### Simple Decorator
#user = {'username': 'jose', 'access_level': 'guest'}
#
#def get_admin_password():
#    return '1234'
#
#def make_secure(func):
#    def secure_function():
#        if user['access_level'] == 'admin':
#            return func()
#        else:
#            return f'No admin permissions for {user["username"]}.'
#    
#    return secure_function
#
#get_admin_password = make_secure(get_admin_password)
#print(get_admin_password())
#user = {'username': 'jose', 'access_level': 'admin'}
#print(get_admin_password())


### @ at syntax for decorator
#import functools
#
#user = {'username': 'jose', 'access_level': 'guest'}
#
#def make_secure(func):
#    # Wraps a function with another function
#    @functools.wraps(func)
#    def secure_function():
#        if user['access_level'] == 'admin':
#            return func()
#        else:
#            return f'No admin permissions for {user["username"]}.'
#    
#    return secure_function
#
#@make_secure
#def get_admin_password():
#    return '1234'
#
## Without wraps, it returns secure_function
## With wraps, it returns get_admin_password
#print(get_admin_password.__name__)


### Decorating functions with parameters
#import functools
#
#user = {'username': 'jose', 'access_level': 'guest'}
#
#def make_secure(func):
#    # Wraps a function with another function
#    @functools.wraps(func)
#    def secure_function(*args, **kwargs):
#        if user['access_level'] == 'admin':
#            return func(*args, **kwargs)
#        else:
#            return f'No admin permissions for {user["username"]}.'
#    
#    return secure_function
#
#@make_secure
#def get_password(panel):
#    if panel == 'admin':
#        return '1234'
#    elif panel == 'billing':
#        return 'super_secure_password'
#
#
## Without wraps, it returns secure_function
## With wraps, it returns get_admin_password
#print(get_password('billing'))



### Decorators with parameters
#import functools
#
#user = {'username': 'jose', 'access_level': 'guest'}
#
#def make_secure(access_level):
#    def decorator(func):
#        # Wraps a function with another function
#        @functools.wraps(func)
#        def secure_function(*args, **kwargs):
#            if user['access_level'] == access_level:
#                return func(*args, **kwargs)
#            else:
#                return f'No admin permissions for {user["username"]}.'
#        
#        return secure_function
#    return decorator
#
#
#@make_secure('admin')
#def get_admin_password():
#    return 'admin: 1234'
#
#@make_secure('guest')
#def get_dashboard_password():
#    return 'user: user_password'
#
#print(get_admin_password())
#print(get_dashboard_password())


### Mutable parameter in Python
from typing import List, Optional

class Student:
    def __init__(self, name: str, grades: Optional[List[int]] = None):
        self.name = name
        self.grades = grades or []
    
    def take_exam(self, result: int):
        self.grades.append(result)

bob = Student('Bob')
rolf = Student('Rolf')
bob.take_exam(90)
print(bob.grades)
print(rolf.grades)