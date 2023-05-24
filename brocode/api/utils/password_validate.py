def password_check(passwd):
     
    SpecialSym =['$', '@', '#', '%']
    val = True
     
    if len(passwd) < 6:
        val = False
        return (val, 'length should be at least 6')
         
    if len(passwd) > 20:
        val = False
        return (val, 'length should be not be greater than 8')
         
    if not any(char.isdigit() for char in passwd):
        val = False
        return (val, 'Password should have at least one numeral')
         
    if not any(char.isupper() for char in passwd):
        val = False
        return (val, 'Password should have at least one uppercase letter')
         
    if not any(char.islower() for char in passwd):
        val = False
        return (val, 'Password should have at least one lowercase letter')
         
    if not any(char in SpecialSym for char in passwd):
        val = False
        return (val,'Password should have at least one of the symbols $@#')
    if val:
        return (val, 'successful')