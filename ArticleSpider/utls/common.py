#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Fade Zhao'

import hashlib

def get_md5(url):
    if isinstance(url,str):
        # 因为在python3中所有的字符默认都是Unicode，而Md5不能够给Unicode加密，所以转换成utf-8
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()