
# Usage:
# python read-wikisource.py >test-pages-x.txt

import urllib
import urllib.request
import re
import textwrap

"""
'''inhibition''' s Action de imbibir, de imbiber se; 
absorption.<noinclude></noinclude>
"""

def cut_noinclude (txt):
  p = re.compile (r'<noinclude>.*?</noinclude>')
  return p.sub ('', txt)

# (part,start,end): start <= p < end
page_range = [
  (1,1,416),
  (2,1,401),
  (3,1,401),
  (4,1,366), ]
test_range = [
  (1,1,3),
  (1,240,246),
  (2,264,267), ]

"""
# existing:
test_1 = "https://wikisource.org/wiki/Page:Macovei-Dictionario_
Encyclopedic_de_Interlingua-1_de_4.pdf/1?action=raw"

# non-existing:
test_2 = "https://wikisource.org/wiki/Page:Macovei-Dictionario_
Encyclopedic_de_Interlingua-1_de_4.pdf/33?action=raw"
"""

def read_page (m,n):
  link = ("https://wikisource.org/wiki/Page:Macovei-Dictionario_"
    f"Encyclopedic_de_Interlingua-{m}_de_4.pdf/{n}?action=raw")
  try:
    f = urllib.request.urlopen (link)
    html = f.read ()
    html = html.decode ()
    html = cut_noinclude (html)
  except urllib.error.HTTPError:
    html = "\n[Hic manca un pagina.]"
  return html + "\n"

# html = read_page (2,266)
# print (html)

txtwrap = True
wrp = textwrap.TextWrapper(width=65)

def wrapped (txt):
  xs = txt.splitlines ()
  y = []
  for x in xs:
    z = "\n".join (wrp.wrap(text=x))
    y.append (z)
  result = "\n".join (y)
  return result

for part,start,end in test_range:
 for p in range (start,end):
  html = read_page (part,p)
  if textwrap: html = wrapped (html)
  print (html)

