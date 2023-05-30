import string, random

def rnd_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
def getItems(parent):
    children = []
    for i in range(parent.count()):
        children.append(parent.item(i))
