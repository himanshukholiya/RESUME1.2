import csv
import re

def extract_skills(resume_string):
    resume_string = resume_string.replace(',',' ')

    #Converting all the charachters in lower case
    
    resume_string= resume_string.lower()
    # resume_string = re.finditer(r'[a-zA-Z0-9 \.\/\++\@\(\)\]', resume_string)

    with open(r"C:\Users\HimanshuKholiya\Desktop\newUI\programmingskills.csv", 'rt') as f:
        reader = csv.reader(f)
        your_list1 = list(reader)
        your_list1 = set(your_list1[0])
        your_list1 = [word.lower() for word in your_list1]

    with open(r"C:\Users\HimanshuKholiya\Desktop\newUI\toolandsoftware.csv", 'rt') as f:
        reader = csv.reader(f)
        your_list2 = list(reader)
        your_list2 = set(your_list2[0])
        your_list2 = [word.lower() for word in your_list2] 

    your_list = your_list1+your_list2

    your_list = ' | '.join(your_list)
    your_list = your_list.replace(r"+",r"\+").replace(r".",r"\.").replace(r')',r"").replace(r'(',r"")
    mylist = []
    try:
        matched_list = re.finditer(your_list, resume_string)
        for match in matched_list:
            mylist.append(match.group())
        return list(set(mylist))
    except Exception as e:
        print(e)


