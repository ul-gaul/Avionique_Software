import sys
import unittest

if __name__ == "__main__":
    tests = unittest.defaultTestLoader.discover(".")
    test_runner = unittest.TextTestRunner()
    test_result = test_runner.run(tests)

    if not test_result.wasSuccessful():
        sys.exit(-1)
