"""Utility to parse Qualtrics Survey Format (.qsf) files into SurveyMan objects."""

import ujson as json
from ..survey import surveys
from ..survey.blocks import Block
from ..survey.questions import Question
from ..survey.constraints import Constraint
from ..survey.options import Option
from dataclasses import dataclass, field
from datetime import date
from typing import List, Dict, Optional
from collections import defaultdict
import re

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

@dataclass
class SurveyElement:
    """Core objects and logic in a Qualtrics Survey"""
    SurveyID: str
    Element: str
    PrimaryAttribute: str
    SecondaryAttribute: str | None
    TertiaryAttribute: str | None
    Payload: dict | list | None


def parse_payload(elt: SurveyElement):
    codes = {
        'BL'  : lambda payload : BlockListElement(payload),
        'FL'  : lambda payload : FlowElement(**payload),
        'NT'  : lambda payload : NoteElement(**payload), 
        'PL'  : lambda payload : PreviewLinkElement(**payload), 
        'RS'  : lambda payload : None, 
        'SO'  : lambda payload : SurveyOptionsElement(**payload), 
        'QGO' : lambda payload : QuotaGroupOrder(zip(range(len(payload)), payload)),
        'SCO' : lambda payload : ScoringCategoriesElement(**payload), 
        'PROJ': lambda payload : ProjectCategoryElement(**payload), 
        'STAT': lambda payload : SurveyStatisticsElement(**payload), 
        'QC'  : lambda payload : None, 
        'SQ'  : lambda payload : QuestionElement(**payload),
        'QG'  : lambda payload : QuotaGroupElement(**payload)
    }
    return codes[elt.Element](elt.Payload)
        
    # elif type(elt.Payload) is list:
    #     clz, keys = codes[elt.Element]
    #     return clz(zip(keys, elt.Payload))
    # else: 
    #     return codes[elt.Element]()

class RSElement: pass


@dataclass(kw_only=True)
class QuestionElement:
    Configuration: dict #= field(default_factory=dict)
    DataExportTag: str # appears to the column label used in response data
    DefaultChoices: bool
    GradingData: list
    Language: str
    NextAnswerId: int 
    NextChoiceId: int
    QuestionDescription : str # the actual question text
    QuestionID: str # should match the PrimaryAttribute value of the SurveyElement object
    QuestionText: str
    QuestionType: str 
    Selector: str 
    Validation: dict
    ChoiceDataExportTags : Optional[dict] = None
    Choices: Optional[Dict[StrInt, Dict]] = field(default_factory=dict) # map from string ints to another map with the keys 'Display' for display text and 'TextEntry' bool
    ChoiceOrder: Optional[List[StrInt]] = field(default_factory=list)
    DataVisibility: Optional[dict] = field(default_factory=lambda : {'Private': False, 'Hidden': False})
    DisplayLogic: Optional[dict] = field(default_factory=dict) # encodes branching?
    DynamicChoices : Optional[dict] = None
    DynamicChoicesData : Optional[dict] = None
    QuestionJS : Optional[str] = None
    QuestionText_Unsafe : Optional[str] = None
    Randomization: Optional[dict] = None
    SearchSource : Optional[str] = None
    SubSelector : Optional[str] = None
    Answers : Optional[dict] = None
    AnswerOrder : Optional[dict] = None

def get_surveyman_qtype(self : QuestionElement) -> str:
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
class QuotaGroupElement:
    ID: str
    Name: str
    Selected: bool
    MultipleMatch: str
    Public: bool
    Quotas: list
    DynamicChoicesData : Optional[dict] = None

@dataclass(frozen=True)
class SurveyStatisticsElement:
    MobileCompatible: bool # note: this was converted into a python bool, not a string bool like the others
    ID: str 

@dataclass
class ScoringCategoriesElement:
    ScoringCategories: list
    ScoringCategoryGroups: list
    ScoringSummaryCategory: str | None
    ScoringSummaryAfterQuestions: int
    ScoringSummaryAfterSurvey: int 
    DefaultScoringCategory: str | None 
    AutoScoringCategory: str | None


@dataclass(frozen=True)
class ProjectCategoryElement:
    ProjectCategory: str 
    SchemaVersion: str

class QuotaGroupOrder(dict): pass

@dataclass
class SurveyOptionsElement:
    AvailableLanguages: dict
    BackButton: bool # need to double check that this won't cause problems when converting between Python and Qualtrics/JSON
    BallotBoxStuffingPrevention : bool
    CollectGeoLocation: bool
    CustomStyles: str
    EmailThankYou: bool
    EOSMessage: str | None
    EOSMessageLibrary: str | None
    EOSRedirectURL: str | None
    Footer: str
    Header: str
    InactiveMessage : str
    InactiveMessageLibrary: str | None
    InactiveSurvey: str
    NewScoring: int
    NextButton: str
    nextButtonLid: str
    nextButtonMid: str
    NoIndex: str # no idea; in example, 'Yes'
    PartialData: str
    PasswordProtection: str # 'Yes' 'No'
    PartialDataCloseAfter : str
    PartialDeletion: str | None
    PreviousButton: str
    ProgressBarDisplay: str
    ProtectSelectionIds: bool
    QuestionsPerPage: str
    RefererCheck: str  # 'Yes' 'No'
    ResponseSummary: str 
    SaveAndContinue: bool # Not sure
    SecureResponseFiles: bool # no idea
    ShowExportTags: bool
    Skin: dict 
    SkinLibrary: str
    SkinType: str 
    SurveyExpiration: date | None
    SurveyLinkCompletedMessage: str | None
    SurveyLinkCompletedMessageLibrary: str | None
    SurveyMetaDescription: str 
    SurveyName : str
    SurveyProtection: str # byInvitation
    SurveyTermination: str
    SurveyTitle: str
    ThankYouEmailMessage: str | None
    ThankYouEmailMessageLibrary: str | None
    UseCustomSurveyLinkCompletedMessage: str | None
    ValidateMessage: bool
    ValidationMessage: str | None
    ValidationMessageLibrary: str | None
    AnonymizeResponse : bool
    AnonymizeSurvey: Optional[str] = None # 'Yes' 'No'
    

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
class FlowData:
    Type : str # 'Standard'
    ID : str # id of flow element?
    FlowID : str
    Autofill : list

