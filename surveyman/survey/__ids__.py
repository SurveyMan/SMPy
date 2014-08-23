__author__ = 'mmcmahon13'

class IdGenerator:
    """
    Generates ids for survey components; component prefixes are passed as arguments
    (op=option id, s=survey id, q=question id, b=block id, c=constraint id)
    """
    def __init__(self, prefix):
        self.numAssigned=0
        self.prefix=prefix

    def generateID(self):
        """Generates a new component id with the appropriate prefix"""
        self.numAssigned+=1
        return self.prefix+str(self.numAssigned)