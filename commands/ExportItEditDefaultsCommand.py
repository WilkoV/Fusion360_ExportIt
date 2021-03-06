import adsk.core, adsk.fusion, adsk.cam, traceback
import apper

from apper import AppObjects
from .BaseLogger import logger
from .ExportItExportDesignCommand import initializeConfiguration, initializeUi, createDefaultConfiguration, validateConfiguration, resetExportDirecotry, validateExportDirectory
from .UiHelper import getSelectedDropDownItems
from .ConfigurationHelper import writeDefaultConfiguration, logConfiguration, resetConfiguration, setDefaultConfiguration, getConfiguration
from .GithubReleaseHelper import checkForUpdates, getGithubReleaseInformation, showReleaseNotes
from .Statics import *

class ExportItEditDefaultsCommand(apper.Fusion360CommandBase):
    def on_preview(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        pass

    def on_destroy(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, reason, input_values):
        try:
            logger.info("--------------------------------------------------------------------------------")
            logger.info("Finished editing of defaults")
            logger.info("--------------------------------------------------------------------------------")

            resetConfiguration()

        except:
            logger.error("--------------------------------------------------------------------------------")
            logger.error("Error:")
            logger.error("--------------------------------------------------------------------------------")

            logger.critical(traceback.format_exc())

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input, input_values):
        logger.debug("changed_input.objectType: %s", changed_input.objectType)

        # process changed element
        if changed_input.objectType == 'adsk::core::CommandInput':
            pass
        # process changed element
        elif type(input_values[changed_input.id]) == adsk.core.ListItems:
            # element supports a list of selections. Process all selected elements
            setDefaultConfiguration(changed_input.id, getSelectedDropDownItems(inputs, changed_input.id))
        else:
            # element is a single element
            setDefaultConfiguration(changed_input.id, input_values[changed_input.id])

        # check if the integrity between configured parameters are still valid
        validateConfiguration(inputs)

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        try:
            logger.info("--------------------------------------------------------------------------------")
            logger.info("Start processing configuration")
            logger.info("--------------------------------------------------------------------------------")

            if input_values[UI_EXPORT_DIRECTORY_RESET_ID]:
                resetExportDirecotry(input_values)

            if getConfiguration(CONF_EXPORT_DIRECTORY_CONFIGURE_KEY) == UI_EXPORT_DIRECTORY_CONFIGURE_DEFAULT_VALUE:
                
                validateExportDirectory()
            
            elif (getConfiguration(CONF_EXPORT_DIRECTORY_KEY) and
                    (getConfiguration(CONF_EXPORT_DIRECTORY_CONFIGURE_KEY) == UI_EXPORT_DIRECTORY_CONFIGURE_NEW_DESIGN_VALUE
                    or getConfiguration(CONF_EXPORT_DIRECTORY_CONFIGURE_KEY) == UI_EXPORT_DIRECTORY_CONFIGURE_ALWAYS_VALUE)):
                
                setDefaultConfiguration(CONF_EXPORT_DIRECTORY_KEY, "")    

            # print configuration to the log file
            logConfiguration()

            # write configuration to the configuration file
            writeDefaultConfiguration()

        except:
            logger.error("--------------------------------------------------------------------------------")
            logger.error("Error:")
            logger.error("--------------------------------------------------------------------------------")

            logger.critical(traceback.format_exc())

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        ao = AppObjects()

        try:
            logger.info("--------------------------------------------------------------------------------")
            logger.info("Initializing edit defaults")
            logger.info("--------------------------------------------------------------------------------")

            # load or create configuration
            initializeConfiguration(None, CONF_PROJECT_ATTRIBUTE_GROUP, CONF_PROJECT_ATTRIBUTE_KEY, createDefaultConfiguration())

            # check for new version
            isCheckOverdue = checkForUpdates()
            logger.debug("isCheckOverdue %s", isCheckOverdue)
            showReleaseNotes(isCheckOverdue, ao)

            # create UI elements and populate configuration to the fields
            initializeUi(inputs, True, isCheckOverdue)

            # check if ui values are valid
            validateConfiguration(inputs)

        except:
            logger.error("--------------------------------------------------------------------------------")
            logger.error("Error:")
            logger.error("--------------------------------------------------------------------------------")

            logger.critical(traceback.format_exc())