import ujson as json
from .blocks import get_farthest_ancestor, NEXTBLOCK, NEXT
from . import IdGenerator
from .survey_exceptions import *
import dominate
import dominate.tags as tags
from typing import List, Tuple

__surveyGen__ = IdGenerator("s")


class Survey:
    """
    Contains the components of a survey:
    A survey is defined as a list of blocks and a list of branching constraints
    "breakoff" indicates whether the user can quit the survey early
    """

    def __init__(self, blocklist, constraints, breakoff=True, surveyID=None, name=None):
        """
        Creates a Survey object with a unique id.
        The block list and branch lists are required arguments
        The default value of "breakoff" is true

        :param blocklist: The top level list of blocks
        :param constraints: The associated constraints
        :param breakoff: Boolean value indicating the ability to submit results early
        """
        # generate ID
        self.surveyID = surveyID or __surveyGen__.generateID()
        self.name = name or ""

        # survey is a list of blocks, which hold questions and subblocks
        # at least one block with all the questions in it
        self.blockList = blocklist
        # list of branching constraints
        self.constraints = constraints
        self.hasBreakoff = breakoff

    def add_block(self, block):
        """
        Adds a top level block to the end of the survey's block list (assumed to be a top level block)

        :param block: The block to add
        """
        self.blockList.append(block)

    def add_block_by_index(self, block, index):
        """
        Adds a top level block to the desired index in the survey's block list.
        If the index is out of range, just inserts in the last position.

        :param block: The block to add to the top level of the survey
        :param index: The index at which the block should be added
        """
        self.blockList.insert(index, block)

    def validate(self):
        """
        Checks that the survey branching is valid before producing the JSON representation
        Confirms that:
        -all blocks follow either the branch-one, branch-all, or branch-none policy
        -all branch questions branch to top-level blocks in the survey's blocklist
        -all branches branch forward
        An exception is thrown if any of these conditions are violated
        """
        # check that all blocks are either branch none, branch one, or branch all
        # change so that it checks subblocks for branching also?
        for b in self.blockList:
            b.valid_branch_number()

        # check that all branches branch to top level blocks in the survey
        for c in self.constraints:
            for (_, block) in c.constraintMap:
                if block != NEXTBLOCK and block not in self.blockList:
                    raise InvalidBranchException(
                        "Branch target \n\t %s \n not found in the survey \n %s." % (block, self))

        # check that all branches branch forward
        for c in self.constraints:
            branch_question = c.question
            topmost_enclosing_block = get_farthest_ancestor(branch_question.block)
            for block in c.get_blocks():
                if topmost_enclosing_block not in self.blockList:
                    raise InvalidBranchException("Block %s not in survey block list." % topmost_enclosing_block)
                if block != NEXTBLOCK and self.blockList.index(topmost_enclosing_block) >= self.blockList.index(block):
                    raise InvalidBranchException("Question " + branch_question.qText + " does not branch forward")

    def __str__(self):
        # include some visualization of current branch/block structure?
        output = "Survey ID: " + self.surveyID + "\n"
        for b in self.blockList:
            output = output + str(b) + "\n"
        return output

    def jsonize(self):
        """
        Returns the JSON representation of the survey. This is validated against

        :return: JSON object according to the `Survey Schema <http://surveyman.github.io/Schemata/survey_input.json>`_
        """
        self.validate()
        __survey__      = "survey"
        __breakoff__    = "breakoff"
        __correlation__ = "correlation"
        __otherValues__ = "otherValues"

        output = {__survey__     : [json.loads(b.jsonize()) for b in self.blockList],
                  __breakoff__   : self.hasBreakoff,
                  __correlation__: {},
                  __otherValues__: {}}

        return json.dumps(output)
    
    
    def distribute(self, 
                   exclude_instructional=False, 
                   skipids=[],
                   replacements=[],
                   links:   List[Tuple[str, str]] = [], 
                   scripts: List[Tuple[str, str]] = []) -> tags.div:
        """Produces an html snippet for use in a distributable webpage for the purpose of sharing the survey instrument ahead of time with participants."""
        import re
        doc = dominate.document(title='Survey Preview')

        remaining_postext = []

        def parse(txt, tagstack=[]):
            m = re.match('(.*?)<(/?)(\w+)(\s+.*?)?\s*(/?)\s*>(.*)', txt)
            if m is None:
                return [txt]
            
            pretext, close, tag, attrs, nomatch, posttext = m.groups()
            remaining_postext.pop() if len(remaining_postext) > 0 else None
            remaining_postext.append(posttext)
            
            if nomatch:
                elts = parse(posttext, tagstack)
                return [pretext or '',
                        eval(f'tags.{tag}({attrs or ""})'),
                        *elts
                        ]
            if close:
                assert tag == tagstack[-1]
                return [pretext]
            
            else:
                inner = parse(posttext, tagstack=tagstack+[tag])
                elt = eval(f'tags.{tag}({attrs or ""})')
                for i in inner:
                    elt.add(i)
                return [pretext or '',
                        elt,
                        *parse(remaining_postext[0], tagstack=tagstack)
                        ]
                        
        def text_replace(txt, replacements):
            if replacements:
                return text_replace(txt.replace(*replacements[0]), replacements[1:])
            else: return txt

        with doc.head:
            for (rel, href) in links:
                tags.link(rel=rel, href=href)
            for (_type, src) in scripts:
                tags.script(type=_type, src=src)
            tags.meta(charset="UTF-8")
            # move this external
            tags.style("""body { background-color: yellow; }
                       .SMSurvey{
                       max-width:1024;
                       width:100%;
            }
                       .SMInstructions {
                       width:100%;
                       padding: 5pt 5pt 5pt 5pt;
                       font-size: 22pt;
                       font-family: sans-serif;
                       }
                       .SMBlock {
                       outline-style:solid;
                       outline-width:3pt;
                       padding: 2pt 2pt 2pt 2pt;
                       margin: 3pt 3pt 3pt 3pt;
                       background-color: white;
                       }
                       .SMBlock_description {
                        font-size: 20pt;
                        background: black;
                        color: white;
                        padding: 4pt 4pt 4pt 4pt;
                        margin: 0pt 0pt 2pt 0pt;
                       }
                       .SMQuestion {
                       font-size:14pt;
                       outline-style:solid;
                       outline-width:1pt;
                        padding: 2pt 2pt 2pt 2pt;
                       margin: 3pt 3pt 3pt 3pt;

                       }
                       .SMOption {
                       font-size:12pt;
                       }

                       .oneof {
                         list-style-type: '⚬';
                            padding-inline-start: 1cm;
                       }

                    .likert {
                         list-style-type: '⚬';
                            padding-inline-start: 1cm;
                       }

                    .checkbox {
                        list-style-type: '☐';
                        padding-inline-start: 1cm;
                       }

                    }

                       """)
            tags.script(r"""
function section_onclick(bid) {
    var view = document.getElementById("view_" + bid);
    var ques = document.getElementById("ques_"+bid);
                        
    toggle_map = {'none': 'block', 'block' : 'none'};
    button_map = {'View questions' : 'Hide questions', 'Hide questions' : 'View questions'};
    view.textContent = button_map[view.textContent];
    ques.style.display = toggle_map[ques.style.display];                       
}
function options_onclick(qid) {
    var view = document.getElementById("view_" + qid);
    var opts = document.getElementById("opts_" + qid);
                        
    toggle_map = {'none': 'block', 'block' : 'none'};
    button_map = {'View options' : 'Hide options', 'Hide options' : 'View options'};
    view.textContent = button_map[view.textContent];
    opts.style.display = toggle_map[opts.style.display];
}""")
        
        with doc.body:
            with tags.div(_id='instructions', _class='SMInstructions'):
                tags.p(f'This is an HTML preview of the content of the {self.name} survey.')
                tags.p('This document is meant to give the survey-taker a sense of the nature of the questions and potential flows through the survey.')
                tags.p('The questions you see, the wording, and the formatting may all differ from your actual experience.')
            with tags.div(_id=self.surveyID, _class='SMSurvey'):
                # flatten top-level blocks
                for block in self.blockList:
                    if block.blockId in skipids: continue
                    with tags.div(id=block.blockId, cls='SMBlock'):
                        with tags.div(id=f'desc_{block.blockId}', cls='SMBlock_description') as descbar:
                            if block.description:
                                descbar.add(text_replace(block.description, replacements))
                            # tags.button("View questions", 
                            #         style='display:block;background-color:lightgray;', 
                            #         id=f'view_{block.blockId}', 
                            #         cls='SMBLock_description',
                            #         _onclick=f'block_onclick("{block.blockId.strip()}")')
                        with tags.div(id=f'ques_{block.blockId}'):#, style='display:none;'):
                            for question in block.get_questions():
                                if question.qId in skipids: continue
                                content = [c for c in parse(text_replace(question.qText, replacements)) if c]
                                with tags.div(id=question.qId, cls='SMQuestion') as qelements:
                                    qelements.add(*content)
                                    if question.qType == 'freetext':
                                        qelements.add(tags.br())
                                        qelements.add(tags.textarea(_readonly=True, style='resize:none;'))
                                    if question.qType in ['oneof', 'likert', 'checkbox']:
                                        qelements.add(tags.button("View options", 
                                                                    style='display:block;color:white;background-color:darkgray;', 
                                                                    id=f'view_{question.qId}', 
                                                                   _onclick=f'options_onclick("{question.qId.strip()}")'))
                                        qelements.add(tags.ul(
                                            *[tags.li(text_replace(o.opText, replacements)) for o in question.options],
                                            id=f'opts_{question.qId}',
                                            cls=f'SMOption {question.qType}',
                                            style='display:none;'
                                            ))
        
        return doc
    
