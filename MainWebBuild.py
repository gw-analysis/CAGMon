#!/usr/bin/env python
from MainHTML import *
import ast
import ConfigParser
config=ConfigParser.ConfigParser()
config.read("CAGConfig.ini")
chlist=ast.literal_eval(config.get('Parameter','chlist'))

print 'Generating index.html page...'
filename=CAGHeader(chlist)
CAGBody(filename)
CAGFoot(filename)

print 'All Processes Done.'





