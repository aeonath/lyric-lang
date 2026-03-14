class Person:
    var name = "Guest"
    var age = 25
    
    def greet() {
        print("Hello, I'm", self.name)
        print("I am", self.age, "years old")
    }
    
    def set_name(new_name) {
        self.name = new_name
    }
    
    def set_age(new_age) {
        self.age = new_age
    }
+++

class Student
    var name = "Student"
    var grade = "A"
    
    def introduce() {
        print("Hi, I'm", self.name)
        print("My grade is", self.grade)
    }
+++

def main() {
    print("Testing class functionality in Lyric")
    
    # Create instances
    var person = Person()
    var student = Student()
    
    # Test basic functionality
    print("\n=== Person Tests ===")
    person.greet()
    
    print("\n=== Student Tests ===")
    student.introduce()
    
    # Test instance variable modification
    print("\n=== Modifying Instance Variables ===")
    person.set_name("Alice")
    person.set_age(30)
    person.greet()
    
    student.name = "Bob"
    student.grade = "B+"
    student.introduce()
    
    # Test type checking
    print("\n=== Type Checking ===")
    print("person is Person:", isinstance(person, Person))
    print("person is Student:", isinstance(person, Student))
    print("student is Student:", isinstance(student, Student))
    print("student is Person:", isinstance(student, Person))
    
    print("Type of person:", type(person))
    print("Type of student:", type(student))
    print("Type of 5:", type(5))
    print("Type of 'hello':", type("hello"))
}
