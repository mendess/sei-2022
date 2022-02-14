with open('flag', 'rb') as f:
    flag = f.read().strip()


def as_nibbles(b):
    yield (b & 0b11000000) >> 6
    yield (b & 0b00110000) >> 4
    yield (b & 0b00001100) >> 2
    yield b & 0b00000011
    return

towers = {
    0b00: '|',
    0b01: '/',
    0b10: '-',
    0b11: '\\'
}

with open('input.txt', 'w') as f:
    for b in flag:
        for nibble in as_nibbles(b):
            f.write(towers[nibble])


