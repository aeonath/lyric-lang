# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Tests for Sprint 3 Task 4: Class Enhancements and Self Behavior."""

import pytest
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.errors import RuntimeErrorLyric
import io
import sys


def test_class_with_init_method_a11():
    """Test A11: Classes with init() initialize instance variables correctly."""
    source = '''
    class Person
        def init(name, age) {
            self.name = name
            self.age = age
            self.greeting = "Hello"
        }
        def get_info() {
            return self.name + " is " + str(self.age) + " years old"
        }
    +++
    
    def main() {
        person = Person("Alice", 30)
        info = person.get_info()
        return info
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == "Alice is 30 years old"


def test_method_calls_instance_syntax_a12():
    """Test A12: Method calls using instance.method() work and print correct values."""
    source = '''
    class Calculator
        def init() {
            self.history = []
        }
        def add(a, b) {
            result = a + b
            self.history = self.history + [result]
            return result
        }
        def get_history() {
            return self.history
        }
    +++
    
    def main() {
        calc = Calculator()
        result1 = calc.add(5, 3)
        result2 = calc.add(10, 20)
        history = calc.get_history()
        return result1 + result2
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 38  # 8 + 30


def test_instance_variable_assignment_a13():
    """Test A13: Assigning and reading instance variables works correctly."""
    source = '''
    class BankAccount
        def init(initial_balance) {
            self.balance = initial_balance
            self.transactions = []
        }
        def deposit(amount) {
            self.balance = self.balance + amount
            self.transactions = self.transactions + ["deposit: " + str(amount)]
        }
        def withdraw(amount) {
            if self.balance >= amount:
                self.balance = self.balance - amount
                self.transactions = self.transactions + ["withdraw: " + str(amount)]
                return True
            else:
                return False
            end
        }
        def get_balance() {
            return self.balance
        }
    +++
    
    def main() {
        account = BankAccount(100)
        account.deposit(50)
        account.withdraw(25)
        return account.get_balance()
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 125  # 100 + 50 - 25


def test_class_without_init_method():
    """Test that classes without init() method still work correctly."""
    source = '''
    class Point
        x = 0
        y = 0
        def move(dx, dy) {
            self.x = self.x + dx
            self.y = self.y + dy
        }
        def get_position() {
            return [self.x, self.y]
        }
    +++
    
    def main() {
        point = Point()
        point.move(5, 10)
        point.move(-2, 3)
        pos = point.get_position()
        return pos[0] + pos[1]
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 16  # (5-2) + (10+3) = 3 + 13 = 16


def test_multiple_instances_independence():
    """Test that multiple instances of the same class are independent."""
    source = '''
    class Counter
        def init() {
            self.count = 0
        }
        def increment() {
            self.count = self.count + 1
        }
        def get_count() {
            return self.count
        }
    +++
    
    def main() {
        counter1 = Counter()
        counter2 = Counter()
        
        counter1.increment()
        counter1.increment()
        counter2.increment()
        
        return counter1.get_count() + counter2.get_count()
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 3  # 2 + 1


def test_init_method_with_no_parameters():
    """Test init() method with no parameters."""
    source = '''
    class DefaultPerson
        def init() {
            self.name = "Unknown"
            self.age = 0
        }
        def set_name(name) {
            self.name = name
        }
        def get_name() {
            return self.name
        }
    +++
    
    def main() {
        person = DefaultPerson()
        person.set_name("Bob")
        return person.get_name()
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == "Bob"


def test_init_method_with_type_parameters():
    """Test init() method with typed parameters."""
    source = '''
    class TypedPerson
        def init(str name, int age) {
            self.name = name
            self.age = age
        }
        def get_info() {
            return self.name + ":" + str(self.age)
        }
    +++
    
    def main() {
        person = TypedPerson("Charlie", 25)
        return person.get_info()
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == "Charlie:25"


def test_init_method_type_error():
    """Test that init() method enforces parameter types."""
    source = '''
    class TypedPerson
        def init(str name, int age) {
            self.name = name
            self.age = age
        }
    +++
    
    def main() {
        person = TypedPerson("Charlie", "invalid")
        return person.name
    }'''
    
    ast = parse(source)
    with pytest.raises(RuntimeErrorLyric, match="Type error: parameter 'age' expects int"):
        evaluate(ast)


def test_complex_class_with_multiple_methods():
    """Test complex class with multiple methods and instance variables."""
    source = '''
    class ShoppingCart
        def init() {
            self.items = []
            self.total = 0
        }
        def add_item(str name, int price) {
            self.items = self.items + [name]
            self.total = self.total + price
        }
        def remove_item(str name) {
            # Simple removal - just remove first occurrence
            new_items = []
            removed = False
            # Simplified: just add all items for now (no actual removal logic)
            new_items = self.items
            self.items = new_items
        }
        def get_total() {
            return self.total
        }
        def get_item_count() {
            return len(self.items)
        }
    +++
    
    def main() {
        cart = ShoppingCart()
        cart.add_item("apple", 2)
        cart.add_item("banana", 1)
        cart.add_item("apple", 2)
        return cart.get_total()
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 5  # 2 + 1 + 2


def test_self_reference_in_nested_calls():
    """Test self reference in nested method calls."""
    source = '''
    class MathUtils
        def init() {
            self.multiplier = 2
        }
        def double(x) {
            return self.multiply(x, self.multiplier)
        }
        def multiply(a, b) {
            return a * b
        }
        def triple(x) {
            return self.multiply(x, 3)
        }
    +++
    
    def main() {
        math = MathUtils()
        result1 = math.double(5)
        result2 = math.triple(4)
        return result1 + result2
    }'''
    
    ast = parse(source)
    result = evaluate(ast)
    assert result == 22  # (5 * 2) + (4 * 3) = 10 + 12 = 22
