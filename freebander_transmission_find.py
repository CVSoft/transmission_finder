import sys
import time
import rtl_power_process as rtl

def main(fn, ofn, threshold=1):
    first_tx, last_tx, dead_tx = (None, None, None)
    with open(ofn, 'w'): pass
    with open(fn, 'r') as f:
        ll = [rtl.Line(l) for l in iter(f)]
        do_update = True
        for l in ll:
            s = squelch(l, threshold=threshold)
            if s[0]:
##                print "Squelch broken!"
##                print "Freq  : %.6f" % s[3]
##                print "Power : %2.2f dB" % s[1]
##                print "Margin: %2.2f dB" % s[2]
                last_tx = l
                if do_update:
                    first_tx = l
                    dead_tx = None
                    do_update = False
            else:
                if not dead_tx: dead_tx = l
            if not last_tx or not first_tx: continue
            if time.mktime(l.ts)-time.mktime(last_tx.ts) > 60:
                s = squelch(first_tx, threshold=threshold)
                with open(ofn, 'a') as f:
                    f.write("%s: Transmission on %.6f MHz exceeded threshold \
by %2.2f dB and lasted %d seconds.\n" % \
                            (time.strftime("%Y-%m-%d_%H:%M:%S", first_tx.ts),
                             s[3]/1000000, #frequency
                             s[2], #margin
                             time.mktime(dead_tx.ts)-\
                             time.mktime(first_tx.ts)))
                    do_update = True
                    first_tx, last_tx, dead_tx = (None, None, None)

def squelch(l, threshold):
    """checks if a Line object breaks squelch at 148.465 MHz"""
    i = l.get_idx(148465000)
    nf = l.noise_floor()
    freqs, data = zip(*l.data)
    # search zone is +/- 5 kHz (148.460 to 148.470)
    sb_io = int(max([0, 5000/l.binsize])) # bandwidth adjustable here
    pf = max(data[i-sb_io:i+sb_io+1])
    # look for 0.5dB signal-to-noise
    if pf-nf > threshold:
        return (True, pf, pf-nf,
                freqs[data[i-sb_io:i+sb_io+1].index(pf)+(i-sb_io)])
    return (False,)

if __name__ == "__main__":
    if len(sys.argv) == 1: main("freebanders.csv", "transmissions.txt")
    else: main(sys.argv[1], sys.argv[2], float(sys.argv[3]))
