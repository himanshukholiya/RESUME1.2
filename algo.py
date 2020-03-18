from flask import Flask, render_template
from collections import Counter
from textblob import TextBlob
import io, nltk
from nltk.corpus import stopwords
stop = stopwords.words('english')
import nltk, os, subprocess, glob, sys, random
import PyPDF2, spacy
from spacy.matcher import Matcher
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
import extract_email as eemail
import phonenumber as pn
import skills 



# load pre-trained model
nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)

#txt = read_pdf(r'C:\Users\KailashChandraOli\Desktop\Project\Anushree hms.pdf')
# txt = read_pdf(r'C:\Users\TarunVashishth\Desktop\aditya bhartia.pdf')
    
class Parse():
    # List (of dictionaries) that will store all of the values
    # For processing purposes
    information=[]
    inputString = ''
    tokens = []
    lines = []
    sentences = []
    #path = r'C:\Users\TarunVashishth\Desktop\Language_Processing-master'

    def __init__(self, verose):
        print('Starting Programme')
        #fields = ["name", "address", "email", "phone", "mobile", "telephone","residence status","experience","degree","cainstitute","cayear","caline","b.cominstitute","b.comyear","b.comline","icwainstitue","icwayear","icwaline","m.cominstitute","m.comyear","m.comline","mbainstitute","mbayear","mbaline"]
        
        #Glob module matches certain patterns
        doc_files = glob.glob("Resume/*.doc")
        docx_files = glob.glob("Resume/*.docx")
        pdf_files = glob.glob("Resume/*.pdf")
        rtf_files = glob.glob("Resume/*.rtf")
        text_files = glob.glob("Resume/*.txt")

        files = set(doc_files + docx_files + pdf_files + rtf_files + text_files)

        files = list(files)
        # print(files)
        print ("{} files identified" .format(len(files)))
 
        for f in files:
            # info is a dictionary that stores all the data obtained from parsing
            info = {}
            extension = f.split(".")[-1]

            info['extension'] = extension 
            inputString =  self.readFile(f, extension)

            name = self.extract_name(inputString)
            phonenumbers = pn.extract_phone_numbers(inputString)
            if phonenumbers == []:
                phonenumber = 'NA'
            else:
                phonenumber = random.choice(phonenumbers)

            emails = eemail.extract_email_addresses(inputString)
            
            skill_set = skills.extract_skills(inputString)
            # experience = self.extract_experience(inputString)
            info = {'Name': name, 'Number':str(phonenumber), 'Mail':str(emails), 'Skills': skill_set}
            self.information.append(info)

    def readFile(self, fileName, extension):

        if extension == "txt":
            f = open(fileName, 'r')
            string = b'f.read()'
        
            f.close() 
            return string

        elif extension == "doc":
            return subprocess.Popen(['antiword', fileName], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

        # elif extension == "docx":
        #     try:
        #         print('hello')
        #         return convertDocxToText(fileName)
        #     except:
        #         return ''
        #         pass

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
        # codec = 'utf-8'
        # laparams = LAParams()

        #print("""ssss""" + TextConverter.__init__(rsrcmgr, retstr))
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

    



