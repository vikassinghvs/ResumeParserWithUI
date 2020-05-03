from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import re
#import docx2txt
import spacy
from spacy.matcher import Matcher
import io

file_path="/Users/vikassingh/Desktop/2020/upWork/python/res/uploads/Resume.pdf"

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as fh:
        # iterate over all pages of PDF document
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            # creating a resoure manager
            resource_manager = PDFResourceManager()
            
            # create a file handle
            fake_file_handle = io.StringIO()
            
            # creating a text converter object
            converter = TextConverter(
                                resource_manager, 
                                fake_file_handle, 
                                codec='utf-8', 
                                laparams=LAParams()
                        )

            # creating a page interpreter
            page_interpreter = PDFPageInterpreter(
                                resource_manager, 
                                converter
                            )

            # process current page
            page_interpreter.process_page(page)
            
            # extract text
            text = fake_file_handle.getvalue()
            yield text

            # close open handles
            converter.close()
            fake_file_handle.close()

# calling above function and extracting text
'''for page in extract_text_from_pdf(file_path):
    text += ' ' + page'''


'''def extract_text_from_doc(doc_path):
    temp = docx2txt.process("resumes/Chinmaya_Kaundanya_Resume.docx")
    text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    return ' '.join(text)'''




# load pre-trained model
'''nlp = spacy.load('en_core_web_sm')

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)'''

def extract_name(resume_text):
    nlp = spacy.load('en_core_web_sm')
    matcher = Matcher(nlp.vocab)
    nlp_text = nlp(resume_text)
    # First name and Last name are always Proper Nouns
    '''pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
    matcher.add('NAME', None, *pattern)
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text'''
    
    name = ""
    for i in range(len(nlp_text)):
        if re.search("NAME*",nlp_text[i].text.upper()):
            name=nlp_text[i+1]
    if name != "":
        return name
    else:
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
        matcher.add("NAME", None , pattern)
        matches = matcher (nlp_text)
        for match_id, start, end in matches:
            name = nlp_text[start:end]
            break
    return name.text    
        




def extract_mobile_number(text):
    phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), text)
    
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return '+' + number
        else:
            return number

def extract_email(email):
    email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", email)
    if email:
        try:
            return email[0].split()[0].strip(';')
        except IndexError:
            return None

if __name__ == "__main__":
    file_path="/Users/vikassingh/Desktop/2020/upWork/python/res/uploads/Resume.pdf"
    text = ''
    for page in extract_text_from_pdf(file_path):
        text += ' ' + page
    # load pre-trained model
    '''nlp = spacy.load('en_core_web_sm')

    # initialize matcher with a vocab
    matcher = Matcher(nlp.vocab)'''
    name = extract_name(text)
    emailV = extract_email(text)
    contact = extract_mobile_number(text)
    print("Name: "+ str(name))
    print("<br>Email: "+ str(emailV))
    print("<br> Contact Details: "+str(contact))


    

