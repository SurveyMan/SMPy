#example survey based on https://github.com/etosch/SurveyMan/blob/master/data/samples/sample3.csv
#outputs JSON representation

import surveyman.survey.surveys as surveys
import surveyman.survey.blocks as blocks
import surveyman.survey.questions as questions
import surveyman.survey.options as options

def create_survey():

    b1 = blocks.Block([])

    oneof = "oneof"
    
    q1 = questions.Question(oneof, "Block 1a", [])
    q1.add_option("a")
    q1.add_option("b")

    b1.add_question(q1)

    q2 = questions.Question(oneof, "Block 1.1a", [])
    q2.add_option("c")
    q2.add_option("d")

    #trying different ways to add options
    q3 = questions.Question(oneof, "Block 1.1b", [options.Option("e"), options.Option("f")])

    b1_1 = blocks.Block([q2, q3])
    b1.add_subblock(b1_1)

    q4 = questions.Question(oneof, "Block 1b", [options.Option("g")])

    b1.add_question(q4)

    q5 = questions.Question(oneof, "Block 1.2a", [options.Option("h")])

    b1_2 = blocks.Block([q5])

    q6 = questions.Question(oneof, "Block 1.2.1b", [options.Option("X"), options.Option("Y")])

    q7 = questions.Question(oneof, "Block 1.2.1a", [options.Option("j")])

    q8 = questions.Question(oneof, "Block 1.2.2a", [options.Option("k")])

    q9 = questions.Question(oneof, "Block 1.2.2b", [options.Option("l")])

    q10 = questions.Question(oneof, "Block 1.2b", [options.Option("m")])

    b1_2_1 = blocks.Block([q6, q7])
    b1_2_2 = blocks.Block([q8, q9])

    b1_2.add_question(q10)

    b1_2.add_subblock(b1_2_1)
    b1_2.add_subblock(b1_2_2)

    q11 = questions.Question(oneof, "Block 1.3a", [options.Option("n")])

    q12 = questions.Question(oneof, "Block 1.3b", [options.Option("o")])

    q13 = questions.Question(oneof, "Block 1.3c", [options.Option("p")])

    b1_3 = blocks.Block([q11, q12, q13])

    b1.add_subblock(b1_3)

    q14 = questions.Question(oneof, "Block 2a", [options.Option("q"), options.Option("r")])
                   
    q15 = questions.Question(oneof, "Block 2c", [options.Option("s"), options.Option("t")])

    q16 = questions.Question(oneof, "Block 3a", [options.Option("u"), options.Option("v")])

    b2 = blocks.Block([q14, q15])

    b3 = blocks.Block([q16])

    q17 = questions.Question(oneof, "Block 4a", [])
    q17.add_option("w")
    q17.add_option("x")
    q17.add_option("y")
    q17.add_option("z")

    b4 = blocks.Block([q17])

    q18 = questions.Question(oneof, "Block 5.1a", [options.Option("1"), options.Option("2"), options.Option("3")])

    q19 = questions.Question(oneof, "Block 5.1b", [options.Option("3"), options.Option("4")])

    b5_1 = blocks.Block([q18, q19])

    q20 = questions.Question(oneof, "Block 5.2a", [options.Option("5"), options.Option("6")])

    q21 = questions.Question(oneof, "Block 5.2b", [options.Option("7"), options.Option("8")])

    b5_2 = blocks.Block([q20, q21])

    b5 = blocks.Block([b5_1, b5_2])

    survey = surveys.Survey([b1, b2, b3, b4, b5], [])

    return survey