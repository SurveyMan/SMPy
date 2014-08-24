#example of invalid branching
#based on https://github.com/etosch/SurveyMan/blob/master/data/tests/test4_two_branches_one_block.csv
from surveyman.survey.surveys import *
from surveyman.survey.blocks import *
from surveyman.survey.constraints import *


def create_survey():
    
    oneof = "oneof"
    
    q1 = Question(oneof, "Question 1", [Option("foo"), Option("bar"), Option("baz")])
    q2 = Question(oneof, "Question 2", [Option("boo"), Option("far"), Option("faz")])
    q3 = Question(oneof, "Question 3", [Option("eggs"), Option("ham")])

    block1 = Block([q1, q2, q3])

    q4 = Question(oneof, "Question 4", [Option("oscar"), Option("lucille"), Option("george")])
    q5 = Question(oneof, "Question 5", [Option("maeby"), Option("george")])
    q6 = Question(oneof, "Question 6", [Option("gob"), Option("lindsay")])
    q7 = Question(oneof, "Question 7", [Option("anne veal"), Option("gene parmesean")])

    block2 = Block([q4, q5, q6, q7])

    #didn't add all options
    q8 = Question(oneof, "Question 8", [Option("lupe"), Option("marky mark"), Option("tony wonder")])
    q9 = Question(oneof, "Question 9", [Option("whooopsie"), Option("daisy")])

    block3 = Block([q8, q9])

    q10 = Question(oneof, "Her?", [])

    block4 = Block([q10])

    q11 = Question(oneof, "Would you mind telling us how this survey made you feel?", [])

    block5 = Block([q11])

    q12 = Question(oneof, "Did someone say wonder?", [])

    block6 = Block([q12])

    branch1 = Constraint(q3)
    branch1.add_branch_by_op_text("eggs", block2)
    branch1.add_branch_by_op_text("ham", block3)

    #branch backwards
    branch2 = Constraint(q7)
    branch2.add_branch_by_index(0, block1)
    branch2.add_branch_by_index(1, block1)


    block_list = [block1, block2, block3, block4, block5, block6]
    branch_list = [branch1, branch2]

    survey = Survey(block_list, branch_list)

    return survey