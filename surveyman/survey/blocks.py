__author__ = 'mmcmahon13'
from __ids__ import *
from surveyman.survey.questions import *

__blockGen__ = IdGenerator("b_")
__branch_one__ = "branch-one"
__branch_all__ = "branch-all"
__branch_none__ = "branch-none"

branch_types = [__branch_all__, __branch_none__, __branch_one__]
"""
The complex interactions between branching and blocking are what gives SurveyMan its sophisticated control flow.
SurveyMan supports the following branching policies:

- branch-one: Either this block directly contains a branch question, or one of its sub-blocks is a branch-one.

- branch-none: This block contains no branching questions. None of its sub-blocks are branch-one. Its sub-blocks may be
a mix of branch-none or branch-all with the NEXT pointer.

- branch-all: Every question in a block has branching logic associated with it. All questions must have equivalent
branch maps. This block cannot contain any sub-blocks.

"""


def get_farthest_ancestor(block):
    """
    Returns the topmost block for the input.

    :param block: A block, which may be the sub-block of some other block.
    :return: A Block
    """

    assert isinstance(block, Block), type(block)

    if block.parent is None:
        return block
    else:
        return get_farthest_ancestor(block.parent)


def get_all_subblocks(block):
    """
    Traverses all sub-blocks and returns all descendants of the input block.

    :param block: The block whose descendants we want
    :return: A list of all sub-blocks.
    """

    assert(isinstance(block, Block))

    subblocks = [b for b in block.contents if isinstance(b, Block)]
    retval = []

    if len(subblocks) == 0:
        retval.append(block)
    else:
        blocks = [block]
        for sb in subblocks:
            blocks.extend(get_all_subblocks(sb))
        retval.extend(blocks)

    return retval


class Block:
    """
    Contains the components of a survey Block. A block can hold both questions and sub-blocks.
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
        self.parent = None

    def __subblock_ids(self):
        """
        Checks if block contains other blocks, giving them appropriate labels.
        Sub-blocks have ids in the form "parent_id.child_id."
        Fixes block labels of the questions contained in the sub-blocks.
        """
        if len(self.contents) != 0:
            for c in self.contents:
                if isinstance(c, Block):
                    # update blockId
                    c.blockId = self.blockId + "." + c.blockId
                    # set parent pointer
                    c.parent = self

    def __label_questions(self):
        """
        Labels questions with the id of the block that contains them

        :return:
        """
        if len(self.contents) != 0:
            for q in self.contents:
                if isinstance(q, Question):
                    q.block = self

    def __ensure_no_cycles(self, block):
        farthest_ancestor = get_farthest_ancestor(self)
        all_blocks = get_all_subblocks(farthest_ancestor)
        if block in all_blocks:
            raise CycleException("Block %s contains a cycle" % farthest_ancestor)

    def add_question(self, question):
        """
        Adds question to the end of the Block's list of contents.
        Labels the question with the containing block's id

        :param question: The question to add 
        """
        question.block = self
        self.contents.append(question)

    def add_subblock(self, subblock):
        """
        Adds a subblock to the end of the Block's list of contents.
        Labels the subblock with the containing block's id

        :param subblock:  The subblock to add.
        """
        self.__ensure_no_cycles(subblock)
        subblock.parent = self
        subblock.blockId = self.blockId + "." + subblock.blockId
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
            blocks_branched_to = None
            if len(branching) is not 0 and branching[0].branch_map is not None:
                blocks_branched_to = branching[0].branch_map.get_blocks()
            for q in branching:
                if q.branch_map is not None:
                    if q.branch_map.get_blocks() != blocks_branched_to:
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
        return isinstance(other, Block) and self.blockId == other.blockId

    def __str__(self):
        output = "Block ID: "+self.blockId+"\n"
        for c in self.contents:
            output = output+str(c)+"\n"
        return output

    def __hash__(self):
        return self.blockId.__hash__()

    def jsonize(self):
        """
        Returns the JSON representation of the block

        :return: A JSON object according to the `Block Schema <http://surveyman.github.io/Schemata/survey_block.json>`_
        """
        __id__ = "id"
        __questions__ = "questions"
        __randomize__ = "randomize"
        __subblocks__ = "subblocks"
        output = {__id__: self.blockId, __questions__: [], __randomize__: self.randomize, __subblocks__: []}
        for thing in self.contents:
            if isinstance(thing, Question):
                output[__questions__].append(json.loads(thing.jsonize()))
            elif isinstance(thing, Block):
                output[__subblocks__].append(json.loads(thing.jsonize()))
            else:
                raise UnknownContentsException("Block %s has contents %s. Only %s and %s are permitted." %
                                               (self.blockId, type(thing), Question.__class__, Block.__class__))
        return json.dumps(output)