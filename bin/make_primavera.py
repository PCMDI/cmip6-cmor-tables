"""
SYNOPSIS

    make_primavera.py

DESCRIPTION

    Copy the CMOR3 MIP table JSON files and generate the additional PRIMAVERA
    tables.

REQUIREMENTS

    Requires the openpyxl Python library. Tested with openpyxl version 2.4.1
"""
import json
import os
from pprint import pprint

from openpyxl import load_workbook


SRC_FILE = 'CMIP6_3hr.json'

EXCEL_FILE = 'PRIMAVERA_MS21_DRQ_0-beta-37.1.xlsx'


def main():
    """
    Run the software
    """
    with open(SRC_FILE) as src_file:
        src_data = json.load(src_file)
    pprint(src_data)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.abspath(current_dir,
                                 os.path.join('..', 'etc', EXCEL_FILE))
    data_req = load_workbook(excel_path)





if __name__ == '__main__':
    main()