@dataclass
class FlowElement:
    Type: str # 'Root'
    FlowID: str
    Flow: List[FlowData] = field(default_factory=lambda _ : [])
    Properties: dict = field(default_factory=lambda : {'Count' : 0, 'RemovedFieldsets' : []})

    def __post_init__(self):
        flows = [FlowData(**fd) for fd in self.Flow]
        self.Flow = flows

@dataclass
class SkipLogicCode:
    ChoiceLocator: str #url
    Condition: str
    Locator : str
    SkipLogicId: str 
    SkipToDescription : str
    SkipToDestination: str

    def __post_init__(self): 
        assert self.Condition in ['Selected']
        assert self.SkipToDestination in ['ENDOFBLOCK']
        assert self.Locator == self.ChoiceLocator
    
    def get_skip_from(self, survey: surveys.Survey) -> Option:
        qid, index = re.match('q://(.*?)/SelectableChoice/(\d+)', self.ChoiceLocator)
        print(f'Skip from question {qid}, option index{index}')
        # need to add facility to get get question from the survey by id

    

@dataclass
class BlockElementType:
    Type : str
    QuestionID : Optional[str] = None
    SkipLogic : Optional[List[SkipLogicCode]] = field(default_factory=list)

    def __post_init__(self):
        assert self.Type in ['Question', 'Page Break'], self.Type

@dataclass
class BlockElement:
    Type: str # Default, Trash, Standard
    Description : str
    ID : str
    BlockElements: List[BlockElementType]
    Options: Optional[dict] = field(default_factory=dict)
    SubType: Optional[str] = None

    def __post_init__(self):
        print(self.BlockElements)
        elttypes = [BlockElementType(**e) for e in self.BlockElements]
        self.BlockElements = elttypes

class BlockListElement(dict):
    def __init__(self, map):
        super().__init__()
        for (k, v) in map.items():
            try:
                self[k] = BlockElement(**v)
            except Exception as e:
                print(v.keys())
                raise e
            
    def __iter__(self):
        return iter([v for _, v in sorted(self.items(), key = lambda t : t[0])])


class SMQualtricsQuestion(Question):
    
    def __init__(self, obj: QuestionElement):
        qtype = get_surveyman_qtype(obj)
        options = []
        if obj.QuestionType == 'MC':
            options = [Option(o['Display']) for o in obj.Choices.values()]
        super().__init__(qtype, 
                         obj.QuestionText,
                         options=options,
                         qID=obj.QuestionID)


class SMQualtricsSurvey(surveys.Survey):

    def __init__(self, 
                 surveyEntry : dict, 
                 surveyElements : list):
        surveyEntry    = SurveyEntry(**surveyEntry)
        surveyElements = [SurveyElement(**elt) for elt in surveyElements]

        elements = defaultdict(list)
        for elt in surveyElements:
            p = parse_payload(elt)
            elements[type(p).__name__].append((elt, p))

        assert len(elements[BlockListElement.__name__])  == 1
        assert len(elements[QuestionElement.__name__]) > 1

        blocks    = [bl for (_, bl) in elements[BlockListElement.__name__]]
        questions = [qe for (_, qe) in elements[QuestionElement.__name__]]
        flows     = [fe for (_, fe) in elements[FlowElement.__name__]]

        blocklist      = SMQualtricsSurvey.extractBlocklist(blocks, questions, surveyEntry.SurveyID)
        constraints    = SMQualtricsSurvey.extractConstraints(blocklist, flows)
        breakoff       = SMQualtricsSurvey.detectBreakoff(surveyElements)
        
        super().__init__(blocklist=blocklist, constraints=constraints, breakoff=breakoff, surveyID=surveyEntry.SurveyID)
        
        self.SurveyEntry = surveyEntry

    def extractBlocklist(blocklists: List[BlockListElement],
                         questions: List[QuestionElement],
                         id: str
                         ) -> List[Block]:
        print(len(questions), questions[0], type(questions[0]), questions[0].__class__)
        questions = {q.QuestionID : SMQualtricsQuestion(q) for q in questions}
        
        blocks = []
        for blocklist in blocklists:
            # is the default block always located at 0?
            for block in blocklist:
                description = block.Description
                qs = []
                for obj in block.BlockElements:
                    if obj.QuestionID:
                        qs.append(questions[obj.QuestionID])
                blocks.append(Block(qs, description=description, blockId=block.ID))
        
        return blocks
    
    def extractConstraints(blocklist: List[Block],
                           flows: List[FlowElement]
                           ) -> List[Constraint]:
        def get_root():
            roots = [f for f in flows if f.Type == 'Root']
            assert len(roots) == 1
            return roots[0]
        root = get_root()
        assert len(flows) == 1 # So far I've only seen one top-level flow
        blockmap = {b.blockId : b for b in blocklist}
        blocklist.clear()
        for flow in root.Flow:
            # So far I've only seen flow ids be block ids
            # maybe we can just sort the block list by order in flow?
            blocklist.append(blockmap[flow.ID])

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
        