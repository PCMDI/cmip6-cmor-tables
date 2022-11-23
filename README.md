# UKESM1 ARISE-SAI project

A project description and other details are available via the [wiki](https://github.com/MetOffice/arise-cmor-tables/wiki) in this repository.

# UKESM1 ARISE-SAI data

CMOR standardised data from the UKESM1 ARISE-SAI simulations is now available for download from the [CEDA archive](https://catalogue.ceda.ac.uk/uuid/26b89d8d76bd40bfbaf9fedfa383e9cf).

A searchable table describing all possible variables is available [here](https://metoffice.github.io/arise-cmor-tables/), but note that only a subset of these were produced. A list of all variables produced can be found [here](https://github.com/MetOffice/arise-cmor-tables/wiki/List-of-variables-prepared-for-ARISE).

# CMOR tables for ARISE

The tables here were forked from the [PCMDI/cmip6-cmor-tables](https://github.com/PCMDI/cmip6-cmor-tables) repository and adapted to allow data to be output for the ARISE SAI project. The changes made to the MIP tables are restricted to the mip era, with changes related to the activity id (`ARISE`), license text and experiment id (`arise-sai-1p5`) made to the CVs file.

In addition the CDDS plugin used to drive the post-processing is included here (works with v2.2.2)

