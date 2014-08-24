#survey exception class
#based on suggestions from
#http://stackoverflow.com/questions/1319615/proper-way-to-declare-custom-exceptions-in-modern-python


class ExceptionTemplate(Exception):
    def __call__(self, *args):
        return self.__class__(*(self.args + args))


class SurveyException(ExceptionTemplate):
    pass


class InvalidBlockException(ExceptionTemplate):
    pass


class InvalidBranchException(ExceptionTemplate):
    pass


class NoSuchBlockException(ExceptionTemplate):
    pass


class NoSuchQuestionException(ExceptionTemplate):
    pass


class NoSuchOptionException(ExceptionTemplate):
    pass


class HTMLValidationException(ExceptionTemplate):
    pass


class NoSuchQuestionTypeException(ExceptionTemplate):
    pass


class QuestionTypeException(ExceptionTemplate):
    pass

class UnknownContentsException(ExceptionTemplate):
    pass

class CycleException(ExceptionTemplate):
    pass