#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""
Runfile for netcamscp
    Ian Nesbitt <ian.nesbitt@gmail.com>
"""

import urllib
import os
import json
import time
from datetime import datetime
import paramiko
from scp import SCPClient
from PIL import Image

BASEPATH = os.path.dirname(os.path.abspath(__file__))
JSONPATH = os.path.abspath(os.path.join(BASEPATH, "settings.json"))

SUCCESS = False

try:
    with open(JSONPATH) as j:
        SETTINGS = json.load(j)
    IMAGE = SETTINGS["image_loc"]
    LOCAL = SETTINGS["temp_loc"]
    SERVER = SETTINGS["server_hostname"]
    REMOTE = SETTINGS["server_img_loc"]
    USERNAME = SETTINGS["user"]
    VERBOSE = SETTINGS["verbose"]
    if SETTINGS["using_pkey"] == True:
        PKEY = SETTINGS["pkey"]
    else:
        PASSWORD = SETTINGS["pass"]
except IOError as io_err:
    print("Could not find or could not open JSON at " + JSONPATH)
    raise PathError("You must have a JSON named settings.json in the top level directory.")

if VERBOSE:
    print("-------------------------------------")
    print("e4 webcam image retrieval and scp put")
    print("Copyright © 2016 e4sciences, LLC")
    print("written by Ian Nesbitt")
    print("")


def download_image(url):
    """
    download an image
    """
    image = urllib.urlopen(url)
    with open(os.path.basename(LOCAL), "wb") as output:
        output.write(image.read())
    output = Image.open(LOCAL)
    output.save(LOCAL, optimize=True, quality=85)

os.chdir(os.path.split(LOCAL)[0])  # download location
try:
    url = str(IMAGE)
    download_image(url)  # uses the function defined above to download the image
    size = str(os.path.getsize(LOCAL)/1024)
    if VERBOSE:
        print("size: " + size + "kb")
except IOError:  # urllib raises an IOError for a 404 error, when the image doesn't exist
    print str("error fetching image.")

else:
    if VERBOSE:
        print("image downloaded.")
    if SETTINGS["using_pkey"] == True:
        k = paramiko.RSAKey.from_private_key_file(PKEY)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if VERBOSE:
        print("connecting to host server...")
    try:
        if SETTINGS["using_pkey"] == True:
            ssh.connect( hostname = SERVER, username = USERNAME, pkey = k )
        else:
            ssh.connect( hostname = SERVER, username = USERNAME, password = PASSWORD )
        if VERBOSE:
            print("connected")
        scp = SCPClient(ssh.get_transport())
        if VERBOSE:
            print("uploading latest image...")
        scp.put( LOCAL, REMOTE )
        if VERBOSE:
            print("done.")
        scp.close()
        ssh.close()
        SUCCESS = True
        if VERBOSE:
            print("upload successful to " + SERVER)
    except IOError:
        if VERBOSE:
            print("upload failed.")
finally:
    if VERBOSE:
        print("process exit")
        time.sleep(2)
    now = datetime.now()
    now = now.strftime('%Y/%m/%d %H:%M:%S %Z')
    if SUCCESS:
        print(now + " - Success. " + size + "kb")
    else:
        if VERBOSE:
            print(now + " - Failure.")
        else:
            print(now + " - Failure. Enable verbose mode for details.")
