# -*- coding: utf-8 -*-
# ##################################
#   ____                     _     #
#  / ___|___  _ __ ___   ___| |_   #
# | |   / _ \| '_ ` _ \ / _ \ __|  #
# | |__| (_) | | | | | |  __/ |_   #
#  \____\___/|_| |_| |_|\___|\__|  #
#                                  #
#        Copyright (c) 2023        #
#      rd2md Development Team      #
#       All rights reserved        #
####################################

import argparse
import os

from .parser import rd2md


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("input_folder")
    parser.add_argument("output_folder")
    parser.add_argument("filenames", nargs="+", type=str)

    args = parser.parse_args()

    for filename in args.filenames:
        file_in = os.path.join(args.input_folder, "%s.Rd" % filename)
        file_out = os.path.join(args.output_folder, "%s.md" % filename)
        rd2md(file_in, file_out, filename[0].isupper())


if __name__ == "__main__":
    main()
