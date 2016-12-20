"""
SYNOPSIS

    make_primavera.py

DESCRIPTION

    Generate the additional PRIMAVERA mip tables for CMOR version 3.

REQUIREMENTS

    Requires the openpyxl Python library. Tested with openpyxl version 2.4.1
"""
import json
import os

from openpyxl import load_workbook


EXCEL_FILE = 'PRIMAVERA_MS21_DRQ_0-beta-37.5.xlsx'

HEADER_COMMON = {
    'data_specs_version': '01.beta.45',
    'cmor_version': '3.2',
    'table_date': '19 December 2016',
    'missing_value': '1e20',
    'product': 'output',
    'approx_interval': '0.125000',
    'generic_levels': '',
    'mip_era': 'CMIP6',
    'Conventions': 'CF-1.6 CMIP-6.0'
    }


def generate_header(header, table_name):
    """
    Populate the `Header` section of the output dictionary with the
    variables in the PRIMAVERA mip table passed in to `req_sheet`.

    :param dict header: The dictionary that is the value `Header` key
    :param str table_name: The name of table being generated
    """
    table_name_parts = table_name
    table_name_parts.strip('prim')

    # copy the standard header items into the header
    header.update(HEADER_COMMON)

    # set the table name
    header['table_id'] = 'Table {}'.format(table_name)

    # set the frequency
    # 1 hour should be 0.041666 but existing files use 0.017361 and so have
    # stuck with that
    frequencies = {'mon': '30.00000', 'day': '1.00000', '6hr': '0.250000',
                   '3hr': '0.125000', '1hr': '0.017361'}
    for freq in frequencies:
        if freq in table_name.lower():
            header['frequency'] = freq
            table_name_parts.strip(freq)
            break

    if 'frequency' not in header:
        msg = ('Unable to determine frequency for table name: {}'.
               format(table_name))
        raise ValueError(msg)

    # set the realm
    if table_name_parts.startswith('O'):
        realm = 'ocean'
    elif table_name_parts.startswith('SI'):
        realm = 'seaIce'
    else:
        realm = 'atmos'

    header['realm'] = realm

    # set the approx_interval
    header['approx_interval'] = frequencies[header['frequency']]


def generate_variable_entry(req_sheet, output):
    """
    Populate the `variable_entry` section of the `output` dictionary with the
    variables in the PRIMAVERA mip table passed in to `req_sheet`.

    :param openpyxl.worksheet.worksheet.Worksheet req_sheet: A worksheet from
        the Data Request spreadsheet
    :param dict output: The `variable_entry` dictionary from the output
        dictionary that will be converted to a JSON file
    """


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
        # create a blank output dictionary
        output = {}

        # choose the corresponding worksheet from the Excel data request
        req_sheet = data_req[table['name']]

        # add the Header dictionary
        output['Header'] = {}
        generate_header(output['Header'], table['name'])

        # add the variables
        output['variable_entry'] = {}
        generate_variable_entry(req_sheet, output['variable_entry'])

        # write the new JSON file for the PRIMAVERA table
        output_json_name = 'CMIP6_{}.json'.format(table['name'])
        output_path = os.path.abspath(
            os.path.join(current_dir, '..', 'Tables', output_json_name))
        with open(output_path, 'w') as dest_file:
            json.dump(output, dest_file, indent=4)


if __name__ == '__main__':
    main()

