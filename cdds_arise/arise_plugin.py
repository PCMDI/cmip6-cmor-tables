"""
A Sample module for Adding a new project to CDDS, updated for CDDS v2.2.3.

This will require MIP tables and CVs and an appropriate request JSON file.

Note that this module must be installed somehow, e.g. through inclusion in
a .pth file in your local python site-packages directory
($HOME/.local/python3.8/site-packages/cdds.pth)
"""
import logging
import os
from typing import Type

from cdds.common.plugins.file_info import ModelFileInfo, GlobalModelFileInfo
from cdds.common.plugins.grid import GridLabel
from cdds.common.plugins.models import ModelParameters
from cdds.common.plugins.plugins import CddsPlugin
from cdds.common.plugins.common import LoadResults

from cdds.common.plugins.base.base_models import BaseModelStore
from cdds.common.plugins.base.base_streams import BaseStreamInfo, BaseStreamStore

from cdds.common.plugins.cmip6.cmip6_models import (
    UKESM1_0_LL_Params, HadGEM3_GC31_LL_Params)
from cdds.common.plugins.cmip6.cmip6_grid import Cmip6GridLabel
import cdds.common.plugins.cmip6 as cmip6
from cdds.common.plugins.streams import StreamInfo


class ArisePlugin(CddsPlugin):

    def __init__(self):
        super(ArisePlugin, self).__init__("ARISE")

    def models_parameters(self, model_id: str) -> ModelParameters:
        models_store = AriseModelStore.instance()
        return models_store.get(model_id)

    def overload_models_parameters(self, source_dir: str) -> None:
        models_store = AriseModelsStore.instance()
        models_store.overload_params(source_dir)

    def grid_labels(self) -> Type[GridLabel]:
        # Use CMIP6 settings for grid labels
        return Cmip6GridLabel

    def stream_info(self) -> StreamInfo:
        stream_store = AriseStreamStore.instance()
        return stream_store.get()

    def model_file_info(self) -> ModelFileInfo:
        return GlobalModelFileInfo()


class AriseModelStore(BaseModelStore):

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


class AriseStreamInfo(BaseStreamInfo):

    def __init__(self, config_path: str = '') -> None:
        if not config_path:
            local_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(local_dir, 'data/streams/streams_config.json')
        super(AriseStreamInfo, self).__init__(config_path)


class AriseStreamStore(BaseStreamStore):
    def __init__(self) -> None:
        stream_info = AriseStreamInfo()
        super(AriseStreamStore, self).__init__(stream_info)

    @classmethod
    def create_instance(cls) -> 'AriseStreamStore':
        return AriseStreamStore()
