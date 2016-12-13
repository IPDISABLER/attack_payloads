#!/usr/bin/env python

binary_data = b'\x03\xff\x00d' * (2 ** 32)
with open("blob.bin", "wb") as blob_handle:
    blob_handle.write(bytearray(binary_data))
