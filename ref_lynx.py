#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : ref_lynx.py
# Creation Date : 16-12-2012
# Last Modified : Mon 17 Dec 2012 12:37:20 AM EET
# Created By : Greg Liras <gregliras@gmail.com>
#_._._._._._._._._._._._._._._._._._._._._.*/

from sys import stdin
import re
from conf import api_key, username

import bitly_api


def main():
    data = stdin.read()
    r = re.compile(" *[1-9][0-9]*\. .*")
    bcl = bitly_api.Connection(username, api_key)
    print data[:data.rfind("References")]
    print "References:"
    for ans in re.findall(r, data):
        ans = ans.split()
        try:
            btlurl = bcl.shorten(ans[1])
            print ans[0], btlurl['url']
        except bitly_api.bitly_api.BitlyError:
            print ans[0], ans[1]



if __name__=="__main__":
    main()

