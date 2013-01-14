from urllib import quote
from .useragentlib import DisguisedOpener, urlopen
from lxml.html import document_fromstring as parse

RANKINGS_URL = "http://q3df.org/records/details?map=%s&physic=%d"

def getBest(mapname, promode):
    """
    sigue e l modelo
     [[td.text_content() for td in tr.xpath('td')] for tr in document_fromstring(z).xpath('//table//tr') if len(tr.xpath('t
        d')) == 6]
    
    returns
      ["Mar 22nd, '11, 20:40",
      u'\xa0Bazz',
      '12:824',
      '8/73',
      'cpm-run',
      'mDd | Defrag CPM Runs I'],
    """

    raw = urllib.urlopen(RANKINGS_URL % (mapname, promode)).read()

    results = []
    for tr in parse(raw).xpath("//table//tr"):
        tds = tr.xpath("td")
        if len(tds) != 6:
            continue

        row = dict(zip(("date", "name", "runtime", "rank", "physics", "server"),
                (td.text_content() for td in tds)))
        results.append(row)

    return results
