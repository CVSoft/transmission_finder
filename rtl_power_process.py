import time
from sys import argv

def frange(start, stop, step):
    """generator, like xrange, but works for floats etc."""
    v = start
    while v < stop:
        yield v
        v += step

class Line(object):
    def __init__(self, l):
        # sanity checking and input formatting
        if ',' not in l: raise ValueError
        ll = map(lambda q:q.strip(), l.split(','))
        # define variables provided within line's data
        self.ts = time.strptime(ll[0]+' '+ll[1], "%Y-%m-%d %H:%M:%S")
        self.samples = int(ll[5])
        self.binsize = float(ll[4])
        # build frequency range and data
        fl = frange(*map(float, ll[2:5]))
        self.data = zip(fl, map(float, ll[6:]))

    def noise_floor(self):
        _, v = zip(*self.data)
        v = sorted(v)
        return sum(v[:len(v)/3])/(len(v)/3.)

    def get_idx(self, fc):
        """returns nearest index of given frequency f"""
        f, _ = zip(*self.data)
        f = map(lambda q:abs(fc-q), f)
        mv = f[0]
        for i in xrange(len(f)):
            if mv < f[i]: return i
            mv = f[i]
        return len(f)-1

def test1(fn):
    # takes the first line of an input csv and makes a global to play
    # around with in IDLE
    global l
    with open(fn, 'r') as f:
        l = Line(f.readline())

def test2(fn):
    # draws graphs of each line in the input csv
    global ll
    w = 200
    h = 40
    with open(fn, 'r') as f:
        ll = [Line(l) for l in iter(f)]
    fm = input("Marker freq (Hz):")
    ml = [u' ' for i in xrange(w)]
    ml[int(ll[0].get_idx(fm)*len(ml)/float(len(ll[0].data)))] = unichr(0x2588)
    ml = u''.join(ml)
    for l in ll:
        print '\n'*40
        print "%.0f - %.0f (marker at %.0f)" % (l.data[0][0],
                                                l.data[-1][0],
                                                fm)
        print ml
        print _debug_graph(l.data, w=w, h=h, fillchr=unichr(0x2588),
                           key_i1=True)
        raw_input()

def _debug_graph(data, w=79, h=10, fill=True, fillchr=u'#', key_i1=False):
    """generate a text graph. key_i1 needed if data is from a Line"""
    if len(fillchr) != 1: raise ValueError
    if key_i1:
        data = map(lambda q:q[1], data)
    ymin, ymax = (float(min(data)), float(max(data)))
    # binning
    # peak-holds if len(data)>79
    hgts = [h-1]*w
    i = 0
    step = (float(w)-0.9999)/(len(data)-1)
    last_idx = 0
    for j in frange(0., float(w)-0.9999, step):
        j = int(j)
        # fill in gaps from last step
        if j - last_idx > 1:
            for k in xrange(last_idx+1, j, 1):
                hgts[k] = hgts[last_idx]
        # find and store index for marker
        hgts[j] = min([int((h-1)*(ymax-data[i])/(ymax-ymin)), hgts[j]])
        last_idx = j
        i += 1
    # form graph
    graph = [[u' ' for i in xrange(w)] for j in xrange(h)]
    for i in xrange(w):
##        print "Changing index", hgts[i], i
        if fill:
            for j in xrange(hgts[i], h): graph[j][i] = fillchr
        else:
            graph[hgts[i]][i] = fillchr
    graph.insert(0, [u'=' for i in xrange(w)])
    graph.append([u'=' for i in xrange(w)])
    return u'\n'.join(map(lambda q:u''.join(q), graph))

if __name__ == "__main__":
    if len(argv) == 1: fn = "freebanders.csv"
    else: fn = argv[1]
    test2(fn)
