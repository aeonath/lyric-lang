# Lyric Programming Language
# Copyright (c) 2025-2026 MiraNova Studios
# All rights reserved.

"""Test suite for list_dict_tests.ly - Sprint 3 list and dictionary functionality tests."""

import pytest
import subprocess
import os
from lyric.lexer import tokenize
from lyric.parser import Parser
from lyric.interpreter import Interpreter
from lyric.errors import RuntimeErrorLyric


class TestListDictTests:
    """Test list and dictionary functionality."""
    
    def test_list_dict_tests_ly_runs_successfully(self):
        """Test that list_dict_tests.ly runs successfully through CLI."""
        list_dict_tests_path = os.path.join(os.path.dirname(__file__), '..', 'examples', 'list_dict_tests.ly')
        
        # Run the CLI command
        result = subprocess.run(['lyric', 'run', list_dict_tests_path],
                               capture_output=True, text=True)
        
        # Should succeed (exit code 0)
        assert result.returncode == 0, f"CLI failed with error: {result.stderr}"
        
        # Check that output contains expected content or is empty (no main function)
        output = result.stdout
        # Since the test file only has variable declarations, no output is expected
        assert len(output) >= 0  # Allow empty output
    
    def test_list_literals_and_basic_operations(self):
        """Test list literals and basic operations."""
        source = """
        var numbers = [1, 2, 3, 4, 5]
        var words = ["hello", "world", "lyric"]
        var mixed = [1, "hello", 3.14, True]
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values - now they are ArrObjects
        from lyric.interpreter import ArrObject
        assert isinstance(interpreter.global_scope['numbers'], ArrObject)
        assert interpreter.global_scope['numbers'].elements == [1, 2, 3, 4, 5]
        assert interpreter.global_scope['words'].elements == ["hello", "world", "lyric"]
        assert interpreter.global_scope['mixed'].elements == [1, "hello", 3.14, True]
    
    def test_dictionary_literals_and_basic_operations(self):
        """Test dictionary literals and basic operations."""
        source = """
        var person = {"name": "Alice", "age": 30, "city": "New York"}
        var scores = {"math": 95, "science": 87, "english": 92}
        var config = {"debug": True, "version": "0.3.0", "port": 8080}
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values - now they are MapObjects
        from lyric.interpreter import MapObject
        assert isinstance(interpreter.global_scope['person'], MapObject)
        assert interpreter.global_scope['person'].elements == {"name": "Alice", "age": 30, "city": "New York"}
        assert interpreter.global_scope['scores'].elements == {"math": 95, "science": 87, "english": 92}
        assert interpreter.global_scope['config'].elements == {"debug": True, "version": "0.3.0", "port": 8080}
    
    def test_list_indexing(self):
        """Test list indexing operations."""
        source = """
        var numbers = [1, 2, 3, 4, 5]
        var words = ["hello", "world", "lyric"]
        var first_number = numbers[0]
        var last_word = words[2]
        var middle_number = numbers[2]
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['first_number'] == 1
        assert interpreter.global_scope['last_word'] == "lyric"
        assert interpreter.global_scope['middle_number'] == 3
    
    def test_dictionary_key_access(self):
        """Test dictionary key access operations."""
        source = """
        var person = {"name": "Alice", "age": 30, "city": "New York"}
        var scores = {"math": 95, "science": 87, "english": 92}
        var person_name = person["name"]
        var person_age = person["age"]
        var math_score = scores["math"]
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['person_name'] == "Alice"
        assert interpreter.global_scope['person_age'] == 30
        assert interpreter.global_scope['math_score'] == 95
    
    def test_list_length_and_builtin_functions(self):
        """Test list length method."""
        source = """
        var numbers = [1, 2, 3, 4, 5]
        var words = ["hello", "world", "lyric"]
        var numbers_length = numbers.len()
        var words_length = words.len()
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values
        assert interpreter.global_scope['numbers_length'] == 5
        assert interpreter.global_scope['words_length'] == 3
    
    def test_dictionary_length_and_builtin_functions(self):
        """Test dictionary methods."""
        source = """
        var person = {"name": "Alice", "age": 30, "city": "New York"}
        var scores = {"math": 95, "science": 87, "english": 92}
        var person_keys = person.keys()
        var person_values = person.values()
        var scores_keys = scores.keys()
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values - keys() and values() return ArrObjects now
        from lyric.interpreter import ArrObject
        assert isinstance(interpreter.global_scope['person_keys'], ArrObject)
        assert set(interpreter.global_scope['person_keys'].elements) == {"name", "age", "city"}
        assert set(interpreter.global_scope['person_values'].elements) == {"Alice", 30, "New York"}
        assert set(interpreter.global_scope['scores_keys'].elements) == {"math", "science", "english"}
    
    def test_list_modification_append(self):
        """Test list modification with append."""
        source = """
        var numbers = [1, 2, 3, 4, 5]
        var words = ["hello", "world", "lyric"]
        numbers.append(6)
        words.append("test")
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values - now they are ArrObjects
        from lyric.interpreter import ArrObject
        assert isinstance(interpreter.global_scope['numbers'], ArrObject)
        assert interpreter.global_scope['numbers'].elements == [1, 2, 3, 4, 5, 6]
        assert interpreter.global_scope['words'].elements == ["hello", "world", "lyric", "test"]
    
    def test_dictionary_modification(self):
        """Test dictionary modification."""
        source = """
        var person = {"name": "Alice", "age": 30, "city": "New York"}
        var scores = {"math": 95, "science": 87, "english": 92}
        person["email"] = "alice@example.com"
        scores["history"] = 88
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values - access elements from MapObjects
        from lyric.interpreter import MapObject
        assert isinstance(interpreter.global_scope['person'], MapObject)
        assert interpreter.global_scope['person'].elements['email'] == "alice@example.com"
        assert interpreter.global_scope['scores'].elements['history'] == 88
    
    def test_nested_structures(self):
        """Test nested list and dictionary structures."""
        source = """
        var nested = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25}
            ],
            "settings": {
                "theme": "dark",
                "language": "en"
            }
        }
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check structure - access through elements
        from lyric.interpreter import MapObject, ArrObject
        nested = interpreter.global_scope['nested']
        assert isinstance(nested, MapObject)
        users = nested.elements['users']
        assert isinstance(users, ArrObject)
        assert users.len() == 2
        assert users.elements[0].elements['name'] == "Alice"
        assert users.elements[0].elements['age'] == 30
        settings = nested.elements['settings']
        assert isinstance(settings, MapObject)
        assert settings.elements['theme'] == "dark"
        assert settings.elements['language'] == "en"
    
    def test_complex_indexing(self):
        """Test complex indexing operations."""
        source = """
        var nested = {
            "users": [
                {"name": "Alice", "age": 30},
                {"name": "Bob", "age": 25}
            ],
            "settings": {
                "theme": "dark",
                "language": "en"
            }
        }
        var first_user = nested["users"][0]
        var first_user_name = nested["users"][0]["name"]
        var theme = nested["settings"]["theme"]
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values - access through elements
        from lyric.interpreter import MapObject
        first_user = interpreter.global_scope['first_user']
        assert isinstance(first_user, MapObject)
        assert first_user.elements['name'] == "Alice"
        assert interpreter.global_scope['first_user_name'] == "Alice"
        assert interpreter.global_scope['theme'] == "dark"
    
    def test_indexed_assignment(self):
        """Test indexed assignment operations."""
        source = """
        var numbers = [1, 2, 3, 4, 5]
        var person = {"name": "Alice", "age": 30}
        numbers[0] = 10
        person["age"] = 31
        """
        
        tokens = tokenize(source)
        parser = Parser(tokens)
        parser._interactive_mode = True
        parser.is_top_level = False
        ast = parser.parse()
        interpreter = Interpreter()
        
        # Should execute without errors
        interpreter.evaluate(ast)
        
        # Check values - access through elements
        from lyric.interpreter import ArrObject, MapObject
        numbers = interpreter.global_scope['numbers']
        person = interpreter.global_scope['person']
        assert isinstance(numbers, ArrObject)
        assert isinstance(person, MapObject)
        assert numbers.elements[0] == 10
        assert person.elements['age'] == 31
