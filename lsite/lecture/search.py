import sys
import kws
k = kws.kws()
output_lst = k.search(sys.argv[1:])
for o in output_lst:
    print(o)
