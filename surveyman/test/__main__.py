__author__ = 'etosch'
import unittest
import BlockTests
import ConstraintTests
import SurveyTests
import surveyman.examples.SimpleSurvey as simple
import surveyman.examples.example_survey as example
import surveyman.examples.subblock_example as sub
import surveyman.jsonValidator as validator
import json

unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(BlockTests.BlockTests))
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(ConstraintTests.ConstraintTests))
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(SurveyTests.OptionTests))
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(SurveyTests.QuestionTests))
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(SurveyTests.BlockTests))
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(SurveyTests.ConstraintTests))
unittest.TextTestRunner(verbosity=2).run(unittest.TestLoader().loadTestsFromTestCase(SurveyTests.SurveyTests))

# dump surveys to json
ex1 = simple.create_survey()
ex2 = example.create_survey()
ex3 = sub.create_survey()
examples = [ex1, ex2, ex3]

for (i, ex) in enumerate(examples):
    json_survey = ex.jsonize()
    validator.validate_json(json.loads(json_survey))
    with open("ex"+str(i)+".json", "w") as f:
        f.write(json_survey)