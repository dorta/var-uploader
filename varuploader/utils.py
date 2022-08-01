# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from datetime import datetime
from hashlib import sha224
import math
import os

from config import UNITS
from config import SOFTWARE
from config import OS_B2QT
from config import OS_DEBIAN
from config import OS_YOCTO


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

def _basename(full_path):
    return os.path.basename(os.path.normpath(full_path))

def _get_som_folder_path(som_name, os_type, image_name):
    return {OS_YOCTO   : os.path.join(som_name, SOFTWARE, image_name),
            OS_DEBIAN  : os.path.join(som_name, SOFTWARE, OS_DEBIAN, image_name),
            OS_B2QT    : os.path.join(som_name, SOFTWARE, OS_B2QT, image_name)}[os_type]

def get_remote_path(image_path):
    image_name = _basename(image_path)
    module_name = ""
    os_type = ""

    if "mx8_" in image_name:
        module_name = "mx8"
    elif "mx8x_" in image_name:
        module_name = "mx8x"
    elif "mx8m_" in image_name:
        module_name = "mx8m"
    elif "mx8mm_" in image_name:
        module_name = "mx8mm"
    elif "mx8mn_" in image_name:
        module_name = "mx8mn"
    elif "mx8mp_" in image_name:
        module_name = "mx8mp"
    else:
        return False

    if "yocto" in image_name:
        os_type = "yocto"
    elif "debian" in image_name:
        os_type = "debian"
    elif "b2qt" in image_name:
        os_type = "b2qt"
    else:
        return False

    return _get_som_folder_path(module_name, os_type, image_name)
