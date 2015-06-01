import surveyman.survey.questions as questions
import surveyman.survey.options as options
import surveyman.survey.blocks as blocks
import surveyman.survey.constraints as constraints
import surveyman.survey.surveys as surveys

def create_survey():

    oneof = "oneof"

    q1 = questions.Question(oneof, "Question 1", [options.Option(str(x)) for x in range(1, 4)])
    q2 = questions.Question(oneof, "Question 2", [options.Option(str(x)) for x in range(1, 4)])
    q3 = questions.Question(oneof, "Question 3", [options.Option(str(x)) for x in range(1, 4)])

    b1 = blocks.Block([q1, q2])
    b2 = blocks.Block([q3])
    b4 = blocks.Block([questions.Question(oneof, "Question 4", [])])

    b3 = blocks.Block([b1, b2])

    branch = constraints.Constraint(q3)
    branch.add_branch_by_index(0, b4)

    survey = surveys.Survey([b3, b4], [branch])
    return survey
