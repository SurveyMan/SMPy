__author__ = "mmcmahon13"
import unittest
from surveyman.survey.survey_exceptions import *
import surveyman.examples.subblock_example as subEx
import surveyman.examples.example_survey as exSurv
import surveyman.examples.SimpleSurvey as simpSurv
import surveyman.examples.TwoBranchesOneBlock as twob1b
import surveyman.examples.TwoBranchesOneBlock2 as twob2b2
import surveyman.examples.TwoBranchesOneSubblock2 as twob1sub
import surveyman.examples.BackwardsBranching as backwards
import surveyman.examples.BranchToSubblock as branch2sub


class ConstraintTests(unittest.TestCase):

    def setUp(self):
        self.block_survey = subEx.create_survey()
        self.ipierotis_survey = exSurv.create_survey()
        self.simple_survey = simpSurv.create_survey()
        self.broken_branch = twob1b.create_survey()
        self.broken_branch_2 = twob2b2.create_survey()
        self.broken_branch_subblock = twob1sub.create_survey()
        self.backwards_branch = backwards.create_survey()
        self.branch_to_subblock = branch2sub.create_survey()

    def tearDown(self):
        del self.block_survey
        del self.ipierotis_survey
        del self.simple_survey
        del self.broken_branch
        del self.broken_branch_2
        del self.broken_branch_subblock
        del self.backwards_branch
        del self.branch_to_subblock

    def test_top_level_branch_check(self):
        print("testing top level branch check")
        self.assertRaises(InvalidBranchException, self.branch_to_subblock.jsonize)
        #check that surveys with valid/no branching throw no exceptions
        self.block_survey.jsonize
        self.ipierotis_survey.jsonize
        self.simple_survey.jsonize

    def test_backwards_branch_check(self):
        print("testing backwards branch check")
        self.assertRaises(InvalidBranchException, self.backwards_branch.jsonize)
        #check that surveys with valid/no branching throw no exceptions
        self.block_survey.jsonize
        self.ipierotis_survey.jsonize
        self.simple_survey.jsonize

    def test_block_branch_number(self):
        print("testing block paradigm check")
        #check that survey with invalid BranchAll throws exception
        self.assertRaises(InvalidBranchException, self.broken_branch.jsonize)
        self.assertRaises(InvalidBranchException, self.broken_branch_2.jsonize)
        self.assertRaises(InvalidBranchException, self.broken_branch_subblock.jsonize)
        #check that surveys with valid/no branching throw no exceptions
        self.block_survey.jsonize
        self.ipierotis_survey.jsonize
        self.simple_survey.jsonize


if __name__ == '__main__':
    unittest.main()