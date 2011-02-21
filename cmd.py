#!/usr/bin/env python3
# Copyright 2011 Tom Vincent <http://www.tlvince.com/contact/>

"""Setup cmd with some sane defaults."""

import os
import ctypes
import subprocess
import getpass
import sys
import logging

from urllib.request import getproxies_registry
from urllib.parse import urlparse

def getMyDocs():
    """Return the path to My Documents.
    http://stackoverflow.com/questions/3927259/how-do-you-get-the-exact-path-to-my-documents/3927493#3927493"""
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(300)
    dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False)
    return buf.value

def setProxies(user, password, host, port):
    """Set proxy variables for the currently running shell."""
    schemes = ["http", "https"]

    for scheme in schemes:
        # XXX: https_proxy still uses http scheme
        base = scheme
        if scheme == "https":
            base = scheme[:-1]
        os.putenv(scheme + '_proxy',
            "{0}://{1}:{2}@{3}:{4}".format(base, user, password, host, port)
        )

def postHook():
    """Perform some platform-specific post operations."""
    if sys.platform == "win32":
        cmd = ["cmd.exe", "/k", "cd", getMyDocs()]
        subprocess.call(cmd)

def getProxyHost():
    """Return the proxy host and port from Windows registry."""
    try:
        proxy = getproxies_registry()["http"]
        return urlparse(proxy).netloc.split(":")
    except KeyError:
        logging.error("Cannot retreive proxy settings from registry")

def main():
    """Start execution of cmd."""
    un = getpass.getuser()
    pw = getpass.getpass()

    try:
        host, port = getProxyHost()
    except Exception:
        host = input("Host: ")
        port = input("Port: ")

    setProxies(un, pw, host, port)
    postHook()

if __name__ == "__main__":
    main()
