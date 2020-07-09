import adsk.core, traceback
import os, sys

app_path = os.path.dirname(__file__)

sys.path.insert(0, app_path)
sys.path.insert(0, os.path.join(app_path, 'apper'))

try:
    import config
    import apper

    # Basic Fusion 360 Command Base samples
    from .commands.ExportItExportDesignCommand import ExportItExportDesignCommand

# Create our addin definition object
    my_addin = apper.FusionApp(config.app_name, config.company_name, False)

    my_addin.add_command(
        'Export Design',
        ExportItExportDesignCommand,
        {
            'cmd_description': 'Export a design into several formats',
            'cmd_id': 'exportIt_design_cmd_id',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Commands',
            'cmd_resources': 'exportIt_export_designs_icons',
            'command_visible': True,
            'command_promoted': True,
        }
    )

    app = adsk.core.Application.cast(adsk.core.Application.get())
    ui = app.userInterface

except:
    app = adsk.core.Application.get()
    ui = app.userInterface
    if ui:
        ui.messageBox('Initialization: {}'.format(traceback.format_exc()))

# Set to True to display various useful messages when debugging your app
debug = False

def run(context):
    my_addin.run_app()

def stop(context):
    my_addin.stop_app()
    sys.path.pop(0)
    sys.path.pop(0)
