"""
Prime calculating automaton in Jigsaw model

Ref:
  http://www.wolframscience.com/nksonline/page-1109

"""

NUM_STATES = 16

# [(left, top, bottom, right)]
pieces = [  # initial pattern generation
    ( '0',  '0',  'i1',  'i1'),
    ( '0', 'i1',  'i2',  'i2'),
    ('i1',  '0',  'i2',  'i2'),
    ( '0', 'i2',  'i3',  'i3'),
    ('i2', 'i2',  'i3',  'i4'),
    ('i2',  '0',  'i4',  'i4'),
    ( '0', 'i3', 's10', 's10'),
    ('i3', 'i3',  's0',  's0'),
    ('i4', 'i4',  's4',  's4'),
    ('i4',  '0',  's8',  's8'),
]

# add propagation pieces
for s1 in range(NUM_STATES):
    for s2 in range(NUM_STATES):
        comb = 's%ds%d' % (s1, s2)
        pieces.append(
            ('s%d' % s1, 's%d' % s2,
             comb, comb))

    # consider 0 as state-0
    pieces.append(
        ('s%d' % s1, '0',
         's%ds0' % s1, 's%ds0' % s1))
    pieces.append(
        ('0', 's%d' % s1,
         's0s%d' % s1, 's0s%d' % s1))

# Rule to generate primes

ANY = None

# typedef (ANY | [Int] | Int) Match
# rules :: [((Match, Match, Match), Int)]
rules = [
    ((13, 3, 13), 12),
    ((6, ANY, 4), 15),
    ((10, ANY, [3, 11]), 15),
    ((13, 7, ANY), 8),
    ((13, 8, 7), 13),
    ((15, 8, ANY), 1),
    ((8, ANY, ANY), 7),
    ((15, 1, ANY), 2),
    ((ANY, 1, ANY), 1),
    ((1, ANY, ANY), 8),
    (([2, 4, 5], ANY, ANY), 13),
    ((15, 2, ANY), 4),
    ((ANY, 4, 8), 4),
    ((ANY, 4, ANY), 5),
    ((ANY, 5, ANY), 3),
    ((15, 3, ANY), 12)
] + [
    ((ANY, x, ANY), x) for x in [2, 3, 8]
] + [
    ((ANY, x, ANY), x-1) for x in [11, 12]
] + [
    ((11, ANY, ANY), 13),
    ((13, ANY, [1, 2, 3, 5, 6, 10, 11]), 15),
    ((13, 0, 8), 15),
    ((14, ANY, [6, 10]), 15),
    ((10, [0, 9, 13], [6, 10]), 15),
    ((6, ANY, 6), 0),
    ((ANY, ANY, 10), 9),
    (([6, 10], 15, 9), 14),
    ((ANY, [6, 10], [9, 14, 15]), 10),
    ((ANY, [6, 10], ANY), 6),
    (([6, 10], 15, ANY), 13),
    (([13, 14], ANY, [9, 15]), 14),
    (([13, 14], ANY, ANY), 13),
    ((ANY, ANY, 15), 15),
    ((ANY, ANY, [9, 14]), 9),
    ((ANY, ANY, ANY), 0)
]

# match :: (Int, Match) -> Bool
def match(x, y):
    if isinstance(y, list):
        return (x in y)
    if isinstance(y, int):
        return (x == y)
    if y == None:
        return True
    raise AssertionError('not here', y)


# apply_rules :: (Int, Int, Int) -> Int
def apply_rules(prev):
    for rule in rules:
        matches, result = rule
        if all(match(x, y) for x, y in zip(prev, matches)):
            return result
    raise AssertionError('not here')


for s1 in range(NUM_STATES):
    for s2 in range(NUM_STATES):
        for s3 in range(NUM_STATES):
            next_state = apply_rules((s1, s2, s3))
            pieces.append(
                ('s%ds%d' % (s1, s2), 's%ds%d' % (s2, s3),
                 's%d' % next_state, 's%d' % next_state))

            # consider 0 as s0s0
            if s1 == s2 == 0:
                pieces.append(
                    ('0', 's%ds%d' % (s2, s3),
                     's%d' % next_state, 's%d' % next_state))
            if s2 == s3 == 0:
                pieces.append(
                    ('s%ds%d' % (s1, s2), '0',
                     's%d' % next_state, 's%d' % next_state))


def output_pieces():
    import csv
    w = csv.writer(file('prime_pieces.csv', 'w'))
    symbols = []
    def get_id(x):
        try:
            return symbols.index(x)
        except:
            ret = len(symbols)
            symbols.append(x)
            return ret
    for p in pieces:
        w.writerow(map(get_id, p))

    #print get_id('s0') #-> 6
    #print get_id('s9') #-> 24
#output_pieces()

print 'num pieces: ', len(pieces)

left_border = "0" * 60
top_border = "0" * 60

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
        if bottom == 's9':
            world[y][x] = '|'
        elif bottom == 's0':
            world[y][x] = '.'
        else:
            world[y][x] = ' '
        #world[y][x] = '%7s' % bottom

        # print "%d,%d: %s,%s->%s,%s" % (x, y, left, top, bottom, right)

print "finished:"
print left_joint
print top_joint
print '\n'.join(''.join(line) for line in world)
#print ''.join(world[51][0:50:2])
