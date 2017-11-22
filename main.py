#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Fade Zhao'

from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute([
    "scrapy",
    "crawl",
    "jobbole",  #等同于命令行 scrapy crawl jobbole
])
