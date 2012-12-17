#!/usr/bin/env python
# -*- coding: utf-8
#
#* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# File Name : ref_lynx.py
# Creation Date : 16-12-2012
# Last Modified : Mon 17 Dec 2012 11:50:33 AM EET
# Created By : Greg Liras <gregliras@gmail.com>
#_._._._._._._._._._._._._._._._._._._._._.*/

from sys import stdin
import re
from conf import api_key, username

import bitly_api


import threading, Queue, time
q = Queue.Queue()
rq = Queue.Queue()

def work():
    bcl = bitly_api.Connection(username, api_key)
    while True:
        try:
            arg = q.get(block=False)
        except Queue.Empty:
            break
        else:
            try:
                btlurl = bcl.shorten(arg[1])
            except bitly_api.bitly_api.BitlyError:
                rq.put((arg[0],arg[1]))
            else:
                rq.put((arg[0],btlurl['url']))
    exit()

def main():

    nThreads = 8
    ths=[]
    for i in range(nThreads):
        t = threading.Thread(target=work)
        t.setDaemon(True)
        ths.append(t)

    data = stdin.read()
    r = re.compile("[ \t]*[1-9][0-9]*\. .*")
    ref = data.rfind("References")
    print data[:ref]
    allRefs = re.findall(r, data[ref:])
    for ans in allRefs:
        ans = ans.split()
        q.put(ans)
    map(lambda x: x.start(), ths)
    map(lambda x: x.join(), ths)
    if allRefs:
        print "References:"


    d = {}
    while True:
        try:
            ans = rq.get(block=False)
        except Queue.Empty:
            break
        else:
            d[ans[0]] = ans[1]
    for ans in allRefs:
        ans = ans.split()
        print ans[0], d[ans[0]]



if __name__=="__main__":
    main()

