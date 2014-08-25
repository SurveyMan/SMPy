__author__ = "mmcmahon13"

import json
from surveyman.survey.constraints import NEXT
from surveyman.survey.blocks import get_farthest_ancestor
from __ids__ import *
from survey_exceptions import *

__surveyGen__ = IdGenerator("s")


class Survey:
    """
    Contains the components of a survey:
    A survey is defined as a list of blocks and a list of branching constraints
    "breakoff" indicates whether the user can quit the survey early
    """

    def __init__(self, blocklist, constraints, breakoff=True):
        """
        Creates a Survey object with a unique id.
        The block list and branch lists are required arguments
        The default value of "breakoff" is true

        :param blocklist: The top level list of blocks
        :param constraints: The associated constraints
        :param breakoff: Boolean value indicating the ability to submit results early
        """
        # generate ID
        self.surveyID = __surveyGen__.generateID()
        #survey is a list of blocks, which hold questions and subblocks
        #at least one block with all the questions in it
        self.blockList = blocklist
        #list of branching constraints
        self.constraints = constraints
        self.hasBreakoff = breakoff

    def add_block(self, block):
        """
        Adds a top level block to the end of the survey's block list (assumed to be a top level block)

        :param block: The block to add
        """
        self.blockList.append(block)

    def add_block_by_index(self, block, index):
        """
        Adds a top level block to the desired index in the survey's block list.
        If the index is out of range, just inserts in the last position.

        :param block: The block to add to the top level of the survey
        :param index: The index at which the block should be added
        """
        self.blockList.insert(index, block)

    def validate(self):
        """
        Checks that the survey branching is valid before producing the JSON representation
        Confirms that:
        -all blocks follow either the branch-one, branch-all, or branch-none policy
        -all branch questions branch to top-level blocks in the survey's blocklist
        -all branches branch forward
        An exception is thrown if any of these conditions are violated
        """
        # check that all blocks are either branch none, branch one, or branch all
        #change so that it checks subblocks for branching also?
        for b in self.blockList:
            b.valid_branch_number()

        #check that all branches branch to top level blocks in the survey
        for c in self.constraints:
            for bid in c.get_blocks():
                survey_has_block = False
                for b in self.blockList:
                    #print("survey block: "+b.blockid + " " +"block branched to: "+bid)
                    if b.blockId == bid or bid is NEXT:
                        survey_has_block = True
                        break
                if not survey_has_block:
                    raise InvalidBranchException(
                        "Question " + c.question.qText + " does not branch to a block in survey")

        #check that all branches branch forward 
        for c in self.constraints:
            branch_question = c.question
            #print branchQuestion.block
            topmost_enclosing_block_id = get_farthest_ancestor(branch_question.block).blockId
            block_ids = [b.blockId for b in self.blockList]
            for bid in c.get_blocks():
                if bid is not NEXT and block_ids.index(topmost_enclosing_block_id) >= block_ids.index(bid):
                    raise InvalidBranchException("Question " + branch_question.qText + " does not branch forward")

    def __str__(self):
        # include some visualization of current branch/block structure?
        output = "Survey ID: " + self.surveyID + "\n"
        for b in self.blockList:
            output = output + str(b) + "\n"
        return output

    def jsonize(self):
        """
        Returns the JSON representation of the survey. This is validated against

        :return: JSON object according to the `Survey Schema <http://surveyman.github.io/Schemata/survey_input.json>`_
        """
        self.validate()
        __survey__ = "survey"
        __breakoff__ = "breakoff"
        __correlation__ = "correlation"
        __otherValues__ = "otherValues"

        output = {__survey__: [json.loads(b.jsonize()) for b in self.blockList], __breakoff__: self.hasBreakoff,
                  __correlation__: {}, __otherValues__: {}}

        return json.dumps(output)