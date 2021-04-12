#!/usr/bin/env python


__doc__ = """ A simple CLI to annotate variants using data from Ensembl. This utility takes in a file of variants, 
 one per line, and generates a tsv file that contains the following values per variant:
   `assembly name`, `seq_region_name`, `start`, `end`, `most_severe_consequnece`, `strand`, and genes.
 """

import sys
import traceback
import argparse
import logging
from tcvariant import TcVariantAnnotation


__version__ = '0.0.1'


def get_opts():
    """ Return an argparse object. """
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--verbose', default=logging.INFO, action='store_const',
                        const=logging.DEBUG, help='enable debug logging')
    parser.add_argument('--version', action='version', version=__version__,
                        help='show version and exit')
    parser.add_argument('--variant', action='store', type=str, required=False,
                        help='individual variant to annotate')
    parser.add_argument('--input', action='store', type=str, required=False,
                        help='name of file containing list of variants')
    parser.add_argument('--output', default='tc_variant_annotations.tsv',
                        help='name of file to write annotations to')
    args = parser.parse_args()
    logging.basicConfig(level=args.verbose)
    return args


def main():
    """ script entry point """
    opts = get_opts()
    try:
        annotate = TcVariantAnnotation(output=opts.output)
        if opts.variant:
            annotate.annotate_single_variant(opts.variant)
        elif opts.input:
            annotate.annotate_variants_from_file(opts.input)
        else:
            logging.error('No variant input provided. Please provide an individual variant with the --variant parameter'
                  'or a file containing a list of variants (one per line) with the --file parameter')

    except Exception as err:
        logging.error(err)
        traceback.print_exc()
        return 255


if __name__ == '__main__':
    sys.exit(main())
