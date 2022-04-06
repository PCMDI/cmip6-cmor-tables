"""
A Sample module for Adding a new project to CDDS.

This will require MIP tables and CVs and an appropriate request JSON file.

Note that this module must be installed somehow, e.g. through inclusion in
a .pth file in your local python site-packages directory
($HOME/.local/python3.8/site-packages/cdds.pth)
"""
import logging
import os
from typing import Type

from cdds_common.cdds_plugins.grid import GridLabel
from cdds_common.cdds_plugins.models import ModelParameters
from cdds_common.cdds_plugins.plugins import CddsPlugin
try:
    from cdds_common.cdds_plugins.common import LoadResults
except ModuleNotFoundError:
    from cdds_common.cdds_plugins.cmip.common import LoadResults

from cdds_common.cdds_plugins.cmip.cmip_models import CmipModelStore

from cdds_common.cdds_plugins.cmip.cmip6.cmip6_models import (
    UKESM1_0_LL_Params, HadGEM3_GC31_LL_Params)
from cdds_common.cdds_plugins.cmip.cmip6.cmip6_grid import Cmip6GridLabel
from cdds_common.cdds_plugins.cmip.cmip6.cmip6_models import Cmip6ModelsStore
import cdds_common.cdds_plugins.cmip.cmip6 as cmip6


class ArisePlugin(CddsPlugin):

    def __init__(self):
        super(ArisePlugin, self).__init__("arise")

    def models_parameters(self, model_id: str) -> ModelParameters:
        models_store = AriseModelStore.instance()
        return models_store.get(model_id)

    def overload_models_parameters(self, source_dir: str) -> None:
        models_store = AriseModelsStore.instance()
        models_store.overload_params(source_dir)

    def grid_labels(self) -> Type[GridLabel]:
        # Use CMIP6 settings for grid labels
        return Cmip6GridLabel


class AriseModelStore(CmipModelStore):

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        models_to_include = [
            UKESM1_0_LL_Params(),
            HadGEM3_GC31_LL_Params(),
        ]
        super(AriseModelStore, self).__init__(models_to_include)

    @classmethod
    def create_instance(cls) -> 'AriseModelsStore':
        return AriseModelStore()

    def _load_default_params(self) -> None:
        local_dir = os.path.dirname(os.path.abspath(cmip6.__file__))
        # alternative
        # local_dir = os.path.dirname(os.path.abspath(_file__))
        # then the file <local_dir>/data/model/<source_id>.json must exist
        default_dir = os.path.join(local_dir, 'data/model')
        results = self.overload_params(default_dir)
        self._process_load_results(results)

    def _process_load_results(self, results: LoadResults) -> None:
        if results.unloaded:
            template = ('Failed to load model parameters for model "{}" from '
                        'file: "{}"')
            error_messages = [
                template.format(model_id, path)
                for model_id, path in results.unloaded.items()
            ]
            self.logger.critical('\n'.join(error_messages))
            raise RuntimeError('\n'.join(error_messages))
