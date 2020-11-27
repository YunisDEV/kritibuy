import string
import random

def generateCouponCode(length=7):
    characterSet = list(
        set(list(string.ascii_lowercase+string.ascii_uppercase+'0123456789')))
    setlen = len(characterSet)
    generatedKey = ''
    for i in range(length):
        generatedKey += str(characterSet[random.randrange(0, setlen-1, 1)])
    return generatedKey