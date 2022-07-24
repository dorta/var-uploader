# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import textwrap
import sys

from config import *

def args_parser():
    parser = ArgumentParser(
       description="Variscite Recovery SD Card Uploader Tool",
       prog='varuploader',
       formatter_class=RawDescriptionHelpFormatter,
       epilog=textwrap.dedent(
         '''1. To set up the FTP login credentials, please run the var-uploader tool with the following arguments:\n\n''' \
         '''$ varuploader --user <user> --passwd <password>\n\n''' \
         '''2. To upload a new recovery SD card using the var-uploader tool, please use the following arguments:\n\n''' \
         '''$ varuploader --som <som_name> --os <os_name> --image <recovery_sd_card_file>\n\n''' \
         '''For more information, please visit the github.com/dorta/var-uploader page.\n\n''' \
         '''Copyright 2022 Variscite LTD'''
       )
    )
    parser.add_argument(
       "--som",
       choices=VAR_SYSTEM_ON_MODULES,
       help='Choose one System on Modules (DART/VAR-SOM) within the list.',
       type=str,
       required=False
    )
    parser.add_argument(
        "--os",
        choices=VAR_OS,
        help='Choose one Operating System within the list.',
        type=str,
        required="--som" in sys.argv
    )
    parser.add_argument(
        "--image",
        help="Specify the recovery SD card to be uploaded to the FTP",
        type=str,
        required="--som" in sys.argv
    )
    parser.add_argument(
        "--user",
        help='User to login to the Variscite FTP',
        type=str
    )
    parser.add_argument(
        "--passwd",
        help='Password to login to the Variscite FTP',
        type=str
    )
    return parser, parser.parse_args()
