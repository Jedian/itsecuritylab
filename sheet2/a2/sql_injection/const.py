#!/usr/bin/env python
import os
FLAG_LOG=os.path.join(os.path.abspath(os.path.dirname(__file__)), "log.txt")

HOST="10.0.23.22"
BASE_URL="http://{}/myspray".format(HOST)
