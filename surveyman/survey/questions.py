__author__ = 'mmcmahon13'
from surveyman.survey.options import *
import __ids__

__qGen__ = __ids__.IdGenerator("q_")


class Question:
    """
    Contains the components of a survey question:
    Question type is either "radio", "dropdown", "check", or "freetext"
    Question contains text and options, and can be shuffled in a block or fixed
    A question may contain a branchmap
    """

    def __init__(self, qType, qText, options=[], shuffle=True):
        """
        Creates a Question object with a unique id
        Question type, text, and a list of options must be specified
            (option list may be empty)
        Shuffling is allowed by default; user must specify otherwise

        :param qType: One of "likert", "checkbox", "oneof", or "instructional"
        :param qText: The text to display
        :param options: The list of options associated with this question, if applicable.
        :param shuffle: Boolean to permit shuffling.
        :return:
        """
        # initialize variables depending on how many arguments provided
        #if you don't want to add options immediately, add empty list as argument
        #call generateID
        self.__likert__ = "likert"
        self.__checkbox__ = "checkbox"
        self.__oneof__ = "oneof"
        self.__instruction__ = "instruction"
        self.__qTypes__ = {
            "likert": self.__likert__
            , "checkbox": self.__checkbox__
            , "oneof": self.__oneof__
            , "instruction": self.__instruction__
        }
        if qType not in self.__qTypes__:
            raise NoSuchQuestionTypeException("%s not in {%s}" % (qType, ",".join(self.__qTypes__.keys())))
        self.qId = __qGen__.generateID()
        self.qType = self.__qTypes__[qType]
        self.qText = qText
        self.options = options
        self.shuffle = shuffle
        self.branching = False
        self.block = None

    def add_option(self, o):
        """
        Adds o to the end of the question's option list. If type(o) is 'str', then this function creates an Option with this text before adding it.
        :param o: Option to add to this questions' option list.
        :return:
        """
        if self.qType is self.__instruction__:
            raise QuestionTypeException("Instructional questions cannot have options.")
        if type(o) is str:
            try:
                self.options.append(HTMLOption(o))
            except HTMLValidationException:
                self.options.append(TextOption(o))
        else:
            self.options.append(o)

    def add_option_by_index(self, index, o):
        """
        Adds o at the desired index in the question's option list. If type(o) is 'str', then this function creates an Option with this text before adding it.
        This method will pad with empty options if an option is added beyond the current list.
        :param index: The target index for where o should be inserted.
        :param o: Either the text or html of a survey object, or an option object.
        :return:
        """
        if self.qType is self.__instruction__:
            raise QuestionTypeException("Instructional questions cannot have options.")
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
        :param q2: Question to compare self to.
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
        if hasattr(self, "branchMap"):
            output = "{'id' : '%s', 'qtext' : '%s', 'options' : [%s], 'branchMap' : %s}" % (
                self.qId, self.qText, ",".join([o.jsonize() for o in self.options]), self.branchMap.jsonize())
        else:
            output = "{'id' : '%s', 'qtext' : '%s', 'options' : [%s]}" % (
                self.qId, self.qText, ",".join([o.jsonize() for o in self.options]))
        output = output.replace('\'', '\"')
        return output


class Instruction(Question):
    def __init__(self, qText):
        Question.__init__(self, qText=qText, qType="instruction")

