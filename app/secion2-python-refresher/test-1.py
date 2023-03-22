#size_input = input('How big is your house (in square feet): ')
#square_feet = int(size_input)
#square_metres = square_feet / 10.8
#print(f'{square_feet} square feet is {square_metres:.2f} square metres')

### Lambda
#add = lambda x, y: x+y
#print(add(2, 3))

### Dictionary Comprehension
#users = {
#    (0, 'Bob', 'password'),
#    (1, 'Rolf', 'bob123'),
#    (2, 'Jose', 'longp4ssword'),
#    (3, 'username', '1234')
#}
#
##username_mapping = {user[1]: user[2] for user in users}
#username_mapping = {user[1]: user for user in users}
#
#print(username_mapping)
#
#username_input = input('Enter your username: ')
#password_input = input('Enter your password: ')
#
#_, username, password = username_mapping[username_input]
#
#if password_input == password:
#    print("Your details are correct")
#else:
#    print("Your details are incorrect")

### Unpacking args

#def multiply(*args):
#    #print(args)
#    total = 1
#    for arg in args:
#        total *= arg
#    print(total)
#    return total
#
#multiply(1, 3, 5)
#
#def add(x, y):
#    return x + y
#
#nums = [3,5]
#print(add(*nums))
#
#nums = {'x': 15, 'y': 25}
#print(add(**nums))
#
#def apply(*args, operator):
#    if operator == '*':
#        return multiply(*args)
#    elif operator == '+':
#        return sum(args)
#    else:
#        return 'No valid operator provided to apply().'
#
#print(apply(1, 3, 6, 7, operator='*'))


### Unpacking Keyword Arguments kwargs
#
#def named(name, age):
#    print(name, age)
#
#details = {
#    'name': 'Bob',
#    'age': 25,
#}
#
#named(**details)
#
#def print_nicely(**kwargs):
#    named(**kwargs)
#    for arg, value in kwargs.items():
#        print(f'{arg}: {value}')
#
#print_nicely(name='Bob', age=25)
#
#def both(*args, **kwargs):
#    print(args)
#    print(kwargs)
#
#both(1, 3, 5, name='Bob', age=25)

