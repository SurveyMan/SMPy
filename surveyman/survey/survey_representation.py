#requires Python 2.7.5
#attempt at survey representation

from __ids__ import *
from surveyman.survey.questions import *

surveyGen = IdGenerator("s")
constraintGen = IdGenerator("c")


class Survey:
    """
    Contains the components of a survey:
    A survey is defined as a list of blocks and a list of branching constraints
    "breakoff" indicates whether the user can quit the survey early
    """

    def __init__(self, blocklist, constraints, breakoff = True):
        """
        Creates a Survey object with a unique id.
        The block list and branch lists are required arguments
        The default value of "breakoff" is true
        """
        #generate ID
        self.surveyID = surveyGen.generateID()
        #survey is a list of blocks, which hold questions and subblocks
        #at least one block with all the questions in it
        self.blockList = blocklist
        #list of branching constraints
        self.constraints = constraints
        self.hasBreakoff = breakoff
        
    def addBlock(self, block):
        """Adds a top level block to the end of the survey's block list"""
        #add block to end of survey (assumed to be a top level block)
        self.blockList.append(block)
        
    def addBlockByIndex(self, block, index):
        """
        Adds a top level block to the desired index in the survey's block list
        Throws index out of bounds exception if index is out of the list's range
        """
        #add block at certain index
        #throws index out of bounds exception (?)
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
        #check that all blocks are either branch none, branch one, or branch all
        #change so that it checks subblocks for branching also?
        for b in self.blockList:
            b.valid_branch_number(); #should throw exception if invalid
        
                
        #check that all branches branch to top level blocks in the survey
        for c in self.constraints:
            for bid in c.getBlocks():
                surveyHasBlock = False
                for b in self.blockList:
                    #print("survey block: "+b.blockid + " " +"block branched to: "+bid)
                    if b.blockid == bid or bid == "NEXT":
                        surveyHasBlock = True
                        break
                if surveyHasBlock == False:
                    badBranch = InvalidBranchException("Question "+c.question.qText+" does not branch to a block in survey")
                    raise badBranch()
            
        #check that all branches branch forward 
        for c in self.constraints:
            branchQuestion = c.question
            #print branchQuestion.block
            blockID = branchQuestion.block.split(".")[0]
            surveyBlockIds = [b.blockid for b in self.blockList]
            for bid in c.getBlocks():
                if(bid !="NEXT" and surveyBlockIds.index(blockID)>=surveyBlockIds.index(bid)):
                    badBranch = InvalidBranchException("Question "+branchQuestion.qText+" does not branch forward")
                    raise badBranch()
        
    def __str__(self):
        """returns a string representation of the survey"""
        #include some visualization of current branch/block structure?
        output = "Survey ID: "+self.surveyID+"\n"
        for b in self.blockList:
            output = output+str(b)+"\n"
        return output
        
    def jsonize(self):
        """returns the JSON representation of the survey"""
        self.validate()
        if self.hasBreakoff:
            breakoff = "true"
        else:
            breakoff = "false"
        output = "{'breakoff' : '%s', 'survey' : [%s] }" %(breakoff, ",".join([b.jsonize() for b in self.blockList]))
        output = output.replace("\'", "\"")
        return output


class Constraint:
    """
    The Constraint object defines a mapping of a question's options to blocks
    in the survey. This is also referred to as branching.
    A branch question has an associated Constraint known as its branch map.
    """
    #defines a mapping from a question options to Blocks
    def __init__(self, question):
        """
        Constructs a Constraint object with a unique id.
        The constraint is associated with the given question, which is labeled as a branch question.
        By default, the options branch to "null" blocks
        """
        self.cid = constraintGen.generateID()
        #add check here to make sure survey contains question
        question.branching = True
        question.branchMap = self
        self.question = question
        #holds list of tuples (opid, blockid)
        self.constraintMap = []
        for o in self.question.options:
            self.constraintMap.append((o.opId, "NEXT"))

    def addBranchByIndex(self, opIndex, block):
        """
        adds a branch from the option at the desired index in the question's option list
        to the desired block.
        Throws an exception if the index is out of the option list's range.
        """
        #throws index out of bounds exception
        self.constraintMap[opIndex] =(self.question.options[opIndex].opId, block.blockid)

    def addBranch(self, op, block):
        """
        adds a branch from a specific option object in the question's option list
        to the desired block.
        Throws an exception if the the question does not have the option.
        """
        for i in range(len(self.question.options)):
            if self.question.options[i].equals(op):
                self.constraintMap[i] = (op.opid, block.blockid)
                return
        noOp = NoSuchOptionException("Question "+self.question.quid+" does not contain option "+op.id)
        raise noOp()

    def addBranchByOpText(self, opText, block):
        """
        adds a branch from the option with the desired text in the question's option list
        to the desired block.
        Throws an exception if the the question does not have the option.
        """
        for i in range(len(self.question.options)):
            if self.question.options[i].opText==opText:
                self.constraintMap[i] = (self.question.options[i].opId, block.blockid)
                return
        noOp = NoSuchOptionException("Question "+self.question.quid+" does not contain option \""+opText+'\"')
        raise noOp()

    #returns all blocks branched to by this question
    def getBlocks(self):
        """returns a list of the blocks branched to by the Constraint"""
        output = []
        for c in self.constraintMap:
            output.append(c[1])
        return output

    def __str__(self):
        """returns the string representation of the Constraint"""
        output = "Constraint ID: "+self.cid+"\n"+"branches: \n"
        for (opid, blockID) in self.constraintMap:
            output = output+"\t"+str((opid, blockID))+"\n"
        return output

    def jsonize(self):
        """returns the JSON representation of the Constraint"""
        temp = "";
        cmap = []
        for tup in self.constraintMap:
            temp+="'"+tup[0]+"' : "
            if(tup[1] == "null"):
                temp+="null"
            else:
                temp+="'"+tup[1]+"'"
            cmap.append(temp)
            temp=""
        output = "[%s]"%(",".join(cmap))
        output = output.replace('\'', '\"');
        output= output.replace('[','{')
        output = output.replace(']','}')
        return output


    
