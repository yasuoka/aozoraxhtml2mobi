#!/usr/bin/python

#
# Copyright (c) 2012 YASUOKA Masahiko <yasuoka@yasuoka.net>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

# See README.md

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
    htmldom = xml.dom.minidom.parseString(s)
    head = htmldom.getElementsByTagName("head")[0]
    for m in head.getElementsByTagName("meta"):
        if m.hasAttribute("name") and m.hasAttribute("content") and m.getAttribute("name").startswith("DC."):
            dc[m.getAttribute("name")] = m.getAttribute("content")

    body = htmldom.getElementsByTagName("body")[0]
    body.setAttribute('style', '-webkit-writing-mode: vertical-rl;')

    opfdom = xml.dom.minidom.parseString(opf_string)
    metadata = opfdom.getElementsByTagName("metadata")[0]
    dcmetadata = opfdom.getElementsByTagName("dc-metadata")[0]

    m = opfdom.createElement('dc:Title')
    if not 'DC.Title' in dc:
        title = body.getElementsByTagName("h1")[0].firstChild.nodeValue
    else:
        title = dc['DC.Title']
    m.appendChild(opfdom.createTextNode(title))
    dcmetadata.appendChild(m)

    m = opfdom.createElement('dc:Creator')
    m.appendChild(opfdom.createTextNode(dc['DC.Creator']))
    dcmetadata.appendChild(m)

    fout = open('content.html', 'wb')
    fout.write(htmldom.toxml("Shift_JIS"))
    fout.close()

    fout = open('content.opf', 'wb')
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
