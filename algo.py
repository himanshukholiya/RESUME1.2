from flask import Flask, render_template
from collections import Counter
from textblob import TextBlob
import io, nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')
import nltk, os, subprocess, glob, sys, random
import PyPDF2, spacy, pandas as pd
from spacy.matcher import Matcher
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
import extract_email as eemail
import phonenumber as pn
import extractdocx as ed
import nexp
import skills as sk



# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)
    
class Parse():

    information=[]
    inputString = ''
    tokens = []
    lines = []
    sentences = []

    def __init__(self, verose):

        #Glob module matches certain patterns
        doc_files = glob.glob("Resume/*.doc")
        docx_files = glob.glob("Resume/*.docx")
        pdf_files = glob.glob("Resume/*.pdf")


        files = set(doc_files + docx_files + pdf_files + rtf_files + text_files)

        files = list(files)
 
        for f in files:
            # info is a dictionary that stores all the data obtained from parsing
            info = {}
            extension = f.split(".")[-1]

            info['extension'] = extension 
            inputString =  self.readFile(f, extension)

            # fetching person name
            name = self.extract_name(inputString)

            # fetching phone number
            phonenumbers = pn.extract_phone_numbers(inputString)
            if phonenumbers == []:
                phonenumber = 'NA'
            else:
                phonenumber = random.choice(phonenumbers)
            # print(phonenumber)

            #fetching mail 
            mail = eemail.extract_email_addresses(inputString)
            # print(mail)

            #fetching skills of person
            skillset = sk.extract_skills(inputString)
            if skillset == []:
                skill_set = 'NA'
            else:
                skill_set = skillset
                skillcount = len(skill_set)
            # print(skill_set)

            #fetching experience of person
            experiences = nexp.extract_experience(filetext)
            if experiences == []:
                experience = 'NA'
            else:
                experience = experiences
                experience = experience.split(' ')
                experience = experience[0]


            # experience = self.extract_experience(inputString)
            info['Name'] = name

            info['Phone Number'] = phonenumber

            if len(mail) > 0:
                info['mail id'] = emails
            else:
                info['mail id'] = 'NA'

            info['Experience']= experience

            info['Skill Count'] = skillcount            

            info['Skills']= skill_set

            self.information.append(info)


    def readFile(self, fileName, extension):

        if extension == "docx":
            try:
                filetext = ed.extract_text_from_doc(f)
                filetext = filetext.replace('\t',' ')
                filetext = filetext.replace('  ',' ').replace('      ',' ').replace('   ',' ').replace('   ',' ')
                return filetext

            except:
                return ''
                pass

        elif extension == "pdf":
            print("read pdf")
            try:
                text = self.read_pdf(fileName)
                return text
            except:
                return ''
                pass
                
        else:
            print ('Unsupported format')
            return ''
    
    def read_pdf(self, path):
       
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()

        device = TextConverter(rsrcmgr, retstr)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True): 
            interpreter.process_page(page)
        text = retstr.getvalue()
        text = " ".join(text.replace(u"\xa0", " ").strip().split())
        text = text.replace('\uf0b7','').lower()
        fp.close()
        device.close()
        retstr.close()
        return text
    
    def extract_name(self, resume_text):
        nlp_text = nlp(resume_text)

        # First name and Last name are always Proper Nouns
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
        matcher.add('NAME', [pattern])
        
        matches = matcher(nlp_text)
        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text

    



