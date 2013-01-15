"""
Cell Automaton to Jigsaw model encoding

output:

start:
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']
finished:
['s1', 's0s1', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0']
['s1', 's1s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0', 's0s0', 's0']
* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

*   *   *   *   *   *   *   *   *   *   *   *   *   *   *   *

* *     * *     * *     * *     * *     * *     * *     * *

*       *       *       *       *       *       *       *

* * * *         * * * *         * * * *         * * * *

*   *           *   *           *   *           *   *

* *             * *             * *             * *

*               *               *               *

* * * * * * * *                 * * * * * * * *

*   *   *   *                   *   *   *   *

* *     * *                     * *     * *

*       *                       *       *

* * * *                         * * * *

*   *                           *   *

* *                             * *

*                               *

* * * * * * * * * * * * * * * *

*   *   *   *   *   *   *   *

* *     * *     * *     * *

*       *       *       *

* * * *         * * * *

*   *           *   *

* *             * *

*               *

* * * * * * * *

*   *   *   *

* *     * *

*       *

* * * *

*   *

* *

*
"""

NUM_STATES = 2

# [(left, top, bottom, right)]
pieces = [
    ('0', '0', 's1', 's1') # initial pattern generation
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

# Rule 90
#111	110	101	100	011	010	001	000
#0	1	0	1	1	0	1	0
RULE = 90
for s1 in range(NUM_STATES):
    for s2 in range(NUM_STATES):
        for s3 in range(NUM_STATES):
            i = (s1 * NUM_STATES + s2) * NUM_STATES + s3
            next_state = 1 if RULE & (1 << i) else 0
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

print 'num pieces:', len(pieces)

left_border = "0" * 63
top_border = "0" * 63

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
        if right == 's1':
            world[y][x] = '*'
        else:
            world[y][x] = ' '

        # print "%d,%d: %s,%s->%s,%s" % (x, y, left, top, bottom, right)

print "finished:"
print left_joint
print top_joint
print '\n'.join(''.join(line) for line in world)
