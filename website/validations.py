import re

from sqlalchemy import false

def email_validation(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def password_validation(password):
    if len(password) < 8:
        return False, "Your password should be at least 8 characters"
    elif not any(char.isdigit() for char in password):
        return False, "Your password should contain digits"
    elif not any(char.isupper() for char in password):
        return False, "Your password should contain capital letters"
    else:
        return (True, "success")

def name_validation(name):
    if name.isalpha():
        return True
    else:
        return False
    
    
def postalValidate(S):
    spaceless = S.replace(' ','')
    if not re.match(r"[a-zA-Z][0-9]+[a-zA-Z][0-9]+[a-zA-Z][0-9]+",spaceless):
       return False
    else :
        return True

def cardVAlidation(s):
    pattern = '^[45973][0-9]{15}|[45973][0-9]{3}-[0-9]{4}-[0-9]{4}-[0-9]{4}$'
    result = re.match(pattern, s)
    if result:
        return True
    else:
        return False