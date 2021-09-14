
# python thoreau-substitue.py -i dictionario-encyclopedic-2021-09-13.txt -o output.txt --log

import argparse
import re
import time
from datetime import datetime
from math import *
from collections import defaultdict
from tabulate import tabulate

def read_args ():
  parser = argparse.ArgumentParser ()
  parser.add_argument ("-i", "--input", default="input.txt")
  parser.add_argument ("-o", "--output", default="output.txt")
  parser.add_argument ("-s", "--substitue", default="substitue.txt")
  parser.add_argument ("-p", "--prefixdate", default="")
  parser.add_argument ("-sep", "--separator", default="\t")
  parser.add_argument ("--log", action="store_true")
  args = parser.parse_args ()
  return (args)

args = read_args()

start = time.time()
date = datetime.today().strftime('%Y-%m-%d')

g = open (args.substitue)
xs = g.readlines ()
g.close ()

subs = []
for x in xs:
  sb = x.strip ("\n").split (args.separator)
  if len (sb) == 2:
    subs.append (sb)

f = open (args.input)
text = f.read ()
f.close ()

found = defaultdict (int) # default = 0
for pattern,repl in subs:
  text,fnd = re.subn (pattern,repl,text)
  found [(pattern,repl)] = found [(pattern,repl)] + fnd

outputfile = args.output
if args.prefixdate:
  outputfile = args.prefixdate + "-" + date + ".txt"
h = open (outputfile,"w")
h.write (text)
h.close ()

subs2 = []
for a,(k,v) in zip (subs,found.items()):
  subs2.append (a + [v])

end = time.time()
total = end - start
decimals = abs (floor (log (total,10))) + 2
if args.log:
  print ("Scribeva", outputfile)
  print (tabulate (subs2))
  print (f"({total:.{decimals}} s)\n") 

