import utils
import sys  # This library is imported in order to access execution arguments

if len(sys.argv) != 4:
    print "Correct calling format is ./train < model > < heb-pos.train > < smoothing(y/n) >"
    exit(0)

model = sys.argv[1]
fileName = sys.argv[2]
smoothing = sys.argv[3]
