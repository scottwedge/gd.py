from pathlib import Path
import os

from ..utils._async import run_blocking_io

from ..utils.crypto.coders import Coder

from .save import SaveAPI

__all__ = ('SaveLoader', 'path')


path = Path.cwd()

try:
    local_path = Path(os.getenv('localappdata'))
    path = local_path / 'GeometryDash'

except Exception as error:
    print(
        'Failed to load local Geometry Dash path. '
        'Error: [{0.__class__.__name__}: {0}]'.format(error)
    )


class SaveLoader:
    main_data = 'CCGameManager.dat'
    level_data = 'CCLocalLevels.dat'

    def __call__(self, *args, **kwargs):
        return self.local()

    @classmethod
    async def local(cls):
        return await run_blocking_io(cls._local)

    @classmethod
    def _local(cls):
        try:
            with open(path / cls.main_data, 'rb') as main_file:
                main = Coder.decode_save(main_file.read())

            with open(path / cls.level_data, 'rb') as level_file:
                levels = Coder.decode_save(level_file.read())

            return SaveAPI(main, levels)

        except FileNotFoundError:
            print('Failed to find save files in the path: {!r}.'.format(str(path)))


SaveLoader = SaveLoader()