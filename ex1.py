"""
Jigsaw model

Changed from the paper:
input->output : top->bottom or left->right

start:
['2', '0', '1']
['0', '0', '0', '0', '0']
finished:
['0', '0', '0']
['1', '1', '0', '0', '1']
"""

# [(left, top, bottom, right)]
pieces = [
    "0000",
    "1010",
    "2001",
    "0111",
    "1102",
    "2112",
]

left_border = "201"
top_border = "00000"

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

print "start:"
print left_joint
print top_joint

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

print "finished:"
print left_joint
print top_joint
