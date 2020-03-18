import docx2txt

def extract_text_from_doc(path):
    temp = docx2txt.process(path)
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    text = ' '.join(text)
    text = text.lower()
    return text

