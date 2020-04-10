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

    def __init__(self, verose):

        #Glob module matches certain patterns
        docx_files = glob.glob("Resume/*.docx")
        pdf_files = glob.glob("Resume/*.pdf")


        files = set(docx_files + pdf_files)
        skillcount = 0;

        files = list(files)
        i=1;
 
        for f in files:
            print(i)
            i+=1
            # info is a dictionary that stores all the data obtained from parsing
            info = {}
            extension = f.split(".")[-1]

            # info['extension'] = extension 
            inputString =  self.readFile(f, extension)
            inputString = inputString.lower()
            
            __nlp = nlp(inputString)
            __noun_chunks = list(__nlp.noun_chunks)

            # fetching person name
            # name = self.extract_name(inputString)


            # fetching phone number
            phonenumbers = pn.extract_phone_numbers(inputString)
            if phonenumbers == []:
                phonenumber = 'NA'
            else:
                phonenumber = random.choice(phonenumbers)
            # print(phonenumber)
            # info['Phone Number'] = phonenumber


            #fetching mail 
            mail = eemail.extract_email_addresses(inputString)
            # print(mail)
            if mail is None or len(mail) < 0:
                info['mail id'] = 'NA'
            else:
                info['mail id'] = mail


            #fetching skills of person
            skillset = sk.extract_skills(__nlp,__noun_chunks)
            # skillset = sk.extract_skills(inputString)
            if skillset == [] or skillset ==0 or skillset is None:
                skill_set = 'NA'
                skillcount = 0
            else:
                skill_set = skillset
                skillcount = len(skillset)
            # print(skill_set)
            info['Skills']= skill_set
            # info['Skill Count'] = skillcount 


            #fetching experience of person
            experiences = nexp.extract_experience(inputString)
            
            if experiences == [] or experiences == 0:
                experience = 'Fresher'
                # print(experience)
            else:
                experience = experiences.split(' ')
                experience = experience[0]
                # print(experience)
            info['Experience']= experience
            
            print('\n')

            # info['Name'] = name
            self.information.append(info)


    def readFile(self, fileName, extension):
        if extension == "docx":
            try:
                print(fileName)
                filetext = ed.extract_text_from_doc(fileName)
                filetext = filetext.replace('\t',' ')
                filetext = filetext.replace('  ',' ').replace('      ',' ').replace('   ',' ').replace('   ',' ')
                return filetext
            except:
                return ''
                pass

        elif extension == "pdf":
            try:
                print(fileName)
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
    

    # def extract_name(self, resume_text):
    #     nlp_text = nlp(resume_text)

    #     # First name and Last name are always Proper Nouns
    #     pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    #     matcher.add('NAME', [pattern])
        
    #     matches = matcher(nlp_text)
    #     for match_id, start, end in matches:
    #         span = nlp_text[start:end]
    #         return span.text



verose = False
if "-v" in str(sys.argv):
    verose = True
p = Parse(verose)
print(p.information)

key = input('Enter your required Skills')
index_of_dict_in_list= []
data = p.information
for dict in data:
    skill_list = dict.get('Skills')
    if key in skill_list:
        index_of_dict_in_list.append(data.index(dict))

# print(index_of_dict_in_list)

for index in index_of_dict_in_list:
    print(data[index])
df = pd.DataFrame(data)
df.to_csv('data1.csv')
#print('done')
