def auth_login(email:str, password:str):
    ######
        # username = fucntion call  >> check the database for user and return the user name
    ####
    username = True
    if username != None:
        return True, username
    else: return False, None # user was not foud in the database