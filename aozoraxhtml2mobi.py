#!/usr/bin/python

#
# See README.md
#

import xml.dom.minidom
import codecs
import os
import sys

KINDLEGEN = './kindlegen'

def main():
    if len(sys.argv) != 2:
	print >> sys.stderr, 'usage: python aozoraxhtml2mobi.py htmlfile'
	sys.exit(1)
    aozoraxhtml2mobi(sys.argv[1])

def aozoraxhtml2mobi(htmlfile):
    f = codecs.open(htmlfile, 'r', 'shift_jis')
    f.readline()		# delete the XML declaration with encoding
    s = f.read()
    s = s.encode('utf-8')	# convert to UTF-8

    dc = dict()
    self.htmldom = xml.dom.minidom.parseString(s)
    head = self.htmldom.getElementsByTagName("head")[0]
    for m in head.getElementsByTagName("meta"):
	if m.hasAttribute("name") and m.hasAttribute("content") and \
	   m.getAttribute("name").startswith("DC."):
	    dc[m.getAttribute("name")] = m.getAttribute("content")

    body = self.htmldom.getElementsByTagName("body")[0]
    body.setAttribute('style', '-webkit-writing-mode: vertical-rl;')

    opfdom = xml.dom.minidom.parseString(opf_string)
    metadata = opfdom.getElementsByTagName("metadata")[0]
    dcmetadata = opfdom.getElementsByTagName("dc-metadata")[0]

    m = opfdom.createElement('dc:Title')
    m.appendChild(opfdom.createTextNode(unicode(dc['DC.Title'])))
    dcmetadata.appendChild(m)

    m = opfdom.createElement('dc:Creator')
    m.appendChild(opfdom.createTextNode(unicode(dc['DC.Creator'])))
    dcmetadata.appendChild(m)

    fout = open('content.html', 'w')
    fout.write(self.htmldom.toxml("Shift_JIS"))
    fout.close()

    fout = open('content.opf', 'w')
    fout.write(opfdom.toxml("UTF-8"))
    fout.close()

    os.system(KINDLEGEN + ' -locale ja content.opf -o output.mobi')

opf_string = """
<package xmlns:xx="http://saxon.sf.net/" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:dc="http://purl.org/metadata/dublin_core" unique-identifier="BookId" version="2.0">

	<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">

		<meta name="primary-writing-mode" content="vertical-rl"/>
		<dc-metadata xmlns:dc="http://purl.org/metadata/dublin_core" xmlns:oebpackage="http://openbook.org/namespaces/oeb-package/1.0/">
		    <dc:Language>ja</dc:Language>
		</dc-metadata>
	</metadata>

	<manifest>

		<item id="content" href="content.html" media-type="application/xhtml+xml"/>
	
	</manifest>
	<spine>
		<itemref idref="content"/>
	</spine>
</package>
"""
if __name__ == '__main__':
    main()
