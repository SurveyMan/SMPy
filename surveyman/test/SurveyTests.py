__author__ = 'etosch'

import json
import unittest
import re
import surveyman.jsonValidator as validator
import surveyman.examples.SimpleSurvey as simple
import surveyman.examples.example_survey as example
import surveyman.examples.subblock_example as sub
import surveyman.survey.questions as questions
import surveyman.survey.surveys as surveys
import surveyman.survey.blocks as blocks
import surveyman.survey.options as options
import surveyman.survey.constraints as constraints
from surveyman.survey.questions import __instruction__, __likert__, __checkbox__, __freetext__
from surveyman.survey.blocks import __branch_none__

class SurveyTests(unittest.TestCase):

    def setUp(self):
        self.ex1 = simple.create_survey()
        self.ex2 = example.create_survey()
        self.ex3 = sub.create_survey()
        self.s = surveys.Survey([blocks.Block([])], [])

    def test_add_block(self):
        b = blocks.Block([questions.Question(__instruction__, "")])
        self.s.add_block(b)
        self.assertEqual(self.s.blockList.index(b), 1)
        b.add_question(questions.FreeText(""))
        self.assertEqual(len(self.s.blockList[-1].contents), 2)

    def test_add_block_by_index(self):
        self.s.add_block_by_index(blocks.Block([]), 2)
        self.s.add_block_by_index(blocks.Block([]), 10)

    def test_jsonize(self):
        for ex in [self.s, self.ex1, self.ex2, self.ex3]:
            validator.validate_json(json.loads(ex.jsonize()))


class QuestionTests(unittest.TestCase):

    def setUp(self):
        self.q1 = questions.Question("oneof", "", [options.Option(str(a)) for a in range(4)])
        self.q2 = questions.Instruction("")
        self.q3 = questions.FreeText("", regex="[0-9]+")
        self.q4 = questions.FreeText("", regex=re.compile("[0-9]+"))
        self.q5 = questions.FreeText("", default="")

    def test_question_types(self):
        self.assertRaises(surveys.NoSuchQuestionTypeException, questions.Question, "rank", "blah")

    def test_add_option(self):
        self.q1.add_option("")
        self.assertEqual(len(self.q1.options), 5)
        self.assertRaises(surveys.QuestionTypeException, self.q2.add_option, options.Option(""))

    def test_add_option_by_index(self):
        opt1, opt2 = options.Option("asdf"), options.Option("fdsa")
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
        self.assertRaises(surveys.QuestionTypeException, questions.FreeText, "", regex=".*", default="")


class OptionTests(unittest.TestCase):

    def setUp(self):
        self.text_opt = options.TextOption("some text")
        self.html_opt = options.HTMLOption("<img src='http://dogr.io/doge.png' alt='Such Coding'>")

    def test_option_subtypes(self):
        self.assertIsInstance(self.text_opt, options.Option, "TextOption should be an instance of Option")
        self.assertIsInstance(self.html_opt, options.Option, "HTMLOption should be an instance of Option")
        self.assertNotEquals(self.text_opt, self.html_opt)

    def test_html_parse_error(self):
        self.assertRaises(surveys.HTMLValidationException, options.HTMLOption, "<a>asdf")

    def test_jsonize(self):
        json1 = json.loads(self.text_opt.jsonize())
        validator.validate_json(json1, schema=validator.option_schema)
        print self.html_opt.jsonize()
        json2 = json.loads(self.html_opt.jsonize())
        validator.validate_json(json2, schema=validator.option_schema)


