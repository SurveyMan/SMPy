__author__ = 'etosch'
import unittest
from surveyman.survey.survey_representation import *
import surveyman.jsonValidator as validator


class SurveyTests(unittest.TestCase):
    pass


class QuestionTests(unittest.TestCase):
    pass


class OptionTests(unittest.TestCase):

    def setUp(self):
        self.text_opt = TextOption("some text")
        self.html_opt = HTMLOption("<img src='http://dogr.io/doge.png' alt='Such Coding'>")

    def test_option_subtypes(self):
        self.assertIsInstance(self.text_opt, Option, "TextOption should be an instance of Option")
        self.assertIsInstance(self.html_opt, Option, "HTMLOption should be an instance of Option")
        self.assertNotEquals(self.text_opt, self.html_opt)

    def test_html_parse_error(self):
        self.assertRaises(HTMLValidationExeception, HTMLOption, "<a>asdf")

    def test_jsonize(self):
        json1 = json.loads(self.text_opt.jsonize())
        validator.validateJSON(json1, schema=validator.option_schema)
        print self.html_opt.jsonize()
        json2 = json.loads(self.html_opt.jsonize())
        validator.validateJSON(json2, schema=validator.option_schema)


class BlockTests(unittest.TestCase):
    pass


class ConstraintTests(unittest.TestCase):
    pass


