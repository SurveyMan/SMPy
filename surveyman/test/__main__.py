__author__ = 'etosch'
import unittest
import BlockTests
import ConstraintTests

unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(BlockTests.BlockTests))
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(ConstraintTests.ConstraintTests))