class BlockTests(unittest.TestCase):

    def setUp(self):
        self.basic_block = blocks.Block([questions.Question(__likert__, "", [])])

    def test_add_question(self):
        ct = len(self.basic_block.get_questions())
        self.assertGreater(ct, 0)
        self.basic_block.add_question(questions.Question(__checkbox__, "", [options.Option(str(a)) for a in range(4)]))
        self.assertEquals(ct+1, len(self.basic_block.get_questions()))

    def test_add_subblock(self):
        qct = len(self.basic_block.get_questions())
        bct = len(self.basic_block.get_subblocks())
        self.basic_block.add_subblock(blocks.Block([questions.Question(__instruction__, ""),
                                                    blocks.Block([questions.Question(__freetext__, "")])]))
        self.assertEqual(qct, len(self.basic_block.get_questions()))
        self.assertEqual(bct+1, len(self.basic_block.get_subblocks()))
        self.assertEqual(1, len(self.basic_block.get_subblocks()[0].get_subblocks()))

    def test_branch_validity(self):
        self.assertEqual(__branch_none__, self.basic_block.valid_branch_number())

    def test_farthest_ancestor(self):
        sb1 = blocks.Block([questions.FreeText("")])
        sb2 = blocks.Block([sb1])
        sb3 = blocks.Block([sb2])
        self.assertEqual(surveys.get_farthest_ancestor(sb1), sb3)

    def test_get_all_blocks(self):
        sb1 = blocks.Block([questions.FreeText("")])
        self.assertEqual(len(sb1.contents), 1)
        self.assertIsInstance(sb1.contents[0], questions.Question)
        self.assertItemsEqual(blocks.get_all_subblocks(sb1), [sb1])
        sb4 = blocks.Block([questions.Instruction("")])
        sb2 = blocks.Block([sb1, sb4])
        self.assertEqual(len(sb2.contents), 2)
        self.assertIsInstance(sb2.contents[0], blocks.Block)
        self.assertIsInstance(sb2.contents[1], blocks.Block)
        self.assertItemsEqual(blocks.get_all_subblocks(sb2), [sb1, sb2, sb4])
        sb3 = blocks.Block([sb2])
        self.assertEqual(len(sb3.contents), 1)
        self.assertIsInstance(sb3.contents[0], blocks.Block)
        self.assertItemsEqual(blocks.get_all_subblocks(sb3), [sb1, sb2, sb3, sb4])

    def test_cycles(self):
        sb1 = blocks.Block([])
        sb2 = blocks.Block([sb1])
        self.assertRaises(surveys.CycleException, sb1.add_subblock, sb2)
        self.basic_block.add_subblock(sb2)
        self.assertRaises(surveys.CycleException, sb1.add_subblock, self.basic_block)

    def test_jsonize(self):
        validator.validate_json(json.loads(self.basic_block.jsonize()), schema=validator.block_schema)


class ConstraintTests(unittest.TestCase):

    def setUp(self):
        self.q = questions.Question(__checkbox__, "", [options.TextOption(str(a)) for a in range(4)])
        self.outer_block_1 = blocks.Block([self.q])
        self.outer_block_2 = blocks.Block([])
        self.constraint = constraints.Constraint(self.q)

    def test_add_branch_by_index(self):
        self.constraint.add_branch_by_index(0, self.outer_block_2)
        self.assertRaises(IndexError, self.constraint.add_branch_by_index, 10, self.outer_block_2)

    def test_add_branch(self):
        opt = self.q.options[1]
        self.constraint.add_branch(opt, self.outer_block_2)
        opt2 = options.TextOption("")
        self.assertRaises(surveys.NoSuchOptionException, self.constraint.add_branch, opt2, self.outer_block_2)

    def test_add_branch_by_op_text(self):
        self.constraint.add_branch_by_op_text("2", self.outer_block_2)
        self.assertRaises(surveys.NoSuchOptionException, self.constraint.add_branch_by_op_text, "asdf", self.outer_block_2)

    def test_get_blocks(self):
        # add a bunch of constraints and see if we get the right stuff back
        b1, b2 = blocks.Block([]), blocks.Block([])
        self.constraint.add_branch_by_op_text("0", self.outer_block_2)
        self.constraint.add_branch(self.q.options[2], b1)
        self.constraint.add_branch_by_index(3, b2)
        self.assertItemsEqual(self.constraint.get_blocks(), [self.outer_block_2, b1, b2, blocks.NEXTBLOCK])

    def test_jsonize(self):
        b1, b2 = blocks.Block([]), blocks.Block([])
        self.constraint.add_branch_by_op_text("0", self.outer_block_2)
        self.constraint.add_branch(self.q.options[2], b1)
        self.constraint.add_branch_by_index(3, b2)
        json1 = self.outer_block_1.jsonize()
        json2 = self.outer_block_2.jsonize()
        validator.validate_json(json.loads(json1), schema=validator.block_schema)
        validator.validate_json(json.loads(json2), schema=validator.block_schema)