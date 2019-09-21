#Created to not be lazy
class PAMsErrors(Exception):
    """Base error Class for P.A.M."""
    pass

class PAM_WrongAnswer(PAMsErrors):
    """Wrong Answer"""
    pass

class PAM_Disappointed(PAMsErrors):
    """You made P.A.M. sad"""
    pass