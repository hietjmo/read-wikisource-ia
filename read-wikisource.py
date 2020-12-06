
# Usage (per exemplo):
# python read-wikisource.py --count 20 --sleep 20

import urllib
import urllib.request
import re
import os
import time
import textwrap
import argparse

def cut_noinclude (txt):
  p = re.compile (r'<noinclude>.*?</noinclude>')
  return p.sub ('', txt)

# (part,start,end): start <= p < end
page_range = [(1,1,416), (2,1,401), (3,1,401), (4,1,366)]

prnge = {}
i = 1
for part,start,end in page_range:
 for p in range (start,end):
   prnge [i] = (part,p)
   i += 1

def address (m,n):
  return ("https://wikisource.org/wiki/Page:Macovei-Dictionario_"
    f"Encyclopedic_de_Interlingua-{m}_de_4.pdf/{n}?action=raw")

def read_page (addr):
  try:
    f4 = urllib.request.urlopen (addr)
    html = f4.read ()
    f4.close ()
    html = html.decode ()
    html = cut_noinclude (html)
  except urllib.error.HTTPError:
    html = "\n[Hic manca un pagina.]"
  return html + "\n"


def wrapped (txt):
  wrp = textwrap.TextWrapper (width=args.wrap)
  xs = txt.splitlines ()
  y = []
  for x in xs:
    z = "\n".join (wrp.wrap (text=x))
    y.append (z)
  result = "\n".join (y)
  return result

def pr_or_None (i):
  if i in prnge:
    return prnge [i]
  else:
    return None

parser = argparse.ArgumentParser ()
parser.add_argument ("-i", "--init", default=False)
parser.add_argument ("-n", "--count", type=int, default=1)
parser.add_argument ("-s", "--sleep", type=int, default=5)
parser.add_argument ("-w", "--wrap", type=int, default=0)
parser.add_argument ("-d", "--directory", default="paginas")
args = parser.parse_args ()
for arg in vars (args):
  print (arg, getattr (args, arg))

directory = args.directory

if not os.path.exists (directory):
  os.mkdir (directory)
  print ("Created directory:",directory)

statfile = "current.txt"
if not args.init and not args.directory and os.path.isfile (statfile):
  with open (statfile) as f5:
    pr = int (f5.readline())
else:
  pr = 0

pr += 1
for i in range (pr,pr+args.count):
  pg = pr_or_None (i)
  if pg:
    part,p = pg
    addr = address (part,p)
    print ("Parte:",part,"Pagina:",p)
    print ("Receiving:",addr)
    html = read_page (addr)
    if args.wrap > 0: html = wrapped (html)
    filename = f"{directory}/p{str(i).zfill(4)}.txt"
    with open (filename,"w") as f3:
      f3.write (html)
    print ("Wrote:", filename)
  else:
    print ("Non in intervallo de paginas:", i)
  with open (statfile,"w") as f2:
    f2.write (str(i))
  time.sleep (args.sleep)

