__author__ = 'etosch'
import unittest
import surveyman.jsonValidator as validator
from surveyman.survey.questions import *


class SurveyTests(unittest.TestCase):
    pass


class QuestionTests(unittest.TestCase):

    def setUp(self):
        self.q1 = Question("oneof", "", [Option(a) for a in range(4)])
        self.q2 = Instruction("")

    def test_question_types(self):
        self.assertRaises(NoSuchQuestionTypeException, Question, ["rank", "blah"])

    def test_add_option(self):
        self.q1.add_option("")
        self.assertEqual(len(self.q1.options), 5)
        self.assertRaises(QuestionTypeException, self.q2.add_option, Option(""))

    def test_add_option_by_index(self):
        opt1, opt2 = Option("asdf"), Option("fdsa")
        self.q1.add_option_by_index(2, opt1)
        self.assertEqual(self.q1.options.index(opt1), 2)
        ct = len(self.q1.options)
        self.q1.add_option_by_index(ct+4, opt2)
        self.assertEqual(len(self.q1.options), ct+4)
        self.assertEqual(self.q1.options.index(opt2), ct+4)


class OptionTests(unittest.TestCase):

    def setUp(self):
        self.text_opt = TextOption("some text")
        self.html_opt = HTMLOption("<img src='http://dogr.io/doge.png' alt='Such Coding'>")

    def test_option_subtypes(self):
        self.assertIsInstance(self.text_opt, Option, "TextOption should be an instance of Option")
        self.assertIsInstance(self.html_opt, Option, "HTMLOption should be an instance of Option")
        self.assertNotEquals(self.text_opt, self.html_opt)

    def test_html_parse_error(self):
        self.assertRaises(HTMLValidationException, HTMLOption, "<a>asdf")

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


