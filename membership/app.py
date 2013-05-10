__author__ = 'timp'



def checkPasswordCompliance(password):
    hasAny = lambda cs: True in [c in password for c in cs]
    valid = hasAny(string.lowercase) and hasAny(string.uppercase) and hasAny(string.digits) and len(
        password) >= 7 and len(password) < 32
    if not valid:
        raise StandardError(
            'Pass phrase was insufficiently complex'
#    "Weak password: should be 7-31 characters with at least 1 upper-case letter, 1 lower-case letter and 1 digit."
        )
