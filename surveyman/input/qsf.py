"""Utility to parse Qualtrics Survey Format (.qsf) files into SurveyMan objects."""

import ujson as json
from ..survey import surveys
from ..survey.blocks import Block
from ..survey.questions import Question
from ..survey.constraints import Constraint
from ..survey.options import Option
from dataclasses import dataclass, field
from datetime import date
from typing import List, Dict
from abc import ABC
from collections import defaultdict

class StrInt(int):
    """Integers that apppear as strings in QSF file"""
    def __init__(self, i: str):
        super().__init__(i)

class StrBool(int):
    """Booleans that appear as strings in the QSF file"""
    def __init__(self, b: str):
        super().__init__(bool(b))


@dataclass
class SurveyEntry:
    """Metadata required by Qualtrics"""

    """Internal to Qualtrics. Should be used to override the survey package gensym."""
    SurveyID: str
    SurveyName: str
    SurveyDescription: str | None
    SurveyOwnerID: str
    SurveyBrandID: str
    DivisionID: str
    SurveyLanguage: str 
    SurveyActiveResponseSet: str # no idea what this is
    SurveyStatus : str           # not sure what the set of possibilities is
    SurveyStartDate: date 
    SurveyExpirationDate: date
    SurveyCreationDate: date
    CreatorID: str
    LastModified: date
    LastAccessed: date
    LastActivated: date
    Deleted: str | None

# declarations
class Element(ABC, dict): pass
class BlockListElement(Element): pass
class BlockElement(Element): pass
class FlowElement(Element): pass
class NoteElement(Element): pass
class PreviewLinkElement(Element): pass
class SurveyOptionsElement(Element): pass
class QuotaGroupOrder(Element): pass
class ScoringCategoriesElement(Element): pass
class ProjectCategoryElement(Element): pass
class SurveyStatisticsElement(Element): pass
class QuestionElement(Element): pass
class QuotaGroupElement(Element): pass
class RSElement(Element): pass

class DefaultBlockElement(BlockElement): pass
class QuestionBlockElement(BlockElement): pass
class RootBlockElement(BlockElement): pass


@dataclass
class SurveyElement:
    """Core objects and logic in a Qualtrics Survey"""
    SurveyID: str
    Element: str
    PrimaryAttribute: str
    SecondaryAttribute: str | None
    TertiaryAttribute: str | None
    Payload: dict | list | None

    def payload(self) -> Element:
        return Element.parse(self)


class Element(ABC, dict): 
    codes = {
        'BL'  : BlockListElement,
        'FL'  : FlowElement,
        'NT'  : NoteElement, 
        'PL'  : PreviewLinkElement, 
        'RS'  : RSElement, 
        'SO'  : SurveyOptionsElement, 
        'QGO' : (QuotaGroupOrder, [0]), 
        'SCO' : ScoringCategoriesElement, 
        'PROJ': ProjectCategoryElement, 
        'STAT': SurveyStatisticsElement, 
        'QC'  : QuestionElement, 
        'SQ'  : QuestionElement,
        'QG'  : QuotaGroupElement
    }

    def parse(elt: SurveyElement):
        if type(elt.Payload) is dict:
            return Element.codes[elt.Element](**elt.Payload)
        elif type(elt.Payload) is list:
            clz, keys = Element.codes[elt.Element]
            return clz(zip(keys, elt.Payload))
        else: 
            return Element.codes[elt.Element]()

@dataclass
class QuestionElement(Element):
    QuestionText: str
    DefaultChoices: bool
    DataExportTag: str # appears to the column label used in response data
    QuestionType: str 
    Selector: str 
    SubSelector: str 
    DataVisibility: dict #= field(default_factory=dict) #{'Private': False, 'Hidden': False}
    Configuration: dict #= field(default_factory=dict)
    QuestionDescription : str # the actual question text
    Choices: Dict[StrInt, Dict] # map from string ints to another map with the keys 'Display' for display text and 'TextEntry' bool
    ChoiceOrder: List[StrInt] 
    Validation: dict
    GradingData: list
    Language: str
    NextChoiceId: int
    NextAnswerId: int 
    QuestionID: str # should match the PrimaryAttribute value of the SurveyElement object
    DisplayLogic: dict # encodes branching?
    Randomization: dict 

    def get_surveyman_qtype(self) -> str:
        # I should be able to access these as named fields, but right now that's not working.
        a = self.QuestionType
        b = self.Selector

        # MC   multiple choice
        # MAVR multiple answer vertical
        # SAVR single answer vertical
        # SAHR single answer horizontal
        
        if a == 'MC' and b == 'MAVR':
            return 'checkbox'
        elif a == 'MC' and b in ['SAVR', 'SAHR', 'DL']:
            return 'oneof'
        elif a == 'TE':
            return 'freetext'
        elif b == 'Likert':
            return 'likert'
        elif a == 'DB':
            return 'instruction'
        else:
            raise ValueError('NYI'+str(self))

@dataclass
class QuotaGroupElement(Element):
    ID: str
    Name: str
    Selected: bool
    MultipleMatch: str
    Public: bool
    Quotas: list

@dataclass(frozen=True)
class SurveyStatisticsElement(Element):
    MobileCompatible: bool # note: this was converted into a python bool, not a string bool like the others
    ID: str 

@dataclass
class ScoringCategoriesElement(Element):
    ScoringCategories: list
    ScoringCategoryGroups: list
    ScoringSummaryCategory: str | None
    ScoringSummaryAfterQuestions: int
    ScoringSummaryAfterSurvey: int 
    DefaultScoringCategory: str | None 
    AutoScoringCategory: str | None


@dataclass(frozen=True)
class PrjectCategoryElement(Element):
    ProjectCategory: str 
    SchemaVersion: str

