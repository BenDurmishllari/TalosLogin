from password_strength import PasswordStats
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
        results = []
        if len(password) < 6:
            msg = "Password should be at least 6 characters"
            passwordStrongLevel = PasswordStats(password)
            results.append(msg)
            results.append(passwordStrongLevel)
        elif not re.search("[a-z]", password):
            msg = "Add at least one lowecase for stronger password"
            passwordStrongLevel = PasswordStats(password)
            results.append(msg)
            results.append(passwordStrongLevel)
        elif not re.search("[0-9]", password):
            msg = "Add at least one number for stronger password"
            passwordStrongLevel = PasswordStats(password)
            results.append(msg)
            results.append(passwordStrongLevel)
        elif not re.search("[A-Z]", password):
            msg = "Add at least one upercase for stronger password"
            passwordStrongLevel = PasswordStats(password)
            results.append(msg)
            results.append(passwordStrongLevel)
        elif not re.search("[#@<>_,!?;$%^&*]", password):
            msg = "Add at least one symbol for stronger password"
            passwordStrongLevel = PasswordStats(password)
            results.append(msg)
            results.append(passwordStrongLevel)
        else:
            msg = "Your password is Valid"
            passwordStrongLevel = PasswordStats(password)
            results.append(msg)
            results.append(passwordStrongLevel)
            
        return results

class PasswordStronLevelValidator:
    
    msg = ""
    def checkStrongLevelPassword(self, password):

        if len(password) < 6 or len(password) > 10:
            passwordStrongLevel = PasswordStats(password)
        elif not re.search("[a-z]", password):
            passwordStrongLevel = PasswordStats(password)
        elif not re.search("[0-9]", password):
            passwordStrongLevel = PasswordStats(password)
        elif not re.search("[A-Z]", password):
            passwordStrongLevel = PasswordStats(password)
        elif not re.search("[#@<->,!?;$%^&*_]", password):
            passwordStrongLevel = PasswordStats(password)
        else:
            passwordStrongLevel = PasswordStats(password)
        
        return passwordStrongLevel
       
        