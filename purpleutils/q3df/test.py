from lxml.etree import HTML, XML, XPath
from urllib import urlopen
from re import compile, DOTALL


z = urlopen('http://www.q3df.org/rankings/map-%s/sort-rank/asc/physic-1' % 'pornstar-slopin')
body = compile("(<tbody>.*</tbody>)", DOTALL)
root = HTML(body.search(z.read()).group(1))
print root.xpath("//tbody/tr/")
