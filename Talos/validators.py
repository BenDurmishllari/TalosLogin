import re

class EmailValidator:

    def checkEmail(self, email):
        checker = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        msg = ""
        if re.search(checker, email):
            msg = "Email is valid!"
        else:
            msg = "Email is not valid, please add a valid email!"

        return msg

class PasswordValidator:

    msg = ""
    def checkPassword(self, password):

        if len(password) < 6 or len(password) > 10:
            msg = "Password should be between 6 & 10 characters"
        elif not re.search("[a-z]", password):
            msg = "Password must have at least one lowercase"
        elif not re.search("[0-9]", password):
            msg = "Password must have at least one number"
        elif not re.search("[A-Z]", password):
            msg = "Password must have at least one upercase"
        elif not re.search("[#@<->,!?;$%^&*]", password):
            msg = "Password must have at least one symbol"
        else:
            msg = "Your password is Valid"
        
        return msg
       
        