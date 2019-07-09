#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is Python console script to perform a globus transfer

Example:
```
```
"""

import os
import sys
import argparse
import logging
import time
import brown_globus_utils.utils as globus_utils
from brown_globus_utils import __version__

_logger = logging.getLogger(__name__)

def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Convinience script to submit a globus transfer ")
    parser.add_argument(
        '--version',
        action='version',
        version='brown_globus_utils {ver}'.format(ver=__version__))
    parser.add_argument(
        dest="source_name",
        help="Source Endpoint",
        type=str)
    parser.add_argument(
        dest="target_name",
        help="Target Endpoint",
        type=str)
    parser.add_argument(
        dest="source_loc",
        help="Location of source directory or file",
        type=str)
    parser.add_argument(
        dest="target_loc",
        help="Location of target diirectory or file",
        type=str)
    parser.add_argument(
        '--isfile',
        dest="isfile",
        help="flag to indicate that transfer is for a single file",
        action='store_true')
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main(args):
    """Main entry point allowing external calls

    Args:
      args ([str]): command line parameter list
    """
    args = parse_args(args)
    setup_logging(args.loglevel)
    tc = globus_utils.get_tc()
    # globus_utils.print_endpoints(tc)
    transfer_id = globus_utils.transfer_sync(tc, args.source_name, args.target_name,args.source_loc, args.target_loc, args.isfile)
    
    _logger.info("--------------------------------------------")
    _logger.info("task_id =" + transfer_id)
    _logger.info("--------------------------------------------")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()