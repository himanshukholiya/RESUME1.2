import csv
import re
import spacy
import pandas as pd
import os

nlp = spacy.load('en_core_web_sm')

def extract_skills(nlp_text, noun_chunks):
    '''
    Helper function to extract skills from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param noun_chunks: noun chunks extracted from nlp text
    :return: list of skills extracted
    '''
    tokens = [token.text for token in nlp_text if not token.is_stop]

    data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'skills.csv')) 
    skills = list(data.columns.values)
    skillset = []
    # check for one-grams
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    # check for bi-grams and tri-grams
    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]

# def extract_skills(text):

#     data = pd.read_csv(os.path.join(os.path.dirname(__file__), 'skills.csv')) 
#     skills = list(data.columns.values)
#     skillset = []

#     # check for one-
#     # tokens = [token.text for token in text if not token.is_stop]
#     for skill in skills:
#         if skill in text:
#             skillset.append(skill)
#     return skillset


# def extract_skills(resume_string):    
#     resume_string = resume_string.replace(',',' ')

#     #Converting all the charachters in lower case
#     resume_string= resume_string.lower()

#     #reading all the possible values of a skill from a csv file
#     with open(r"C:\Users\KailashChandraOli\Desktop\talento\skills.csv", 'rt') as f:
#         reader = csv.reader(f)
#         your_list1 = list(reader)
#         your_list1 = set(your_list1[0])
#         your_list1 = [word.lower() for word in your_list1]

    # # with open(r"C:\Users\KailashChandraOli\Desktop\talento\toolandsoftware.csv", 'rt') as f:
    # #     reader = csv.reader(f)
    # #     your_list2 = list(reader)
    # #     your_list2 = set(your_list2[0])
    # #     your_list2 = [word.lower() for word in your_list2] 

    # your_list = your_list1 #+your_list2

    # #joining both the list with the separator '|'
    # # your_list = ''.join(your_list)
    # # your_list = your_list.replace(r"+",r"\+").replace(r".",r"\.").replace(r')',r"").replace(r'(',r"")
    # mylist = []

    #using regex to find the skills from the text
    # try:
    #     for item in your_list:
    #         matched_list = re.search(item.lower(), resume_string)
    #         if matched_list:
    #             mylist.append(matched_list.group())
    #     return mylist
    # except Exception as e:
    #     print(e)


