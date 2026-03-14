# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Test suite for Sprint 6 Task 8: Constructor Recognition."""

import pytest
from lyric.parser import parse
from lyric.interpreter import evaluate
from lyric.errors import ParseError, RuntimeErrorLyric


class TestConstructorRecognition:
    """Test constructor recognition where method name matches class name."""
    
    def test_basic_constructor_recognition(self):
        """Test basic constructor recognition."""
        source = """
        class Person:
            var name
            var age
            
            def Person(str name, int age) {
                self.name = name
                self.age = age
                print("Person created:", self.name, "age", self.age)
            }
        +++
        
        def main() {
            var person = Person("Alice", 30)
            print("Person name:", person.name)
            print("Person age:", person.age)
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)
    
    def test_constructor_with_parameters(self):
        """Test constructor with typed parameters."""
        source = """
        class Calculator:
            var name
            var history
            
            def Calculator(str name) {
                self.name = name
                self.history = []
                print("Calculator created:", self.name)
            }
            
            def add(int a, int b) {
                var result = a + b
                self.history.append(str(a) + " + " + str(b) + " = " + str(result))
                return result
            }
        +++
        
        def main() {
            var calc = Calculator("MyCalc")
            var result = calc.add(5, 3)
            print("Result:", result)
            print("History:", calc.history)
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)
    
    def test_constructor_without_parameters(self):
        """Test constructor without parameters."""
        source = """
        class Counter:
            var count
            
            def Counter() {
                self.count = 0
                print("Counter initialized")
            }
            
            def increment() {
                self.count = self.count + 1
                return self.count
            }
        +++
        
        def main() {
            var counter = Counter()
            var count1 = counter.increment()
            var count2 = counter.increment()
            print("Count:", count2)
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)
    
    def test_constructor_with_mixed_parameters(self):
        """Test constructor with mixed typed and untyped parameters."""
        source = """
        class Student:
            var name
            var id
            var grades
            
            def Student(str name, int id, var grades) {
                self.name = name
                self.id = id
                self.grades = grades
                print("Student created:", self.name, "ID:", self.id)
            }
            
            def get_average() {
                if self.grades.len() > 0:
                    return 85.0
                else:
                    return 0.0
                end
            }
        +++
        
        def main() {
            var student_grades = [85, 92, 78, 96]
            var student = Student("Charlie", 12345, student_grades)
            print("Student name:", student.name)
            print("Student ID:", student.id)
            print("Average:", student.get_average())
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)
    
    def test_multiple_constructors_error(self):
        """Test that multiple constructors raise an error."""
        source = """
        class Person:
            var name
            
            def Person(str name) {
                self.name = name
            }
            
            def Person(int age) {
                self.name = "Unknown"
                self.age = age
            }
        +++
        """
        
        with pytest.raises(ParseError) as exc_info:
            ast = parse(source, interactive=True)
        
        assert "Multiple constructors found for class 'Person'" in str(exc_info.value)
        assert "Only one constructor method is allowed per class" in str(exc_info.value)
    
    def test_constructor_vs_regular_method(self):
        """Test that constructor is distinguished from regular methods."""
        source = """
        class BankAccount:
            var owner
            var balance
            var transactions
            
            def BankAccount(str owner, flt initial_balance) {
                self.owner = owner
                self.balance = initial_balance
                self.transactions = []
                print("Account created for:", self.owner)
            }
            
            def deposit(flt amount) {
                self.balance = self.balance + amount
                self.transactions.append("Deposit: " + str(amount))
            }
            
            def withdraw(flt amount) {
                if self.balance >= amount:
                    self.balance = self.balance - amount
                    self.transactions.append("Withdrawal: " + str(amount))
                else:
                    print("Insufficient funds")
                end
            }
        +++
        
        def main() {
            var account = BankAccount("Alice", 1000.0)
            account.deposit(500.0)
            account.withdraw(200.0)
            print("Final balance:", account.balance)
            print("Transactions:", account.transactions.len())
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)
    
    def test_class_without_constructor(self):
        """Test class without constructor works normally."""
        source = """
        class Point:
            var x
            var y
            
            def move(int dx, int dy) {
                self.x = self.x + dx
                self.y = self.y + dy
            }
        +++
        
        def main() {
            var point = Point()
            point.x = 10
            point.y = 20
            print("Point:", point.x, point.y)
            point.move(5, 5)
            print("After move:", point.x, point.y)
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)
    
    def test_constructor_with_self_access(self):
        """Test constructor can access and modify self."""
        source = """
        class Config:
            var debug
            var version
            var port
            
            def Config() {
                self.debug = False
                self.version = "0.6.0"
                self.port = 8080
                print("Config initialized")
            }
            
            def update_config(str key, var value) {
                if key == "debug":
                    self.debug = value
                else:
                    if key == "version":
                        self.version = value
                    else:
                        if key == "port":
                            self.port = value
                        end
                    end
                end
            }
        +++
        
        def main() {
            var config = Config()
            config.update_config("debug", True)
            config.update_config("port", 9000)
            print("Debug:", config.debug)
            print("Port:", config.port)
            print("Version:", config.version)
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)
    
    def test_constructor_parameter_type_enforcement(self):
        """Test constructor parameter type enforcement."""
        source = """
        class Employee:
            var name
            var id
            var salary
            
            def Employee(str name, int id, flt salary) {
                self.name = name
                self.id = id
                self.salary = salary
                print("Employee created:", self.name)
            }
        +++
        
        def main() {
            # This should work with correct types
            var employee = Employee("David", 67890, 50000.0)
            print("Employee name:", employee.name)
            print("Employee ID:", employee.id)
            print("Employee salary:", employee.salary)
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)
    
    def test_constructor_with_complex_logic(self):
        """Test constructor with complex initialization logic."""
        source = """
        class Library:
            var name
            var books
            var members
            var total_books
            
            def Library(str name) {
                self.name = name
                self.books = []
                self.members = []
                self.total_books = 0
                print("Library created:", self.name)
            }
            
            def add_book(str title, str author) {
                var book = {"title": title, "author": author}
                self.books.append(book)
                self.total_books = self.total_books + 1
            }
            
            def get_stats() {
                return {"books": self.total_books, "members": self.members.len()}
            }
        +++
        
        def main() {
            var library = Library("Central Library")
            library.add_book("The Great Gatsby", "F. Scott Fitzgerald")
            library.add_book("1984", "George Orwell")
            var stats = library.get_stats()
            print("Library stats:", stats)
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)


class TestConstructorBackwardCompatibility:
    """Test backward compatibility with existing init() method."""
    
    def test_init_method_still_works(self):
        """Test that existing init() method still works."""
        source = """
        class Person:
            var name
            var age
            
            def init(str name, int age) {
                self.name = name
                self.age = age
                print("Person created with init():", self.name, "age", self.age)
            }
        +++
        
        def main() {
            var person = Person("Bob", 25)
            print("Person name:", person.name)
            print("Person age:", person.age)
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)
    
    def test_constructor_priority_over_init(self):
        """Test that constructor takes priority over init method."""
        source = """
        class Person:
            var name
            var age
            
            def Person(str name, int age) {
                self.name = name
                self.age = age
                print("Person created with constructor:", self.name, "age", self.age)
            }
            
            def init(str name, int age) {
                self.name = name
                self.age = age
                print("Person created with init():", self.name, "age", self.age)
            }
        +++
        
        def main() {
            var person = Person("Alice", 30)
            print("Person name:", person.name)
            print("Person age:", person.age)
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)


class TestConstructorErrorHandling:
    """Test error handling for constructor functionality."""
    
    def test_constructor_parameter_count_mismatch(self):
        """Test constructor with fewer arguments — missing params get None (nullable)."""
        source = """
        class Person:
            var name
            var age

            def Person(str name, int age) {
                self.name = name
                self.age = age
            }
        +++

        def main() {
            # This should work
            var person1 = Person("Alice", 30)

            # Missing age param gets None (nullable) — no type error
            var person2 = Person("Bob")
            print(person2.name)
            print(person2.age)
        }
        """

        ast = parse(source, interactive=True)
        import sys, io
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            evaluate(ast)
        finally:
            sys.stdout = old_stdout
        lines = captured.getvalue().strip().split("\n")
        assert lines[0] == "Bob"
        assert lines[1] == "None"
    
    def test_constructor_type_mismatch(self):
        """Test constructor with type mismatch."""
        source = """
        class Person:
            var name
            var age
            
            def Person(str name, int age) {
                self.name = name
                self.age = age
            }
        +++
        
        def main() {
            # This should fail with type mismatch
            var person = Person("Alice", "thirty")
        }
        """
        
        ast = parse(source, interactive=True)
        with pytest.raises(RuntimeErrorLyric) as exc_info:
            evaluate(ast)
        
        assert "type" in str(exc_info.value).lower()


class TestConstructorIntegration:
    """Test constructor integration with other language features."""
    
    def test_constructor_with_try_catch(self):
        """Test constructor with try/catch blocks."""
        source = """
        class SafeCalculator:
            var name
            var history
            
            def SafeCalculator(str name) {
                self.name = name
                self.history = []
                print("SafeCalculator created:", self.name)
            }
            
            def safe_divide(int a, int b) {
                try:
                    var result = a / b
                    self.history.append(str(a) + " / " + str(b) + " = " + str(result))
                    return result
                catch:
                    print("Division by zero error")
                    return 0
                fade
            }
        +++
        
        def main() {
            var calc = SafeCalculator("SafeCalc")
            var result1 = calc.safe_divide(10, 2)
            var result2 = calc.safe_divide(10, 0)
            print("Results:", result1, result2)
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)
    
    def test_constructor_with_loops(self):
        """Test constructor with loop initialization."""
        source = """
        class Counter:
            var count
            var max_count
            
            def Counter(int max_count) {
                self.count = 0
                self.max_count = max_count
                print("Counter created with max:", self.max_count)
            }
            
            def count_to_max() {
                int i
                for i in range(self.max_count):
                    self.count = self.count + 1
                    print("Count:", self.count)
                done
            }
        +++
        
        def main() {
            var counter = Counter(5)
            counter.count_to_max()
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)
    
    def test_constructor_with_function_calls(self):
        """Test constructor with function calls."""
        source = """
        class Logger:
            var name
            var log_level
            var messages
            
            def Logger(str name, str level) {
                self.name = name
                self.log_level = level
                self.messages = []
                print("Logger created:", self.name, "level:", self.log_level)
            }
            
            def log(str message) {
                var log_entry = "[" + self.log_level + "] " + message
                self.messages.append(log_entry)
                print(log_entry)
            }
            
            def get_message_count() {
                return self.messages.len()
            }
        +++
        
        def main() {
            var logger = Logger("AppLogger", "INFO")
            logger.log("Application started")
            logger.log("User logged in")
            print("Total messages:", logger.get_message_count())
        }
        """
        
        ast = parse(source, interactive=True)
        evaluate(ast)
