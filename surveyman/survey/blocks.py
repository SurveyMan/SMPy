__author__ = 'mmcmahon13'
from __ids__ import *
from surveyman.survey.questions import *

__blockGen__ = IdGenerator("b")
__branch_one__ = "branch-one"
__branch_all__ = "branch-all"
__branch_none__ = "branch-none"


class Block:
    """
    Contains the components of a survey Block.
    A block can hold both questions and subblocks
    """

    def __init__(self, contents, randomize=False):
        """
        Creates a Block object.
        Blocks are a list of contents which could be either subblocks or questions.
        Blocks may be randomized; by default, they are not.

        :param contents: List of blocks and/or questions
        :param randomize: Boolean -- is this a floating block?
        :return:
        """
        self.contents = contents
        self.blockId = __blockGen__.generateID()
        self.randomize = randomize
        self.__subblock_ids()
        self.__label_questions()

    def __subblock_ids(self):
        """
        Checks if block contains other blocks, giving them appropriate labels.
        Subblocks have ids in the form "parent_id.child_id."
        Fixes block labels of the questions contained in the subblocks.
        :return:
        """
        if len(self.contents) != 0:
            for c in self.contents:
                if isinstance(c,Block):
                    c.blockId=self.blockId+(".")+c.blockId
                    c.__label_questions()

    def __label_questions(self):
        """
        Labels questions with the id of the block that contains them
        :return:
        """
        if len(self.contents) != 0:
            for q in self.contents:
                if isinstance(q, Question):
                    q.block = self.blockId

    def add_question(self, question):
        """
        Adds question to the end of the Block's list of contents.
        Labels the question with the containing block's id
        :param question: The question to add 
        :return:
        """
        question.block = self.blockId
        self.contents.append(question)

    def add_subblock(self, subblock):
        """
        Adds a subblock to the end of the Block's list of contents.
        Labels the subblock with the containing block's id
        :param subblock:  The subblock to add.
        :return:
        """
        subblock.parent = self.blockId
        subblock.blockId = self.blockId+"."+subblock.blockId
        self.contents.append(subblock)

    def get_subblocks(self):
        """
        Returns a list of all the subblocks in the block
        :return: a list of Blocks
        """
        subblocks = []
        for c in self.contents:
            if isinstance(c, Block):
                subblocks.append(c)
        return subblocks

    def get_questions(self):
        """
        Returns a list of all the questions in the block
        :return: a list of Questions
        """
        questions = []
        for c in self.contents:
            if isinstance(c, Question):
                questions.append(c)
        return questions

    #rethinking how this is done, may move check to Survey object instead
    def valid_branch_number(self):
        """
        Checks if there are a valid number of branch questions in the block.
        The three possible policies are branch-one, branch-all, or branch-none.
        :return: a branch policy
        """
        branching = []
        num_questions = len(self.get_questions())
        for q in self.get_questions():
            if q.branching:
                branching.append(q)

        if len(branching) == 1:
            #if block contains a branch question, check that none of the subblocks are branch-one
            for b in self.get_subblocks():
                if b.valid_branch_number() == __branch_one__:
                    raise InvalidBranchException("Branch-one block cannot contain a branch-one subblock")
            return __branch_one__
        elif len(branching) is num_questions and len(branching) is not 0:
            #for branch all: check that all questions branch to the same block(s)
            if len(branching) is not 0 and branching[0].branch_map is not None:
                blocks_branched_to = branching[0].branch_map.getBlocks()
            for q in branching:
                if q.branch_map is not None:
                    if q.branch_map.getBlocks() != blocks_branched_to:
                        raise InvalidBranchException("Block branches to different destinations")
            #check that block does not contain subblocks if branch-all
            if len(self.get_subblocks()) is not 0:
                raise InvalidBranchException("Branch-all block cannot contain subblocks")
            return __branch_all__
        elif len(branching) is not 0:
            #throw invalid branch exception
            raise InvalidBranchException("Block contains too many branch questions")
        else:
            subblock_types = []
            for b in self.get_subblocks():
                subblock_types.append(b.valid_branch_number())
            #if there is a branch-one subblock, all of its siblings must be either branch-none or branch-all
            if subblock_types.count("branch-one") > 1:
                raise InvalidBranchException("Block has too many branch-one subblocks")
            else:
                return __branch_none__

    def __eq__(self, other):
        """
        True if this block has the same id as other.
        :param other: another Block
        :return: Boolean
        """
        return type(other) == Block.__class__ and self.blockId == other.blockid

    def __str__(self):
        output = "Block ID: "+self.blockId+"\n"
        for c in self.contents:
            output = output+str(c)+"\n"
        return output

    def jsonize(self):
        """
        Returns the JSON representation of the block
        :return:
        """
        qs = []
        bs = []
        for q in self.contents:
            if isinstance(q, Question):
                qs.append(q.jsonize())
            else:
                bs.append(q.jsonize())
        if self.randomize:
            r = "true"
        else:
            r = "false"
        output = "{'id' : '%s', 'questions' : [%s], 'randomize' : '%s', 'subblocks' : [%s] }"%(self.blockId, ",".join(qs), r, ",".join(bs))
        output = output.replace('\'', '\"')
        return output