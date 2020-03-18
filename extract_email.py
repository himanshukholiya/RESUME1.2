import re
def extract_email_addresses(string):
    r = re.compile(r'[a-zA-Z0-9_\.+%]+@[a-zA-Z0-9_\.]*\.(com|edu|net|in|org)')    
    e_mail = r.finditer(string)
    for x in e_mail:
        return x.group(0)