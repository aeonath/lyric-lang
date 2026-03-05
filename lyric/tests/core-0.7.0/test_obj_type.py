# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""def main() {\n    
Test suite for obj type (class instances).
Tests that obj can be used to explicitly type class instances.
\n}"""

import pytest
from lyric.parser import parse
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


class TestObjType:
    """def main() {\n    Test cases for obj type with class instances.\n}"""
    
    def test_obj_type_declaration_with_class_instance(self):
        """def main() {\n    Test that obj type can hold a class instance.\n}"""
        code = """
class Person
    def init(str name) {
        self.name = name
    }
+++

obj person = Person("Alice")
var name_value = person.name
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        # Verify the person is stored as obj type
        assert 'person' in interpreter.global_scope
        person = interpreter.global_scope['person']
        assert isinstance(person, dict)
        assert '__instance_class__' in person
        assert person['__instance_class__'] == 'Person'
        assert interpreter.global_scope['name_value'] == "Alice"
    
    def test_obj_type_with_methods(self):
        """def main() {\n    Test that obj instances can call methods.\n}"""
        code = """
class Calculator
    def init(int initial) {
        self.value = initial
    }
    
    def add(int x) {
        self.value = self.value + x
        return self.value
    }
+++

obj calc = Calculator(10)
var result = calc.add(5)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['result'] == 15
    
    def test_obj_type_multiple_instances(self):
        """def main() {\n    Test multiple obj instances of the same class.\n}"""
        code = """
class Counter
    def init() {
        self.count = 0
    }
    
    def increment() {
        self.count = self.count + 1
    }
+++

obj counter1 = Counter()
obj counter2 = Counter()

counter1.increment()
counter1.increment()
counter2.increment()
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        counter1 = interpreter.global_scope['counter1']
        counter2 = interpreter.global_scope['counter2']
        
        assert counter1['count'] == 2
        assert counter2['count'] == 1
    
    def test_obj_type_reassignment(self):
        """def main() {\n    Test that obj variables can be reassigned to different instances.\n}"""
        code = """
class Box
    def init(int size) {
        self.size = size
    }
+++

obj box = Box(10)
box = Box(20)
var final_size = box.size
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['final_size'] == 20
    
    def test_obj_type_with_var_interchangeable(self):
        """def main() {\n    Test that var can also hold class instances (backward compatibility).\n}"""
        code = """
class Animal
    def init(str name) {
        self.name = name
    }
+++

var animal1 = Animal("Dog")
obj animal2 = Animal("Cat")

var name1 = animal1.name
var name2 = animal2.name
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['name1'] == "Dog"
        assert interpreter.global_scope['name2'] == "Cat"
    
    def test_obj_type_error_when_not_class(self):
        """def main() {\n    Test that obj type rejects non-class values.\n}"""
        code = """
obj my_obj = 42
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch" in error_msg or "cannot assign" in error_msg
    
    def test_obj_type_error_with_string(self):
        """def main() {\n    Test that obj type rejects string values.\n}"""
        code = """
obj my_obj = "Hello"
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch" in error_msg or "cannot assign" in error_msg
    
    def test_obj_type_error_with_list(self):
        """def main() {\n    Test that obj type rejects list values.\n}"""
        code = """
obj my_obj = [1, 2, 3]
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            interpreter.evaluate(ast)
        
        error_msg = str(exc_info.value)
        assert "Type mismatch" in error_msg or "cannot assign" in error_msg
    
    def test_obj_in_function_parameter(self):
        """def main() {\n    Test passing obj as function parameter.\n}"""
        code = """
class Point
    def init(int x, int y) {
        self.x = x
        self.y = y
    }
+++

def get_x(obj point) {
    return point.x
}

obj p = Point(10, 20)
var x_value = get_x(p)
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['x_value'] == 10
    
    def test_obj_function_return_type(self):
        """def main() {\n    Test that functions can return obj type.\n}"""
        code = """
class Item
    def init(str name) {
        self.name = name
    }
+++

obj create_item(str item_name) {
    return Item(item_name)
}

obj my_item = create_item("Sword")
var item_name = my_item.name
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['item_name'] == "Sword"
    
    def test_obj_type_in_arr(self):
        """def main() {\n    Test storing obj instances in an arr.\n}"""
        code = """
class Book
    def init(str title) {
        self.title = title
    }
+++

obj book1 = Book("Book1")
obj book2 = Book("Book2")
arr books = [book1, book2]

var first_book = books[0]
var first_title = first_book.title
var count = books.len()
"""
        ast = parse(code, interactive=True)
        interpreter = Interpreter()
        interpreter.evaluate(ast)
        
        assert interpreter.global_scope['first_title'] == "Book1"
        assert interpreter.global_scope['count'] == 2
