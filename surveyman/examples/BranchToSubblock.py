from surveyman.survey.surveys import *
from surveyman.survey.blocks import *
from surveyman.survey.constraints import *


def create_survey():
    
    oneof = "oneof"
    
    q1 = Question(oneof, "Question 1", [Option(str(x)) for x in range(1, 4)])
    q2 = Question(oneof, "Question 2", [Option(str(x)) for x in range(1, 4)])
    q3 = Question(oneof, "Question 3", [Option(str(x)) for x in range(1, 4)])

    b1 = Block([q1, q2])
    b2 = Block([q3])
    b4 = Block([Question(oneof, "Question 4", [])])

    b3 = Block([b1, b2])

    branch = Constraint(q3)
    #not a top level block
    branch.add_branch_by_index(0, b1)
    branch.add_branch_by_index(1, b1)
    branch.add_branch_by_index(2, b1)

    survey = Survey([b3, b4], [branch])
    return survey