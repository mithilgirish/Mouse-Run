SFX_Active = True
Music_Active = True

def set_SFX_Active(value):
    global SFX_Active
    SFX_Active = value

def set_Music_Active(value):
    global Music_Active
    Music_Active = value

def get_SFX_Active():
    return SFX_Active

def get_Music_Active():
    return Music_Active