from PIL import Image
from sys import argv

img = argv[1] if len(argv) > 1 else 'redacted.png'

Image.open(img).convert('RGB').save('solved.png')
