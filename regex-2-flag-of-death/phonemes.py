import string
from random import randint, choice, shuffle
import urllib.request
import sys

letters = string.ascii_lowercase + string.ascii_uppercase

most_common = 'etaoins'
most_common += most_common.upper()

printable_chars = [chr(x) for x in range(33, 127)]
bf_chars = '<>+-[].,'

bf_sei = '>++++++++++[>++++++++>+++++++>+++++++><<<<-]>+++>->+++><<<<>.>.>.'

answer = randint(0, 50000)

where1 = [randint(0, 50000) for _ in range(12345)]
where2 = [randint(0, 50000) for _ in range(12345)]
where3 = [randint(0, 50000) for _ in range(12345)]

where1 = list(filter(lambda x: not (x in where2 and x in where3), where1))
where2 = list(filter(lambda x: not (x in where1 and x in where3), where2))
where3 = list(filter(lambda x: not (x in where1 and x in where2), where3))

for l in [where1, where2, where3]: l.append(answer)

def dictionary():
    try:
        with open('wordlist') as wordlist:
            return wordlist.read().splitlines()
    except:
        word_url = "https://www.mit.edu/~ecprice/wordlist.10000"
        response = urllib.request.urlopen(word_url)
        long_txt = response.read().decode()
        with open('wordlist', 'w') as wordlist:
            wordlist.write(long_txt)
        return long_txt.splitlines()

words = [w for w in dictionary() if len(w) >= 5]


sys.stderr.write(str(answer) + '\n')

for i in range(50000):
    if i == answer:
        print('SEI{iesiesi' + bf_sei  + 'fuzzy}')
        continue

    source = most_common if i in where1 else letters
    start = ''.join(choice(source) for x in range(7))

    source = bf_chars if i in where2 else printable_chars
    middle = ''.join(choice(source) for x in range(randint(len(bf_sei) - 10, len(bf_sei) + 10)))

    end = choice(words)
    print(f'SEI{{{start}{middle}{end}}}')