class QuotaGroupOrder(Element):
    def __init__(self, _, quota_group_id):
        self.quota_group_id = quota_group_id

@dataclass
class SurveyOptionsElement:
    BackButton: bool # need to double check that this won't cause problems when converting between Python and Qualtrics/JSON
    SaveAndContinue: bool # Not sure
    SurveyProtection: str # byInvitation
    BallotBoxStuffingProtection: bool # no idea
    NoIndex: str # no idea; in example, 'Yes'
    SecureResponseFiles: bool # no idea
    SurveyExpiration: date | None
    SurveyTermination: str
    Header: str
    Footer: str
    ProgressBarDisplay: str
    PartialData: str
    ValidationMessage: str | None
    PreviousButton: str
    NextButton: str
    SurveyTitle: str
    SkinLibrary: str
    SkinType: str 
    Skin: dict 
    NewScoring: int
    SurveyMetaDescription: str 
    CustomStyles: str
    QuestionsPerPage: str
    nextButtonLid: str
    nextButtonMid: str
    EOSMessage: str | None
    ShowExportTags: bool
    CollectGeoLocation: bool
    PasswordProtection: str # 'Yes' 'No'
    AnonymizeSurvey: str # 'Yes' 'No'
    RefererCheck: str  # 'Yes' 'No'
    UseCustomSurveyLinkCompletedMessage: str | None
    SurveyLinkCompletedMessage: str | None
    SurveyLinkCompletedMessageLibrary: str | None
    ResponseSummary: str 
    EOSMessageLibrary: str | None
    EOSRedirectURL: str | None
    EmailThankYou: bool
    ThankYouEmailMessageLibrary: str | None
    ThankYouEmailMessage: str | None
    ValidateMessage: bool
    ValidationMessageLibrary: str | None
    InactiveSurvey: str
    PartialDeletion: str | None
    PartilaDataCloseAfter: str
    InactiveMessageLibrary: str | None
    InactiveMesage: str | None
    AvailableLanguages: dict
    ProtectSelectionIds: bool


@dataclass(frozen=True)
class PreviewLinkElement:
    PreviewType: str
    PreviewID: str

    
@dataclass
class NoteElement:
    # should be pushed through with no edits, unless the element it's attached to (parent) is deleted?
    Notes: List[dict]
    UserStatuses: dict
    ParentID: str      # element id that the note is attached to
    ID: str

@dataclass
class FlowElement:
    Type: str
    FlowID: str
    Flow: List[dict]
    Properties: dict

@dataclass
class BlockElement(ABC):
    Type: str # Default, Trash, Standard
    SubType: str
    Description : str
    ID : str
    BlockElements: List[BlockElement]
    Options: dict


class BlockListElement(Element):
    def __init__(self, map):
        super().__init__()
        for (k, v) in map.items():
            self[k] = BlockElement(*v)


class SMQualtricsQuestion(Question):
    
    def __init__(self, obj: QuestionElement):
        qtype = QuestionElement.get_surveyman_qtype(obj)
        options = []
        if obj['QuestionType'] == 'MC':
            options = [Option(o['Display']) for o in obj['Choices'].values()]
        super().__init__(qtype, 
                         obj['QuestionText'],
                         options=options,
                         qID=obj['QuestionID'])


class SMQualtricsSurvey(surveys.Survey):

    def __init__(self, 
                 surveyEntry : dict, 
                 surveyElements : list):
        surveyEntry    = SurveyEntry(**surveyEntry)
        surveyElements = [SurveyElement(**elt) for elt in surveyElements]

        elements = defaultdict(list)
        for elt in surveyElements:
            p = elt.payload()
            elements[type(p).__name__].append((elt, p))

        for k, v in elements.items():
            print(k, len(v))

        assert len(elements[BlockListElement.__name__])  == 1
        assert len(elements[QuestionElement.__name__]) > 1

        blocklist      = SMQualtricsSurvey.extractBlocklist(
            [bl for (_, bl) in elements[BlockListElement.__name__]], 
            [qe for (_, qe) in elements[QuestionElement.__name__]], 
            surveyEntry.SurveyID)
        constraints    = SMQualtricsSurvey.extractConstraints(surveyElements)
        breakoff       = SMQualtricsSurvey.detectBreakoff(surveyElements)
        
        super().__init__(blocklist=blocklist, constraints=constraints, breakoff=breakoff, surveyID=surveyEntry.SurveyID)
        
        self.SurveyEntry = surveyEntry

    def extractBlocklist(blocks: List[BlockListElement],
                         questions: List[QuestionElement],
                         id: str) -> List[Block]:
        print(len(questions), questions[0], type(questions[0]), questions[0].__class__)
        questions = {q.QuestionID : SMQualtricsQuestion(q) for q in questions}
        
        exit(1)

        for blocklist in blocks:
            # is the default block always located at 0?
            for _, block in sorted(blocklist.items(), key= lambda tupe: tupe[0]):
                description = block.Description
                qs = []
                for obj in block.BlockElements:
                    qid = obj.QuestionID
                    qs.append(questions[qid])
                blocks.append(Block(qs, description=description, blockId=block.ID))
        
        return blocks
    
    def extractConstraints(surveyElements: dict) -> List[Constraint]:
        return []
    
    def detectBreakoff(surveyElements: dict) -> bool:
        return True


def parse(text:str = None, file:str = None) -> surveys.Survey:
    if file:
        with open(file, 'r') as f:
            jsobj = json.load(f)
    elif text:
        jsobj = json.loads(text)
    else:
        raise ValueError('Need one of text or file input')
    
    return SMQualtricsSurvey(*jsobj.values())
        