__author__ = 'etosch'

import json
from survey_exceptions import *
from abc import ABCMeta
from tidylib import tidy_fragment
import __ids__

__opGen__ = __ids__.IdGenerator("comp_")


class Option:
    """
    Contains the components of an option:
    An option has associated text

    This class is meant to be abstract. Please use HTMLOption or TextOption.
    """

    __metaclass__ = ABCMeta

    def __init__(self, op_text):
        """
        Creates an Option object with a unique id and the specified option text
        :param op_text:  The text to display (may be HTML)
        :return:
        """
        #initialize option text field
        self.opText = op_text
        #generate id for option
        self.opId = __opGen__.generateID()

    def __eq__(self, other):
        """
        Determines if self is the same option as other
        :param other: the Option to compare with
        :return:
        """
        return type(other) == Option.__class__ and self.opId == other.opId

    def jsonize(self):
        """
        Returns the JSON representation of the option
        :return:
        """
        return json.dumps({"id" : self.opId, "otext" : self.opText})

    def __str__(self):
        return self.opText


class TextOption(Option):
    pass


class HTMLOption(Option):

    def __init__(self, op_html):

        document, errors = tidy_fragment("<!DOCTYPE html><html><head><title></title><body>%s</body></html>" % op_html)
        # python is stupid
        if len(errors) > 1:
            print errors
            raise HTMLValidationException()
        else:
            Option.__init__(self, op_html)