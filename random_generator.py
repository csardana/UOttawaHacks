import requests
from random import randint

firstName = 'Chirag'
lastName = 'Sardana'

DOB = '02-04-1998'

userName = ''

[month, year, day] = DOB.split('-')


def generate():
    global userName
    URL = 'https://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text%2Fplain'
    names = requests.get(URL,headers={'User-Agent': 'Custom'})

    namesText = names.text
    namesSeperated = namesText.split()


    randomInt = randint(0, len(namesSeperated))
    fuser = namesSeperated[randomInt]
    num = str(randomInt)
    userName = fuser + num[:2]


def validate():
    global firstName
    global lastName
    global month
    global year
    global day

    if firstName in userName:
        generate()
    if lastName in userName:
        generate()
    if month or day or year in userName:
        generate()
    return userName

if (__name__ == 'main'):
    generate()
    validate()

