#example of invalid branching
#based on https://github.com/etosch/SurveyMan/blob/master/data/tests/test4_two_branches_one_block.csv
import surveyman.survey.surveys as surveys
import surveyman.survey.blocks as blocks
import surveyman.survey.constraints as constraints
import surveyman.survey.questions as questions
import surveyman.survey.options as options


def create_survey():

    oneof = "oneof"

    q1 = questions.Question(oneof, "Question 1", [options.Option("foo"), options.Option("bar"), options.Option("baz")])
    q2 = questions.Question(oneof, "Question 2", [options.Option("boo"), options.Option("far"), options.Option("faz")])
    q3 = questions.Question(oneof, "Question 3", [options.Option("eggs"), options.Option("ham")])

    block1 = blocks.Block([q1, q2, q3])

    q4 = questions.Question(oneof, "Question 4", [options.Option("oscar"), options.Option("lucille"), options.Option("george")])
    q5 = questions.Question(oneof, "Question 5", [options.Option("maeby"), options.Option("george")])
    q6 = questions.Question(oneof, "Question 6", [options.Option("gob"), options.Option("lindsay")])
    q7 = questions.Question(oneof, "Question 7", [options.Option("anne veal"), options.Option("gene parmesean")])

    block2 = blocks.Block([q4, q5, q6, q7])

    #didn't add all options
    q8 = questions.Question(oneof, "Question 8", [options.Option("lupe"), options.Option("marky mark"), options.Option("tony wonder")])
    q9 = questions.Question(oneof, "Question 9", [options.Option("whooopsie"), options.Option("daisy")])

    block3 = blocks.Block([q8, q9])

    q10 = questions.Question(oneof, "Her?", [])

    block4 = blocks.Block([q10])

    q11 = questions.Question(oneof, "Would you mind telling us how this survey made you feel?", [])

    block5 = blocks.Block([q11])

    q12 = questions.Question(oneof, "Did someone say wonder?", [])

    block6 = blocks.Block([q12])

    branch1 = constraints.Constraint(q3)
    branch1.add_branch_by_op_text("eggs", block2)
    branch1.add_branch_by_op_text("ham", block3)

    #two branch questions in one block
    branch2 = constraints.Constraint(q1)
    branch2.add_branch_by_index(0, block4)
    branch2.add_branch_by_index(1, block3)
    branch2.add_branch_by_index(2, block3)

    block_list = [block1, block2, block3, block4, block5, block6]
    branch_list = [branch1, branch2]

    survey = surveys.Survey(block_list, branch_list)

    return survey