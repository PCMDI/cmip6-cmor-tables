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

from openpyxl import load_workbook


EXCEL_FILE = 'PRIMAVERA_MS21_DRQ_0-beta-37.5.xlsx'


def main():
    """
    Run the software
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    excel_path = os.path.abspath(os.path.join(current_dir, '..',
                                              'etc', EXCEL_FILE))
    data_req = load_workbook(excel_path)

    tables = [{'name': 'prim3hr', 'src_json': 'CMIP6_3hr.json'}]

    for table in tables:
        output = {}

        # load the existing JSON table that our output will be based upon
        src_path = os.path.abspath(
            os.path.join(current_dir, '..', 'Tables', table['src_json']))
        with open(src_path) as src_file:
            src_data = json.load(src_file)

        # choose the corresponding worksheet from the Excel data request
        req_sheet = data_req[table['name']]

        # copy the header section and update the table_id with the
        # PRIMAVERA table name
        output['Header'] = src_data['Header']
        output['Header']['table_id'] = 'Table {}'.format(table['name'])

        # write out the new PRIMAVERA table JSON file
        output_json_name = 'CMIP6_{}.json'.format(table['name'])
        output_path = os.path.abspath(
            os.path.join(current_dir, '..', 'Tables', output_json_name))
        with open(output_path, 'w') as dest_file:
            json.dump(output, dest_file, indent=4)


if __name__ == '__main__':
    main()

