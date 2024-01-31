# -*- coding: utf-8 -*-
import os
import json
import argparse
from collections import OrderedDict


# List of files needed from github for CMIP6 CV
# ---------------------------------------------
filelist = [ 
        "CMIP6_required_global_attributes.json",
        "CMIP6_activity_id.json",
        "CMIP6_institution_id.json",
        "CMIP6_source_id.json",
        "CMIP6_source_type.json",
        "CMIP6_frequency.json",
        "CMIP6_grid_label.json",
        "CMIP6_nominal_resolution.json",
        "CMIP6_realm.json",
        "CMIP6_table_id.json",
        "CMIP6_license.json",
        "CMIP6_DRS.json",
        "mip_era.json",
        "CMIP6_sub_experiment_id.json",
        "CMIP6_experiment_id.json"
        ]

class readWCRP():
    def __init__(self):
        pass

    def createSource(self, myjson):
        root = myjson['source_id']
        for key in root.keys():
            root[key]['source']=root[key]['label'] + ' (' + root[key]['release_year'] + '): ' + chr(10)
            for realm in root[key]['model_component'].keys():
                if( root[key]['model_component'][realm]['description'].find('None') == -1):
                    root[key]['source'] += realm + ': ' 
                    root[key]['source'] += root[key]['model_component'][realm]['description'] + chr(10)
            root[key]['source'] = root[key]['source'].rstrip()
            del root[key]['label']
            del root[key]['release_year']
            del root[key]['label_extended']
            del root[key]['model_component']

    def createExperimentID(self, myjson):
        #
        # Delete undesirable attribute for experiement_id
        #
        root = myjson['experiment_id']
        for key in root.keys():
            del root[key]['tier']
            del root[key]['start_year']
            del root[key]['end_year']
            del root[key]['description']
            del root[key]['min_number_yrs_per_sim']

    def createLicense(self,myjson):
        #
        # Create regex templates for validating license values in CMOR
        #
        # root = myjson['license']
        # base_template = root['license']
        # license_templates = []
        # for key, value in root['license_options'].items():
        #     tmp = base_template.replace(". ", ". *")
        #     tmp = tmp.replace("<Creative Commons; select and insert a license_id; see below>", value['license_id'])
        #     tmp = tmp.replace("<insert the matching license_url; see below>", value['license_url'])
        #     tmp = tmp.replace(".", "\\.")
        #     tmp = tmp.replace("<Your Institution; see CMIP6_institution_id\\.json>", ".*")
        #     tmp = tmp.replace("[ and at <some URL maintained by modeling group>]", ".*")
        #     license_template = "^{}$".format(tmp)
        #     license_templates.append(license_template)
        # myjson['license'] = license_templates

        myjson['license'] =  [
                                "^CMIP6 model data produced by .* is licensed under a Creative Commons .* License (https://creativecommons\\.org/.*)\\. " \
                                "*Consult https://pcmdi\\.llnl\\.gov/CMIP6/TermsOfUse for terms of use governing CMIP6 output, including citation " \
                                "requirements and proper acknowledgment\\. *Further information about this data, including some limitations, can be found via " \
                                "the further_info_url (recorded as a global attribute in this file).*\\. *The data producers and data providers make no warranty, " \
                                "either express or implied, including, but not limited to, warranties of merchantability and fitness for a particular purpose\\. *All " \
                                "liabilities arising from the supply of the information (including any liability arising in negligence) are excluded to the fullest " \
                                "extent permitted by law\\.$"
                            ]

    def readCVFiles(self, cmip6_cv_dir):
        Dico = OrderedDict()
        for file_name in filelist:
            file_path = os.path.join(cmip6_cv_dir, file_name)
            with open(file_path, "r") as f:
                myjson = json.load(f, object_pairs_hook=OrderedDict)
                if(file_name == 'CMIP6_source_id.json'):
                    self.createSource(myjson)
                if(file_name == 'CMIP6_experiment_id.json'):
                    self.createExperimentID(myjson)
                self.createLicense(myjson)
                Dico.update(myjson)
         
        finalDico = OrderedDict()
        finalDico['CV'] = Dico
        return finalDico

def build_cv_file(cmip6_cv_dir, output_dir):

    cv_filepath = os.path.join(output_dir, "CMIP6_CV.json")
    f = open(cv_filepath, "w")
    gather = readWCRP()
    CV = gather.readCVFiles(cmip6_cv_dir)
    regexp = OrderedDict()
    regexp["mip_era"] = [ "CMIP6" ]
    regexp["product"] = [ "model-output" ]
    regexp["tracking_id"] = [ "hdl:21.14100/.*" ]  
    regexp["further_info_url"] = [ "https://furtherinfo.es-doc.org/.*" ]
    regexp["realization_index"] = [ "^\\[\\{0,\\}[[:digit:]]\\{1,\\}\\]\\{0,\\}$" ]
    regexp["variant_label"] = ["r[[:digit:]]\\{1,\\}i[[:digit:]]\\{1,\\}p[[:digit:]]\\{1,\\}f[[:digit:]]\\{1,\\}$" ]
    regexp["data_specs_version"] = [ "^[[:digit:]]\\{2,2\\}\\.[[:digit:]]\\{2,2\\}\\.[[:digit:]]\\{2,2\\}$" ]
    regexp["Conventions"] = [ "^CF-1.7 CMIP-6.[0-2]\\( UGRID-1.0\\)\\{0,\\}$" ]
    regexp["forcing_index"] = [ "^\\[\\{0,\\}[[:digit:]]\\{1,\\}\\]\\{0,\\}$" ]
    regexp["initialization_index"] = [ "^\\[\\{0,\\}[[:digit:]]\\{1,\\}\\]\\{0,\\}$" ]
    regexp["physics_index"] = [ "^\\[\\{0,\\}[[:digit:]]\\{1,\\}\\]\\{0,\\}$" ]


    CV['CV'].update(regexp)
    for exp in CV["CV"]["experiment_id"]:
        CV["CV"]["experiment_id"][exp]["activity_id"] = [ " ".join(CV["CV"]["experiment_id"][exp]["activity_id"])]
        print("AC ID:",CV["CV"]["experiment_id"][exp]["activity_id"])
    f.write(json.dumps(CV, indent=4, separators=(',', ':'), sort_keys=False) )

    f.close()

def main():
    parser = argparse.ArgumentParser(description="Create CMIP6_CV.json from the WCRP-CMIP/CMIP6_CVs repo at https://github.com/PCMDI/cmip6-cmor-tables")
    parser.add_argument("--cmip6_cv_dir", "-c", dest="cmip6_cv_dir", type=str, default='./CMIP6_CVs', help="WCRP CMIP6 CV directory (default is ./CMIP6_CVs)")
    parser.add_argument("--output_dir", "-o", dest="output_dir", type=str, default=os.path.curdir, help="Output directory (default is current directory)")
    args = parser.parse_args()

    if not os.path.isdir(args.cmip6_cv_dir):
        print("{} is not a directory. Exiting.".format(args.cmip6_cv_dir))
        return

    if not os.path.isdir(args.output_dir):
        print("{} is not a directory. Exiting.".format(args.output_dir))
        return

    build_cv_file(args.cmip6_cv_dir, args.output_dir)

if __name__ == '__main__':
    main()
