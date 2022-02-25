import datetime
import json
import os

input_mip_era = 'CMIP6'
output_mip_era = 'ARISE'

today = datetime.datetime.now().strftime('%d %b %Y')

files_to_rename_only = [
    '_CV.json',
    '_coordinate.json',
    '_formula_terms.json',
    '_input_example.json']

for filename in os.listdir('.'):
    new_filename = filename.replace(input_mip_era, output_mip_era)
    if filename.replace(input_mip_era, '') not in files_to_rename_only:

        with open(filename, 'r') as fh:
            file_json = json.load(fh)

        file_json['Header']['table_date'] = today
        file_json['Header']['mip_era'] = output_mip_era

        with open(filename, 'w') as fh:
            fh.write(json.dumps(file_json, indent=4, sort_keys=False))


    print('git mv {} {}'.format(filename, new_filename))
