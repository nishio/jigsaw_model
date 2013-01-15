"""
Prime calculating automaton in Jigsaw model

Ref:
  http://www.wolframscience.com/nksonline/page-1109

"""

NUM_STATES = 16
import csv
r = csv.reader(file('prime_pieces.csv'))
pieces = list(r)

print 'num pieces: ', len(pieces)

left_border = '0' * 60
top_border = '0' * 60

# prepare dictionary
pdict = {}
for p in pieces:
    left, top, bottom, right = p
    k = (left, top)
    assert not pdict.has_key(k)
    pdict[k] = (bottom, right)

# put pieces
WIDTH = len(top_border)
HEIGHT = len(left_border)
world = [[None] * WIDTH for _i in range(HEIGHT)]
left_joint = list(left_border)
top_joint = list(top_border)

for i in range(WIDTH + HEIGHT):
    for x in range(WIDTH):
        y = i - x
        if y < 0: break
        if y >= HEIGHT or x >= WIDTH: continue
        top = top_joint[x]
        left = left_joint[y]
        (bottom, right) = pdict[(left, top)]
        top_joint[x] = bottom
        left_joint[y] = right
        if bottom == '24':
            world[y][x] = '|'
        elif bottom == '6':
            world[y][x] = '.'
        else:
            world[y][x] = ' '

print '\n'.join(''.join(line) for line in world)
