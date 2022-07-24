# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from datetime import datetime
from hashlib import sha224
import math
import os

from config import UNITS 


def get_current_date(date_fmt):
    return datetime.today().strftime(date_fmt)

def calculate_sha224_hash(file_name):
    with open(file_name, "rb") as file:
        data = file.read()
    return sha224(data).hexdigest()

def get_file_size(file_name):
    size_bytes = os.path.getsize(file_name)
    if size_bytes == 0:
        return "0B"
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    size_fmt = f"{s} {UNITS[i]} ({size_bytes:,} bytes)"
    return size_fmt
