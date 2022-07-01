# (C) British Crown Copyright 2022, Met Office.
# Please see LICENSE.rst for license details.
import argparse
import glob
import json
import os
import textwrap

from datetime import datetime

from constants import (HEADINGS, HEADER_ROW_TEMPLATE, ROW_TEMPLATE, CELL_TEMPLATE, TABLE_TEMPLATE, BGCOLORS, HEADER,
                       FOOTER, WRAP_SIZE)


def parse_args():
    """
    Parse the user arguments.

    Returns
    -------
    args : argparse.Namespace
        User arguments.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('-t',
                        '--tables_directory',
                        help='Directory of the mip tables to generate a HTML page for.',
                        type=str,
                        required=True)
    parser.add_argument('-p',
                        '--prefix',
                        help='Prefix used on the mip table json files.',
                        type=str,
                        required=True)
    parser.add_argument('-o',
                        '--output_directory',
                        help='Output location of the generated HTML page.',
                        type=str,
                        required=True)
    args = parser.parse_args()

    return args


def get_mip_tables(tables_directory, prefix):
    """
    Loop over all json files in a directory matching {prefix}_*.json and add their
    namd a filepath to a dictionary if they contain a "variable_entry" key.

    Parameters
    ----------
    tables_directory : str
        Path to the mip tables.
    prefix : str
        Prefix used on table josn files.
    Returns
    -------
    tables_with_variables : dict
        A dictionary with table name as key and path to the table as value.
    """
    glob_string = os.path.join(tables_directory, '{}_*.json'.format(prefix))
    mip_table_json = glob.glob(glob_string)

    tables_with_variables = {}

    excluded_tables = ['grids', 'formula_terms', 'coordinate', 'CV']

    for table_path in mip_table_json:
        table_name = os.path.basename(table_path).split('_')[1].split('.json')[0]
        with open(table_path, 'r') as f:
            table_json = json.loads(f.read())

        if "variable_entry" in table_json.keys() and table_name not in excluded_tables:
            tables_with_variables[table_name] = table_path

    return tables_with_variables


def extract_table_data(tables):
    """
    Using the table name and filepath mappings, read the data for each entry in "variable_entry"
    and extract the relevant values for the headings and save them as a list.

    Parameters
    ----------
    tables : dict
        A dictionary with table name as key and path to the table as value.
    Returns
    -------
    tables_data : list
        List of lists where each sublist contains a list representing a variable and the
        metadata from the miptable entry.
    """
    table_data = [HEADINGS]

    for table, table_path in tables.items():
        with open(table_path, 'r') as f:
            variable_entry = json.loads(f.read())["variable_entry"]
            for variable, metadata in variable_entry.items():
                table_data.append([table,
                                   variable,
                                   metadata['frequency'],
                                   metadata['dimensions'],
                                   metadata['standard_name'],
                                   metadata['long_name'],
                                   metadata['comment'],
                                   metadata['modeling_realm'],
                                   metadata['units'],
                                   metadata['positive'],
                                   metadata['cell_methods'],
                                   metadata['cell_measures']])

    return table_data


def wrap_standard_name(input_text):
    """
    Wraps the input text of a standard name.

    Parameters
    ----------
    input_text : str
        The standard name string to be wrapped.
    Returns
    -------
    wrapped_input_text : str
        The standard name string wrapped if need.
    """

    if len(input_text) > WRAP_SIZE:
        wrapped_input_text = ' '.join(input_text.split('_'))
        wrapped_input_text = textwrap.wrap(wrapped_input_text, width=WRAP_SIZE, break_long_words=False)
        wrapped_input_text = "\n_".join(["_".join(x.split()) for x in wrapped_input_text])
        return wrapped_input_text
    else:
        return input_text


def wrap_comment(input_text):
    """
    Wraps the input text of a comment.

    Parameters
    ----------
    input_text : str
        The standard name string to be wrapped.
    Returns
    -------
    wrapped_input_text : str
        The standard name string wrapped if need.
    """

    if len(input_text) > WRAP_SIZE:
        wrapped_input_text = textwrap.wrap(input_text, width=WRAP_SIZE, break_long_words=True)
        wrapped_input_text = "\n".join(wrapped_input_text)
        return wrapped_input_text
    else:
        return input_text


def display_data(data, prefix):
    """
    Returns a HTML document with a table for displaying the supplied data.
    Standard name and comment fields need separate formatting.

    Parameters
    ----------
    data : list
        Lists of lists where each sublist is a mip table variable.
    prefix : str
        The name of the mip tables.
    Returns
    -------
    html : str
        A string representing a HTML document that can be written out.
    """

    html = ''
    for i, row in enumerate(data):
        cell_type = 'th' if i == 0 else 'td'
        row_html = ''
        if i == 0:
            for entry in row:
                row_html += CELL_TEMPLATE.format(cell_type, entry)
            html += HEADER_ROW_TEMPLATE.format(BGCOLORS[i % len(BGCOLORS)], row_html)
            continue
        for x, entry in enumerate(row):
            if x == 4:
                row_html += CELL_TEMPLATE.format(cell_type, wrap_standard_name(entry))
            elif x == 6:
                row_html += CELL_TEMPLATE.format(cell_type, wrap_comment(entry))
            else:
                row_html += CELL_TEMPLATE.format(cell_type, entry)

        html += ROW_TEMPLATE.format(BGCOLORS[i % len(BGCOLORS)], row_html)

    table = TABLE_TEMPLATE.format(html)
    timestamp = datetime.now().strftime('%H:%M %d/%m/%Y')
    html = (HEADER +
            '<h2>{} MIP Tables (Generated {})</h2>'.format(prefix, timestamp) +
            '<p>Use the search box to filter rows, e.g. search for "tas" or "Amon tas".</p>' +
            table +
            FOOTER)

    return html


if __name__ == '__main__':
    arguments = parse_args()
    tables_directory = arguments.tables_directory
    prefix = arguments.prefix

    tables = get_mip_tables(tables_directory, prefix)
    table_data = extract_table_data(tables)
    html = display_data(table_data, prefix)

    output_filepath = os.path.join(arguments.output_directory, 'mip_table_viewer_{}.html'.format(prefix))

    with open(output_filepath, 'w') as f:
        f.write(html)
