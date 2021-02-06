import requests
from random import randint

def generate(firstname, lastname, dob):
    URL = 'https://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text%2Fplain'
    names = requests.get(URL,headers={'User-Agent': 'Custom'})

    namesText = names.text
    namesSeperated = namesText.split()


    randomInt = randint(0, len(namesSeperated))
    fuser = namesSeperated[randomInt]
    num = str(randomInt)
    userName = fuser + num[:2]
    validate(firstname, lastname, dob, userName)


def validate(firstname, lastname, dob, userName):
    [month, year, day] = dob.split('-')

    if firstname in userName:
        generate(firstname, lastname, dob)
    if lastname in userName:
        generate(firstname, lastname, dob)
    if month or day or year in userName:
        generate(firstname, lastname, dob)

