import re
import io
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
# from datetime import datetime
# from datetime import date,timedelta
# from datetime import datetime 
# from dateutil.relativedelta import relativedelta

experience2=[]

def extract_experience(text):
    resume_string = re.findall(r'[a-zA-Z0-9 @.%,\/\'\:\\]',text)
    resume_string = ''.join(resume_string)
    indexlist = []
    found = False
    lines = [el.strip() for el in resume_string.split("\n") if len(el) > 0] # Splitting on the basis of newlines 
    lines = [sent_tokenize(el) for el in lines]                         # Tokenize the individual lines
    lines = lines[0]


    for line in lines:
        if 'experience' in line or 'exposure' in line:
            if 'years' in line or 'year' in line or 'Year' in line or 'Years' in line:
                indexlist.append(lines.index(line))
                found = True

    if found == True:
        experience = extract_year(indexlist, lines)
        maxval = sorted(experience, key = lambda item: (int(item.partition(' ')[0]) if item[0].isdigit() else float('inf'),item));
        if maxval[-1]!= ' year':
            return maxval[-1]
        else:
            return maxval[-2]
    else:
        return 0
    


    # elif found == False and flag ==1:
    #     experience_2 = extract_yeardate(lines)
    #     print(experience_2)
    #     flag = 0
    #     return 0

    # if all!=[]:
    # all.sort(key = lambda date: datetime.strptime(date, '%b %Y'))
    # start_date = datetime.strptime("01 {0}".format(all[0]), "%d %b %Y")
    # today_date = date.today()
    # experience = relativedelta(today_date, start_date)
    # exp = experience
    # found = True
    # maxval = (exp.years)

def extract_year(selectline, mystringarr):
    experience1 =[]
    for i in selectline:
        pattern = re.finditer(r'([\d+][\.\d+]?[+]?)?(one|two|three|four|five|six|seven|eight|nine|ten|yrs)?\s(?:years|year|Years|Year|yrs|Yrs)',mystringarr[i])
        for m in pattern:
            experience1.append(m.group())
    return experience1
    

# def extract_yeardate(myline):
#         all = re.findall(r"(?:jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)( |')d{2,4}( to | - |-)(?:till date|jan(uary)?|feb(ruary)?|mar(ch)?|apr(il)?|may|jun(e)?|jul(y)?|aug(ust)?|sep(tember)?|oct(ober)?|nov(ember)?|dec(ember)?)( |')\d{2,4}", myline)
#         for item in all:
#             experience2.append(item.group())
#         return experience2


