import adsk.core, adsk.fusion, adsk.cam, traceback
import apper

from apper import AppObjects
from .BaseLogger import logger
from .UiHelper import addGroup, addStringInputToGroup, addBoolInputToGroup, addCheckBoxDropDown, selectDropDownItemByNames, getSelectedDropDownItems, addTextListDropDown, getSelectedDropDownItem
from .ConfigurationHelper import initializeConfiguration, getConfiguration, setConfiguration, writeConfiguration, showSaveConfigWarning, resetConfiguration, logConfiguration
from .Statics import *

def createDefaultConfiguration():
    logger.debug("creating default configuration")

    # create default configuration
    defaultConfiguration = {}

    # common attributes
    defaultConfiguration[CONF_VERSION_KEY] = CONF_VERSION_DEFAULT

    # export directory options
    defaultConfiguration[CONF_EXPORT_DIRECTORY_KEY] = CONF_EXPORT_DIRECTORY_DEFAULT

    return defaultConfiguration

def initializeUi(inputs :adsk.core.CommandInputs):
    pass

class ExportItExportDesignCommand(apper.Fusion360CommandBase):
    def on_preview(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        pass

    def on_destroy(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, reason, input_values):
        try:
            ao = AppObjects()
            designName = ao.design.rootComponent.name
            projectName = ao.app.activeDocument.dataFile.parentProject.name

            logger.info("--------------------------------------------------------------------------------")
            logger.info("Finished processing of %s - %s", projectName, designName)
            logger.info("--------------------------------------------------------------------------------")

            resetConfiguration()

        except:
            logger.info("--------------------------------------------------------------------------------")
            logger.info("Finished")
            logger.info("--------------------------------------------------------------------------------")

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input, input_values):
        # process changed element
        if type(input_values[changed_input.id]) == adsk.core.ListItems:
            # element supports a list of selections. Process all selected elements
            setConfiguration(changed_input.id, getSelectedDropDownItems(inputs, changed_input.id))
        else:
            # element is a single element
            setConfiguration(changed_input.id, input_values[changed_input.id])

        # check if the integrity between configured parameters are still valid
        checkDataIntegrity(inputs)

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        try:
            if not getConfiguration(CONF_EXPORT_DIRECTORY_KEY):
                return

            ao = AppObjects()
            rootComponent = ao.design.rootComponent
            designName = rootComponent.name
            projectName = ao.app.activeDocument.dataFile.parentProject.name

            logger.info("--------------------------------------------------------------------------------")
            logger.info("Starting processing of %s - %s", projectName, designName)
            logger.info("--------------------------------------------------------------------------------")

            # write modified configuration
            writeConfiguration(ao.document, CONF_PROJECT_ATTRIBUTE_GROUP, CONF_PROJECT_ATTRIBUTE_KEY)

            #print configuration to the log file
            logConfiguration()

        except:
            logger.critical(traceback.format_exc())

        showSaveConfigWarning()

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        ao = AppObjects()
        designName = ""
        projectName = ""

        try:
            designName = ao.design.rootComponent.name
            projectName = ao.app.activeDocument.dataFile.parentProject.name

            logger.info("--------------------------------------------------------------------------------")
            logger.info("Initializing processing of %s - %s", projectName, designName)
            logger.info("--------------------------------------------------------------------------------")

            # load or create configuration
            initializeConfiguration(ao.document, CONF_PROJECT_ATTRIBUTE_GROUP, CONF_PROJECT_ATTRIBUTE_KEY, createDefaultConfiguration())

            # create UI elements and populate configuration to the fields
            initializeUi(inputs)

        except AttributeError as err:
            logger.error("--------------------------------------------------------------------------------")
            logger.error("Error: No active document found.")
            logger.error("--------------------------------------------------------------------------------")

            if ao.ui:
                ao.ui.messageBox("Error: No active document found.")
        except:
            logger.error("--------------------------------------------------------------------------------")
            logger.error("Error:")
            logger.error("--------------------------------------------------------------------------------")

            logger.critical(traceback.format_exc())