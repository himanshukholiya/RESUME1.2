import re
def extract_phone_numbers(string):
    phonelist = None
    r = re.compile(r'\d{10,12}|\d\d\d-\d\d\d-\d\d\d\d|\d\d\d\d\d \d\d\d\d\d|\d\d\d-\d\d-\d\d\d\d\d|\d\d\d\d\d-\d\d\d\d\d')
    phone_numbers = r.findall(string)
    phonelist = [re.sub(r'\D', '', number) for number in phone_numbers if number is not None]
    return phonelist
