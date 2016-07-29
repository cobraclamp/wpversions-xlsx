#!/usr/local/bin/python2.7
import argparse
from wpversionscanner.wpvscanner import Scanner
from wpversionscanner.wpvexcel import Xlsx

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Download Sites File from server.'
    )

    parser.add_argument(
        '-d', '--domains',
        help="File containing domains on new line",
        default="sites.txt",
        action="store", nargs=1, dest="domain_list",
        required=True
    )

    args = parser.parse_args()
    scanner = Scanner(args.domain_list[0])
    versions = scanner.check_domains()

    xlsx = Xlsx(versions, "sites")

    xlsx.write_excel()
