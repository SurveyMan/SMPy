# -*- coding: cp1252 -*-
#example survey based on https://github.com/etosch/SurveyMan/blob/master/data/Ipierotis.csv
#outputs JSON representation

from surveyman.survey.surveys import *
from surveyman.survey.blocks import *
from surveyman.survey.constraints import *



def create_survey():
    
    oneof = "oneof"
    
    #question 1
    q1 = Question(oneof, "What is your gender?", [])
    q1.add_option("Male")
    q1.add_option("Female")
    q1.add_option("Other")
    #print q1
    #question 2
    q2 = Question(oneof, "What is your year of birth?", [Option(str(x)) for x in range(1950, 1996)])
    #print q2
    #question 3
    q3 = Question(oneof, "Which of the following best describes your highest achieved education level?", [])
    q3.add_option("Some High School")
    q3.add_option("High School Graduate")
    q3.add_option("Some College, no Degree")
    q3.add_option("Associates Degree")
    q3.add_option("Bachelors Degree")
    q3.add_option("Graduate Degree, Masters")
    q3.add_option("Graduate Degree, Doctorate")
    #print q3
    #question 4
    q4 = Question(oneof, "What is the total income of your household?", [])
    q4.add_option("Less than $10,000")
    q4.add_option("$10,000 - $14,999")
    q4.add_option("$15,000 - $24,999")
    q4.add_option("$25,000 - $39,499")
    q4.add_option("$40,500 - $59,999")
    q4.add_option("$60,000 - $74,999")
    q4.add_option("$75,000 - $99,999")
    q4.add_option("$100,000 - $149,999")
    q4.add_option("More than $150,000")
    #print q4
    #question 5
    q5 = Question(oneof, "What is your marital status?", [])
    q5.add_option("Cohabitating")
    q5.add_option("Divorced")
    q5.add_option("Engaged")
    q5.add_option("Married")
    q5.add_option("Separated")
    q5.add_option("Single")
    q5.add_option("Widowed")
    #print q5
    #question 6
    q6 = Question(oneof, "Do you have children?", [])
    q6.add_option("No children")
    q6.add_option("Yes, 1 child")
    q6.add_option("Yes, 2 children")
    q6.add_option("Yes, 3 children")
    q6.add_option("Yes, 4 children")
    #print q6
    #question 7
    q7 = Question(oneof, "How many members in your household?", [Option(str(x)) for x in range(1, 4)])
    #print q7
    #question 8
    q8 = Question(oneof, "In which country do you live?", [])
    q8.add_option("United States")
    q8.add_option("India")
    q8.add_option("Other")
    #print q8
    #question 9
    q9 = Question(oneof, "Please indicate your race.", [])
    q9.add_option("American Indian or Alaska Native")
    q9.add_option("Asian")
    q9.add_option("Black Latino")
    q9.add_option("Black or African American")
    q9.add_option("Native Hawaiian or Other Pacific Islander")
    q9.add_option("White Latino")
    q9.add_option("White")
    q9.add_option("2 or more races")
    q9.add_option("Unknown")
    #print q9
    #question 10
    q10 = Question(oneof, "Why do you complete tasks in Mechanical Turk? Please check any of the following that applies:", [])
    q10.add_option("Fruitful way to spend free time and get some cash (e.g., instead of watching TV).")
    q10.add_option("For primary income purposes (e.g., gas, bills, groceries, credit cards).")
    q10.add_option("For secondary income purposes, pocket change (for hobbies, gadgets, going out).")
    q10.add_option("To kill time.")
    q10.add_option("I find the tasks to be fun.")
    q10.add_option("I am currently unemployed, or have only a part time job.")
    #question 11
    q11 = Question(oneof, "Has the recession affected your decision to participate on MTurk?", [])
    q11.add_option("Yes")
    q11.add_option("No")
    #question 12
    q12 = Question(oneof, "Has the recession affected your level of participation on MTurk?", [])
    q12.add_option("Yes")
    q12.add_option("No")
    #question 13
    q13 = Question(oneof, "For how long have you been working on Amazon Mechanical Turk?", [])
    q13.add_option("< 6 mos.")
    q13.add_option("6mos-1yr")
    q13.add_option("1-2yrs")
    q13.add_option("2-3yrs")
    q13.add_option("3-5yrs")
    q13.add_option("5-7yrs")
    q13.add_option("7-9yrs")
    q13.add_option("9-15yrs")
    q13.add_option("15+")
    #question 14
    q14 = Question(oneof, "How much do you earn per week on Mechanical Turk?", [])
    q14.add_option("Less than $1 per week")
    q14.add_option("$1-$5 per week.")
    q14.add_option("$5-$10 per week.")
    q14.add_option("$10-$20 per week.")
    q14.add_option("$20-$50 per week.")
    q14.add_option("$50-$100 per week.")
    q14.add_option("$100-$200 per week.")
    q14.add_option("$200-$500 per week.")
    q14.add_option("More than $500 per week.")
    #question 15
    q15 = Question(oneof, "How much time do you spend per week on Mechanical Turk?", [])
    q15.add_option("Less than 1 hour per week.")
    q15.add_option("1-2 hours per week.")
    q15.add_option("2-4 hours per week.")
    q15.add_option("4-8 hours per week.")
    q15.add_option("8-20 hours per week.")
    q15.add_option("20-40 hours per week.")
    q15.add_option("More than 40 hours per week.")
    #question 16
    q16 = Question(oneof, "How many HITs do you complete per week on Mechanical Turk?", [])
    q16.add_option("Less than 1 HIT per week.")
    q16.add_option("1-5 HITs per week.")
    q16.add_option("5-10 HITs per week.")
    q15.add_option("10-20 HITs per week.")
    q16.add_option("20-50 HITs per week.")
    q16.add_option("50-100 HITs per week.")
    q16.add_option("100-200 HITs per week.")
    q16.add_option("200-500 HITs per week.")
    q16.add_option("500-1000 HITs per week.")
    q16.add_option("1000-5000 HITs per week.")
    q16.add_option("More than 5000 HITs per week.")

    q17 = Question(oneof, "In which state do you live?", [])
    q17.add_option("Massachusetts")
    q17.add_option("some other state (too many to list)")

    block1 = Block([q1, q2, q3, q4, q5, q6, q7, q8, q9])
    block2 = Block([q17])
    block3 = Block([q10, q11, q12, q13, q14, q15, q16])

    branch1 = Constraint(q8)
    branch1.add_branch_by_index(0, block2)
    branch1.add_branch_by_index(1, block3)
    branch1.add_branch_by_index(2, block3)
    #print str(branch1)
    
    survey = Survey([block1, block2, block3], [branch1])

##    jsonfile = open("survey1.json", "wb")
##    jsonfile.write(survey.jsonize())
##    jsonfile.close()

    return survey