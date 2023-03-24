### Class 1
#class Student:
#    def __init__(self, name, grades):
#        #self.name = 'Rolf'
#        #self.grades = (90, 90, 93, 78, 90)
#        self.name = name
#        self.grades = grades
#    
#    def average(self):
#        return(sum(self.grades) / len(self.grades))
#
##student = Student()
##print(student.name)
##print(student.grades)
##print(Student.average(student))
##print(student.average())
#
#student = Student('Bob', (100, 100, 90, 90, 23))
#student2 = Student('Rolf', (80, 20, 100, 70, 88))
#print(student.name)
#print(student.grades)
#print(student.average())
#print(student2.name)
#print(student2.grades)
#print(student2.average())


### Class 2
#class Person:
#    def __init__(self, name, age):
#        self.name = name
#        self.age = age
#    
#    #def __str__(self):
#    #    #return f"Person {self.name} is {self.age} years old."
#
#    def __repr__(self):
#        return self.name
#
#bob = Person('bob', 30)
#
#print(bob)

### Class Test and class methods and static method
#class ClassTest:
#    def instance_method(self):
#        print(f'called instance_method of {self}')
#    
#    # With @classmethod decorator, cls will become the class itself i.e. ClassTest
#    @classmethod
#    def class_method(cls):
#        print(f'called instance_method of {cls}')
#    
#    # With @staticmethod decorator, it doesn't get any parameter unlike the other ones e.g. self, cls
#    @staticmethod
#    def static_method():
#        print('Called static_method')
#
#
##test = ClassTest()
##test.instance_method()
##ClassTest.instance_method(test)
#
##ClassTest.class_method()
#ClassTest.static_method()

#class Book():
#    TYPES = ('handcover', 'papaerback')
#
#    def __init__(self, name, book_type, weight):
#        self.name = name
#        self.book_type = book_type
#        self.weight = weight
#    
#    def __repr__(self):
#        return f'<Book {self.name}, {self.book_type}, weighing {self.weight}g>'
#    
#    @classmethod
#    def hardcover(cls, name, page_weight):
#        return cls(name, cls.TYPES[0], page_weight + 100)
#    
#    @classmethod
#    def paperback(cls, name, page_weight):
#        return cls(name, cls.TYPES[1], page_weight)
#
#book = Book('Harry Potter', 'hardcover', 1500)
#
#print(Book.TYPES)
#print(book.name)
#print(book)
#book = Book.hardcover('Harry Potter', 1500)
#light = Book.paperback('Python 101', 600)
#print(book)
#print(light)


### Class Inheritance
#class Device:
#    def __init__(self, name, connected_by):
#        self.name = name
#        self.connected_by = connected_by
#        self.connected = True
#    
#    def __str__(self):
#        return f'Device {self.name!r} ({self.connected_by})'
#    
#    def disconnect(self):
#        self.connected = False
#        print('Disconnected.')
#
#printer = Device('Printer', 'USB')
#print(printer)
#printer.disconnect()
#
## Printer inherits from Device class
#class Printer(Device):
#    def __init__(self, name, connected_by, capacity):
#        # initiate from the parent class
#        super().__init__(name, connected_by)
#        self.capacity = capacity
#        self.remaining_pages = capacity
#    
#    def __str__(self):
#        return f'{super().__str__()} ({self.remaining_pages} pages remaining)'
#    
#    def print(self, pages):
#        if not self.connected:
#            print('Your printer is not connected!')
#            return 
#        print(f'Printing {pages} pages')
#        self.remaining_pages -= pages
#
#printer = Printer('Printer', 'USB', 500)
#printer.print(20)
#
#print(printer)
#
## You can call function from the parent class
#printer.disconnect()
#printer.print(30)


### Class Composition
### e.g. A book shelf is composed of many books - use composition instead of inheritance
#class BookShelf:
#    def __init__(self, *books):
#        self.books = books
#    
#    def __str__(self):
#        return f'BookShelf with {len(self.books)} books.'
#
#shelf = BookShelf(300)
#
#class Book:
#    def __init__(self, name):
#        self.name = name
#    
#    def __str__(self):
#        return f'Book {self.name}'
#
#book = Book('Harry Potter')
#book2 = Book('Python 101')
#shelf = BookShelf(book, book2)
#
#print(shelf)


### Type Hinting

from typing import List # Tuple, Set, etc....

# List parameter, returns float
def list_avg(sequence: List) -> float:
    return sum(sequence) / len(sequence)

print(list_avg([1,2,3]))
