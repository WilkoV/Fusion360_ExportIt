"""
Apper Fusion 360 API Wrapper
============================
Apper a simple wrapper for the Fusion 360 API,
written in Python, for human beings.

Full documentation is at <https://apper.readthedocs.io>.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:copyright: (c) 2019 by Patrick Rainsberry.
:license: Apache 2.0, see LICENSE for more details.

"""

try:
    from .FusionApp import FusionApp
    from .Fusion360AppEvents import Fusion360CustomEvent
    from .Fusion360AppEvents import Fusion360CustomThread
    from .Fusion360AppEvents import Fusion360NewThread
    from .Fusion360AppEvents import Fusion360DocumentEvent
    from .Fusion360AppEvents import Fusion360WorkspaceEvent
    from .Fusion360AppEvents import Fusion360WebRequestEvent
    from .Fusion360AppEvents import Fusion360CommandEvent
    from .Fusion360AppEvents import Fusion360ActiveSelectionEvent
    from .Fusion360CommandBase import Fusion360CommandBase
    from .PaletteCommandBase import PaletteCommandBase
    from .Fusion360CustomFeatureBase import Fusion360CustomFeatureBase
    from .Fusion360Utilities import AppObjects
    from .Fusion360Utilities import *
    from .Fusion360DebugUtilities import *
    from .Fusion360PipInstaller import check_dependency, install_from_list, install_from_requirements

except:
    pass
