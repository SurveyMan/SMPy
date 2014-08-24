#example survey based on https://github.com/etosch/SurveyMan/blob/master/data/samples/sample3.csv
#outputs JSON representation

from surveyman.survey.surveys import *
from surveyman.survey.constraints import *
from surveyman.survey.blocks import *


def create_survey():

    b1 = Block([])

    oneof = "oneof"
    
    q1 = Question(oneof, "Block 1a", [])
    q1.add_option("a")
    q1.add_option("b")

    b1.add_question(q1)

    q2 = Question(oneof, "Block 1.1a", [])
    q2.add_option("c")
    q2.add_option("d")

    #trying different ways to add options
    q3 = Question(oneof, "Block 1.1b", [Option("e"), Option("f")])

    b1_1 = Block([q2, q3])
    b1.add_subblock(b1_1)

    q4 = Question(oneof, "Block 1b", [Option("g")])

    b1.add_question(q4)

    q5 = Question(oneof, "Block 1.2a", [Option("h")])

    b1_2 = Block([q5])

    q6 = Question(oneof, "Block 1.2.1b", [Option("X"), Option("Y")])

    q7 = Question(oneof, "Block 1.2.1a", [Option("j")])

    q8 = Question(oneof, "Block 1.2.2a", [Option("k")])

    q9 = Question(oneof, "Block 1.2.2b", [Option("l")])

    q10 = Question(oneof, "Block 1.2b", [Option("m")])

    b1_2_1 = Block([q6, q7])
    b1_2_2 = Block([q8, q9])

    b1_2.add_question(q10)

    b1_2.add_subblock(b1_2_1)
    b1_2.add_subblock(b1_2_2)

    q11 = Question(oneof, "Block 1.3a", [Option("n")])

    q12 = Question(oneof, "Block 1.3b", [Option("o")])

    q13 = Question(oneof, "Block 1.3c", [Option("p")])

    b1_3 = Block([q11, q12, q13])

    b1.add_subblock(b1_3)

    q14 = Question(oneof, "Block 2a", [Option("q"), Option("r")])
                   
    q15 = Question(oneof, "Block 2c", [Option("s"), Option("t")])

    q16 = Question(oneof, "Block 3a", [Option("u"), Option("v")])

    b2 = Block([q14, q15])

    b3 = Block([q16])

    q17 = Question(oneof, "Block 4a", [])
    q17.add_option("w")
    q17.add_option("x")
    q17.add_option("y")
    q17.add_option("z")

    b4 = Block([q17])

    q18 = Question(oneof, "Block 5.1a", [Option("1"), Option("2"), Option("3")])

    q19 = Question(oneof, "Block 5.1b", [Option("3"), Option("4")])

    b5_1 = Block([q18, q19])

    q20 = Question(oneof, "Block 5.2a", [Option("5"), Option("6")])

    q21 = Question(oneof, "Block 5.2b", [Option("7"), Option("8")])

    b5_2 = Block([q20, q21])

    b5 = Block([b5_1, b5_2])

    survey = Survey([b1, b2, b3, b4, b5], [])

    return survey