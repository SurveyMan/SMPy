__author__ = 'mmcmahon13'

import json
from __ids__ import *
from survey_exceptions import *

__constraintGen__ = IdGenerator("c")
__NEXT__ = "NEXT"


class Constraint:
    """
    The Constraint object defines a mapping of a question's options to blocks
    in the survey. This is also referred to as branching.
    A branch question has an associated Constraint known as its branch map.
    """

    def __init__(self, question):
        """
        Constructs a Constraint object with a unique id.
        The constraint is associated with the given question, which is labeled as a branch question.
        By default, the options branch to "null" blocks
        :param question: The question associated with this constraint
        """
        self.cid = __constraintGen__.generateID()
        #add check here to make sure survey contains question
        question.branching = True
        question.branch_map = self
        self.question = question
        #holds list of tuples (opid, blockid)
        self.constraintMap = []
        for o in self.question.options:
            self.constraintMap.append((o.opId, __NEXT__))

    def add_branch_by_index(self, opIndex, block):
        """
        Adds a branch from the option at the desired index in the question's option list to the desired block.
        Throws an exception if the index is out of the option list's range.
        :param opIndex: The option index associated with this Constraint
        :param block: The target destination for branching
        """
        #throws index out of bounds exception
        self.constraintMap[opIndex] = (self.question.options[opIndex].opId, block.blockId)

    def add_branch(self, op, block):
        """
        Adds a branch from a specific option object in the question's option list to the desired block.
        Throws an exception if the the question does not have the option.
        :param op: The Option object associated with this Constraint
        :param block: The target destination for branching
        """
        for i in range(len(self.question.options)):
            if self.question.options[i].equals(op):
                self.constraintMap[i] = (op.opid, block.blockId)
                return
        raise NoSuchOptionException("Question "+self.question.quid+" does not contain option "+op.id)

    def add_branch_by_op_text(self, opText, block):
        """
        Adds a branch from the option with the desired text in the question's option list to the desired block.
        Throws an exception if the the question does not have the option.
        :param opText: The text of the option to match against
        :param block: The target destination for branching
        """
        for i in range(len(self.question.options)):
            if self.question.options[i].opText == opText:
                self.constraintMap[i] = (self.question.options[i].opId, block.blockId)
                return
        raise NoSuchOptionException("Question "+self.question.quid+" does not contain option \""+opText+'\"')

    def get_blocks(self):
        """
        Returns a list of the blocks branched to by the Constraint
        :return: A list of Blocks
        """
        output = []
        for c in self.constraintMap:
            output.append(c[1])
        return output

    def __str__(self):
        output = "Constraint ID: "+self.cid+"\n"+"branches: \n"
        for (opid, blockID) in self.constraintMap:
            output = output+"\t"+str((opid, blockID))+"\n"
        return output

    def jsonize(self):
        """
        Returns the JSON representation of the Constraint
        :return: JSON representation according to schema at `http://surveyman.github.io/Schemata/survey_branchMap.json`
        """
        return json.dumps({opid : blockid for (opid, blockid) in self.constraintMap})