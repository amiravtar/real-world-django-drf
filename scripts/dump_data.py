#!/usr/bin/env python

import sys
import os

apps = sys.argv[1:]
for i in apps:
    if not os.path.exists("{0}/fixtures".format(i)):
        os.mkdir("{0}/fixtures".format(i))
    os.system("python manage.py dumpdata {0} -o {0}/fixtures/{0}.json".format(i))
