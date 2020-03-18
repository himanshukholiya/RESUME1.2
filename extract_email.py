import re
def extract_email_addresses(text):
    r = re.compile(r'[a-zA-Z0-9_\.]+@[a-zA-Z-\.]*\.(com|edu|net|in|org|COM|EDU|NET|IN|ORG)')
    e_mail = r.finditer(text)
    for x in e_mail:
        return x.group(0)

# def extract_email_address(fulltext):
#     r = re.compile(r'[a-zA-Z0-9_\.]+@[a-zA-Z-\.]*\.(com|edu|net|in|org)')
#     e_mail = r.finditer(fulltext)
#     for x in e_mail:
#         return x.group(0)
