import csv
def extract_skills(resume_string):
    # resume_string1 = resume_string
    resume_string = resume_string.replace(',',' ')
    #Converting all the charachters in lower case
    resume_string = resume_string.lower()

    with open(r"C:\Users\HimanshuKholiya\Desktop\UI\skill.csv", 'rt') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        your_list = your_list[0]
        your_list = [word.lower() for word in your_list]

    #Sets are used as it has a a constant time for lookup hence the overall the time for the total code will not exceed O(n)
    s = set(your_list)

    list_matched = []
    for item in your_list:
        if item in resume_string:
            list_matched.append(item)

    return list_matched