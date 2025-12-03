import os
import sys
class PicoTestBase:
    is_test_class = True

class TestingSuite:
    TEST_DIR = 'test'
    LIB_DIRECTORY = 'firmware'

    def __init__(self):
        self.tests_passed = 0
        self.test_count = 0
    
    def get_test_methods(self, obj):
        """    Returns a list of all the methods in a class that are prefixed with 'test_'. """
        methods = [method for method in dir(obj) if method.startswith('test_') and callable(getattr(obj, method))]
        self.test_count += len(methods)
        return methods
        
    def run_all(self):

        subs = self.find_test_subclasses()
        if len(subs) == 0:
            print("No tests found")
            return
        
        for obj in subs:
            self.run_test_class(obj)

        if self.test_count == 0:
            print("No tests found")
        elif self.tests_passed == self.test_count:
            print("All tests passed") 


    def run_test_class(self, obj):
        inst = obj()
        for m in self.get_test_methods(inst):
            method = getattr(inst, m)
            method()
            self.tests_passed += 1
            print(f"Tests passed: {self.tests_passed}")


    def find_test_subclasses(self):
        """
        Finds all classes that inherit from the given base class name across the project.
        """
        # Add the parent directory (which contains the 'lib' directory) to the system path
        sys.path.insert(0, '..')
        sys.path.insert(0, f'../{self.LIB_DIRECTORY}')

        test_modules = []
        test_subclasses = []
        
        # Get a list of all the class names in the current module
        for filename in os.listdir():
            if filename.endswith(".py") and filename != 'TestingSuite.py':
                test_modules.append(f"{filename.split(".")[0]}")

        for module_name in test_modules:
            module = __import__(module_name)
            for name in dir(module):
                obj = getattr(module, name)
                if isinstance(obj, type) and hasattr(obj, 'is_test_class') and obj.is_test_class:
                    test_subclasses.append(obj)
                    
        return test_subclasses

if __name__ == "__main__":
    t = TestingSuite()
    t.run_all()