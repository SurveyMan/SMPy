__author__ = 'mmcmahon13'
from surveyman.survey.options import *
import __ids__
import re

__qGen__ = __ids__.IdGenerator("q_")
__likert__ = "likert"
__checkbox__ = "checkbox"
__oneof__ = "oneof"
__instruction__ = "instruction"
__freetext__ = "freetext"
__qTypes__ = {
    "likert": __likert__,
    "checkbox": __checkbox__,
    "oneof": __oneof__,
    "instruction": __instruction__,
    "freetext": __freetext__
}


class Question:
    """
    Contains the components of a survey question:
    Question type is either "radio", "dropdown", "check", or "freetext"
    Question contains text and options, and can be shuffled in a block or fixed
    A question may contain a branchmap
    """

    def __init__(self, qType, qText, options=[], shuffle=True, freetext=None, breakoff=True):
        """
        Creates a Question object with a unique id
        Question type, text, and a list of options must be specified
            (option list may be empty)
        Shuffling is allowed by default; user must specify otherwise

        :param qType: One of "likert", "checkbox", "oneof", "freetext", or "instructional"
        :param qText: The text to display
        :param options: The list of options associated with this question, if applicable.
        :param shuffle: Boolean to permit shuffling.
        :param freetext: Boolean, regular expression, or default string. Only use this if qType is "freetext"
        :param breakoff: Boolean indicating whether breakoff is permitted at this question.
        :return:
        """
        # initialize variables depending on how many arguments provided
        # if you don't want to add options immediately, add empty list as argument
        #call generateID
        self.qId = __qGen__.generateID()
        if qType not in __qTypes__:
            raise NoSuchQuestionTypeException("%s not in {%s}" % (qType, ",".join(__qTypes__.keys())))
        else:
            self.qType = __qTypes__[qType]
        self.qText = qText
        self.shuffle = shuffle
        self.branching = False
        self.branch_map = None
        self.block = None
        self.breakoff = breakoff
        self.freetext = freetext
        self.options = options
        assert (freetext is not True or len(self.options) is 0)

    def add_option(self, o):
        """
        Adds o to the end of the question's option list. If type(o) is 'str', then this function creates an Option with
        this text before adding it.
        :param o: Option to add to this questions' option list.
        :return:
        """
        if self.qType in [__instruction__, __freetext__]:
            raise QuestionTypeException("Questions of type %s cannot have options." % self.qType)
        if type(o) is str:
            try:
                self.options.append(HTMLOption(o))
            except HTMLValidationException:
                self.options.append(TextOption(o))
        else:
            self.options.append(o)

    def add_option_by_index(self, index, o):
        """
        Adds o at the desired index in the question's option list. If type(o) is 'str', then this function creates an
        Option with this text before adding it. This method will pad with empty options if an option is added beyond the
        current list.
        :param index: The target index for where o should be inserted.
        :param o: Either the text or html of a survey object, or an option object.
        :return:
        """
        if self.qType in [__instruction__, __freetext__]:
            raise QuestionTypeException("Questions of type %s cannot have options." % self.qType)
        if index > len(self.options):
            for i in range(len(self.options), index):
                self.options.append(Option(""))
        if type(o) is str:
            try:
                self.options.insert(index, HTMLOption(o))
            except HTMLValidationException:
                self.options.insert(index, TextOption(o))
        else:
            self.options.insert(index, o)

    def __eq__(self, other):
        """
        Returns true if self and q2 have the same id.
        :param other: Question to compare self to.
        :return:
        """
        return type(other) == Question.__class__ and self.qId == other.qid

    def __str__(self):
        text = "Question ID: " + str(self.qId) + " Question type: " + self.qType + "\n"
        text = text + self.qText + "\n"
        for o in self.options:
            text = text + "\t" + str(o) + "\n"
        return text

    def jsonize(self):
        """
        Returns JSON representation of the question
        :return: JSON representation of self
        """

        output = {"id": self.qId, "qtext": self.qText, "breakoff": self.breakoff}

        if self.qType is __instruction__:
            return json.dumps(output)

        if self.qType is __freetext__:
            if (type(self.freetext) is bool and self.freetext) or type(self.freetext) is str:
                output["freetext"] = self.freetext
            elif type(self.freetext) is type(re.compile("")):
                output["freetext"] = str("#{%s}" % self.freetext.pattern)
            return json.dumps(output)

        output["options"] = [json.loads(o.jsonize()) for o in self.options]
        output["randomize"] = self.shuffle
        output["ordered"] = self.qType is __likert__
        output["exclusive"] = self.qType in [__likert__, __oneof__]

        if self.branch_map is not None:
            output["options"] = self.branch_map.jsonize()

        return json.dumps(output)


class Instruction(Question):
    """
    Instructional convenience class
    """

    def __init__(self, qText):
        Question.__init__(self, "instruction", qText)


class FreeText(Question):
    """
    Freetext convenience class
    """

    def __init__(self, qText, regex=None, default=None):
        """
        Convenient initialization of a Freetext question. Freetext questions cannot have both regular expressions and
        default values associated with them.
        :param qText: Question text
        :param regex: String or Pattern object for freetext contents to validate against
        :param default: Default text appearing in a freetext box.
        :return:
        """
        if regex is not None and default is not None:
            raise QuestionTypeException("Freetext questions cannot have both a regex and a default value.")
        if regex is not None:
            if type(regex) is str:
                Question.__init__(self, "freetext", qText, freetext=re.compile(regex))
            elif type(regex) is type(re.compile("")):
                Question.__init__(self, "freetext", qText, freetext=regex)
            else:
                raise QuestionTypeException("Unknown regular expression type: %s (recongized values are %s and %s)" %
                                            (type(regex), str, type(re.compile(""))))
        elif default is not None:
            Question.__init__(self, "freetext", qText, freetext=default)
        else:
            Question.__init__(self, "freetext", qText, freetext=True)