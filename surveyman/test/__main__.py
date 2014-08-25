__author__ = 'etosch'
import unittest
import BlockTests
import ConstraintTests
import SurveyTests

unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(BlockTests.BlockTests))
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(ConstraintTests.ConstraintTests))
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(SurveyTests.OptionTests))
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(SurveyTests.QuestionTests))
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(SurveyTests.BlockTests))
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(SurveyTests.ConstraintTests))
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(SurveyTests.SurveyTests))


