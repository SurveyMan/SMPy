__author__ = 'etosch'
import unittest
import surveyman.jsonValidator as validator
from surveyman.survey.questions import *
from surveyman.survey.blocks import *


class SurveyTests(unittest.TestCase):
    pass


class QuestionTests(unittest.TestCase):

    def setUp(self):
        self.q1 = Question("oneof", "", [Option(str(a)) for a in range(4)])
        self.q2 = Instruction("")
        self.q3 = FreeText("", regex="[0-9]+")
        self.q4 = FreeText("", regex=re.compile("[0-9]+"))
        self.q5 = FreeText("", default="")

    def test_question_types(self):
        self.assertRaises(NoSuchQuestionTypeException, Question, "rank", "blah")

    def test_add_option(self):
        self.q1.add_option("")
        self.assertEqual(len(self.q1.options), 5)
        self.assertRaises(QuestionTypeException, self.q2.add_option, Option(""))

    def test_add_option_by_index(self):
        opt1, opt2 = Option("asdf"), Option("fdsa")
        self.q1.add_option_by_index(2, opt1)
        self.assertEqual(self.q1.options.index(opt1), 2)
        ct = len(self.q1.options)
        index = ct+4
        self.q1.add_option_by_index(index, opt2)
        self.assertEqual(len(self.q1.options), index+1)
        self.assertEqual(self.q1.options.index(opt2), index)

    def test_jsonize(self):
        for q in [self.q1, self.q2, self.q3, self.q4, self.q5]:
            validator.validate_json(json.loads(q.jsonize()), schema=validator.question_schema)
        self.assertRaises(QuestionTypeException, FreeText, "", regex=".*", default="")


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
        validator.validate_json(json1, schema=validator.option_schema)
        print self.html_opt.jsonize()
        json2 = json.loads(self.html_opt.jsonize())
        validator.validate_json(json2, schema=validator.option_schema)


class BlockTests(unittest.TestCase):

    def setUp(self):
        self.basic_block = Block([Question(__likert__, "", [])])

    def test_add_question(self):
        ct = len(self.basic_block.get_questions())
        self.assertGreater(ct, 0)
        self.basic_block.add_question(Question(__checkbox__, "", [Option(str(a)) for a in range(4)]))
        self.assertEquals(ct+1, len(self.basic_block.get_questions()))

    def test_add_subblock(self):
        qct = len(self.basic_block.get_questions())
        bct = len(self.basic_block.get_subblocks())
        self.basic_block.add_subblock(Block([Question(__instruction__, ""), Block([Question(__freetext__, "")])]))
        self.assertEqual(qct, len(self.basic_block.get_questions()))
        self.assertEqual(bct+1, len(self.basic_block.get_subblocks()))
        self.assertEqual(1, len(self.basic_block.get_subblocks()[0].get_subblocks()))

    def test_branch_validity(self):
        self.assertEqual(__branch_none__, self.basic_block.valid_branch_number())

    def test_cycles(self):
        pass

    def test_jsonize(self):
        validator.validate_json(json.loads(self.basic_block.jsonize()), schema=validator.block_schema)

class ConstraintTests(unittest.TestCase):

    def test_branch_validity(self):
        pass


