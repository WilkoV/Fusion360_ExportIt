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

    defaultConfiguration[CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_KEY] = CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_DEFAULT
    defaultConfiguration[CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_KEY] = CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_DEFAULT

    # stl options
    defaultConfiguration[CONF_STL_STRUCTURE_KEY] = CONF_STL_STRUCTURE_DEFAULT
    defaultConfiguration[CONF_STL_REFINEMENT_KEY] = CONF_STL_REFINEMENT_DEFAULT

    # filename options
    defaultConfiguration[CONF_FILENAME_ADD_PROJECT_NAME_KEY] = CONF_FILENAME_ADD_PROJECT_NAME_DEFAULT
    defaultConfiguration[CONF_FILENAME_ADD_DESIGN_NAME_KEY] = CONF_FILENAME_ADD_DESIGN_NAME_DEFAULT

    defaultConfiguration[CONF_FILENAME_REMOVE_VERSION_TAGS_KEY] = CONF_FILENAME_REMOVE_VERSION_TAGS_DEFAULT
    defaultConfiguration[CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_KEY] = CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_DEFAULT
    defaultConfiguration[CONF_FILENAME_ELEMENT_SEPERATOR_KEY] = CONF_FILENAME_ELEMENT_SEPERATOR_DEFAULT

    return defaultConfiguration

def initializeUi(inputs :adsk.core.CommandInputs):
    # stl export
    addGroup(inputs, UI_STL_OPTIONS_GROUP_ID, UI_STL_OPTIONS_GROUP_NAME, True)
    addCheckBoxDropDown(inputs, UI_STL_OPTIONS_GROUP_ID, CONF_STL_STRUCTURE_KEY, UI_STL_STRUCTURE_NAME, UI_STL_STRUCTURE_VALUES, getConfiguration(CONF_STL_STRUCTURE_KEY))
    addCheckBoxDropDown(inputs, UI_STL_OPTIONS_GROUP_ID, CONF_STL_REFINEMENT_KEY, UI_STL_REFINEMENT_NAME, UI_STL_REFINEMENT_VALUES, getConfiguration(CONF_STL_REFINEMENT_KEY))

    # export directory
    addGroup(inputs, UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID, UI_EXPORT_DIRECTORY_OPTIONS_GROUP_NAME, True)

    addStringInputToGroup(inputs, UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID, CONF_EXPORT_DIRECTORY_KEY, UI_EXPORT_DIRECTORY_NAME, getConfiguration(CONF_EXPORT_DIRECTORY_KEY))

    addBoolInputToGroup(inputs, UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID, CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_KEY, UI_EXPORT_DIRECTORY_ADD_PROJECT_NAME_NAME, getConfiguration(CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_KEY))
    addBoolInputToGroup(inputs, UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID, CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_KEY, UI_EXPORT_DIRECTORY_ADD_DESIGN_NAME_NAME, getConfiguration(CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_KEY))

    # filename options
    addGroup(inputs, UI_FILENAME_OPTIONS_GROUP_ID, UI_FILENAME_OPTIONS_GROUP_NAME, True)

    addBoolInputToGroup(inputs, UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_ADD_PROJECT_NAME_KEY, UI_FILENAME_ADD_PROJECT_NAME_NAME, getConfiguration(CONF_FILENAME_ADD_PROJECT_NAME_KEY))
    addBoolInputToGroup(inputs, UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_ADD_DESIGN_NAME_KEY, UI_FILENAME_ADD_DESIGN_NAME_NAME, getConfiguration(CONF_FILENAME_ADD_DESIGN_NAME_KEY))

    addBoolInputToGroup(inputs, UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_REMOVE_VERSION_TAGS_KEY, UI_FILENAME_REMOVE_VERSION_TAGS_NAME, getConfiguration(CONF_FILENAME_REMOVE_VERSION_TAGS_KEY))

    addTextListDropDown(inputs, UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_ELEMENT_SEPERATOR_KEY, UI_FILENAME_ELEMENT_SEPERATOR_NAME, UI_FILENAME_ELEMENT_SEPERATOR_VALUES, getConfiguration(CONF_FILENAME_ELEMENT_SEPERATOR_KEY))
    addTextListDropDown(inputs, UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_KEY, UI_FILENAME_OCCURRENCE_ID_SEPERATOR_NAME, UI_FILENAME_OCCURRENCE_ID_SEPERATOR_VALUES, getConfiguration(CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_KEY))

def getExportDirectory():
    # check if export direcotry is set
    logger.info('No export path defined. Asking for input')

    # create dialog
    app = adsk.core.Application.get()
    ui = app.userInterface
    folderDialog = ui.createFolderDialog()
    folderDialog.title = 'Export Directory'

    # open dialog
    dialogResult = folderDialog.showDialog()
    exportDirecotry = ""

    # check if user finished the dialog by pressing okay
    if dialogResult == adsk.core.DialogResults.DialogOK:
        # initialize project configuration
        exportDirecotry = str.format(folderDialog.folder).replace('\\', '/')
        logger.info("Selected export directory: %s", exportDirecotry)

        return exportDirecotry, True
    else:
        # user canceled the dialog
        logger.error('User canceld the request. No export path defined')

        return exportDirecotry, False

def checkDataIntegrity(inputs):
    # check if export directory is defined
    while not getConfiguration(CONF_EXPORT_DIRECTORY_KEY):
        logger.warning('Exportdirecotry is not set. Opening requestor')

        exportPath, isValid = getExportDirectory()
        setConfiguration(CONF_EXPORT_DIRECTORY_KEY, exportPath)

        stringInput = inputs.itemById(CONF_EXPORT_DIRECTORY_KEY)
        stringInput.value = exportPath

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

            # check if the integrity between configured parameters are still valid
            checkDataIntegrity(inputs)

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