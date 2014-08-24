import unittest
from surveyman.survey.blocks import *
import surveyman.examples.subblock_example as sbEx
import surveyman.examples.example_survey as ex
import surveyman.examples.SimpleSurvey as simpEx


class BlockTests(unittest.TestCase):

    def setUp(self):
        self.blockSurvey = sbEx.create_survey()
        self.ipierotisSurvey = ex.create_survey()
        self.simpleSurvey = simpEx.create_survey()

    def tearDown(self):
        del self.blockSurvey
        del self.ipierotisSurvey
        del self.simpleSurvey

    def count_blocks(self, block_list):
        if len(block_list) == 0:
            return 0
        else:
            sum_subblocks = 0
            for b in block_list:
                sum_subblocks += self.count_blocks(b.get_subblocks())
            return sum_subblocks + len(block_list)

    #assert that the test surveys contain the desired number of blocks
    def test_block_number(self):
        print("Running block number test")
        self.assertEqual(self.count_blocks(self.ipierotisSurvey.blockList),3)
        self.assertEqual(self.count_blocks(self.blockSurvey.blockList),9)
        self.assertEqual(self.count_blocks(self.simpleSurvey.blockList),4)
     
    def test_add_blocks(self):
        print("Running add block test")
        block1 = Block([])
        block1.add_question(Question("oneof", "this is a question", [Option("pick me")]))
        block2 = Block([])
        block1.add_subblock(block2)
        self.assertEqual(self.count_blocks([block1]),2)

        #print str(block1)
        self.ipierotisSurvey.add_block(block1)
        self.blockSurvey.add_block(block1)
        self.simpleSurvey.add_block(block1)
        
        self.assertEqual(self.count_blocks(self.ipierotisSurvey.blockList),5)
        self.assertEqual(self.count_blocks(self.blockSurvey.blockList),11)
        self.assertEqual(self.count_blocks(self.simpleSurvey.blockList),6)