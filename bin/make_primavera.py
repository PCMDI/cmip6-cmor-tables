"""
make_primavera.py

Copy the CMOR3 MIP table JSON files and generate the additional PRIMAVERA tables.
"""
import json
from pprint import pprint


SRC_FILE = 'CMIP6_3hr.json'


def main():
    """
    Run the software
    """
    with open(SRC_FILE) as src_file:
        data = json.load(src_file)
    pprint(data)



if __name__ == '__main__':
    main()

