import unittest

if __name__ == "__main__":
    tests = unittest.defaultTestLoader.discover(".")
    test_runner = unittest.TextTestRunner()
    test_runner.run(tests)
