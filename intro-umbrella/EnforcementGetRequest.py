#!/usr/bin/env python
"""


Copyright (c) 2018-2019 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import datetime
import requests
import configparser
import json
import sys
from pathlib import Path
from crayons import blue, green, red
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# Locate the directory containing this file and the repository root.
# Temporarily add these directories to the system path so that we can import
# local files.
here = Path(__file__).parent.absolute()
repository_root = (here / "..").resolve()

sys.path.insert(0, str(repository_root))

sys.path.insert(0, str(repository_root))

from env_lab import UMBRELLA  # noqa
from env_user import UMBRELLA_ENFORCEMENT_KEY

# Disable insecure request warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

enforcement_api_key = UMBRELLA_ENFORCEMENT_KEY

time = datetime.now().isoformat()


# URL needed to do POST requests
domain_url = "https://s-platform.api.opendns.com/1.0/domains"

# URL needed for POST request
url_get = domain_url + '?customerKey=' + enforcement_api_key

# create empty list to contain all domains already in Umbrella
domain_list = []

# keep doing GET requests, until looped through all domains
while True:
    req = requests.get(url_get)
    json_file = req.json()
    for row in json_file["data"]:
        domain_list.append(row["name"])
    # GET requests will only list 200 domains, if more than that, it will request next bulk of 200 domains
    if bool(json_file["meta"]["next"]):
        Url = json_file["meta"]["next"]
    # break out of loop when finished
    else:    
        break

# error handling if true then the request was HTTP 200, so successful 
if(req.status_code == 200):
  print("SUCCESS: the following domain(s) are in your current custom Block List:")
  print(domain_list)
else:
  print("An error has ocurred with the following code %(error)s, please consult the following link: https://enforcement-api.readme.io/" % {'error': req.status_code})