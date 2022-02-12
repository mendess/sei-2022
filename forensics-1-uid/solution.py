import re

f = open('puzzle.jpg', 'rb')
t = f.read()
pat = re.compile(b"......JFIF")
matches = list(pat.finditer(t))
for i in range(len(matches)):
    file = open('foto' + str(i) + '.jpg', 'wb')
    start = matches[i].start(0)
    end = matches[i+1].start(0) if i < (len(matches) - 1) else len(t)
    file.write(t[start:end])
    file.close()
