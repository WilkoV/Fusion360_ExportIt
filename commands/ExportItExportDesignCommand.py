import adsk.core, adsk.fusion, adsk.cam, traceback
import apper
import os, re, json

from apper import AppObjects
from .BaseLogger import logger
from .UiHelper import addTab, addGroupToTab, addGroup, addStringInputToGroup, addBoolInputToGroup, addCheckBoxDropDown, selectDropDownItemByNames, getSelectedDropDownItems, addTextListDropDown, getSelectedDropDownItem, addSelectionCommandToInputs, addIntergerInputSpinnerToGroup, addFloatInputSpinnerToGroup, hideUiElement, showUiElement, setUiValue
from .ConfigurationHelper import initializeConfiguration, getDefaultConfiguration, getConfiguration, setConfiguration, writeConfiguration, showSaveConfigWarning, resetConfiguration, logConfiguration, saveConfigurationInDocument
from .GithubReleaseHelper import checkForUpdates, getGithubReleaseInformation, showReleaseNotes
from .Statics import *

progressDialog = adsk.core.ProgressDialog.cast(None)                        # progress dialog for larger exports
progressValue = 0                                                           # current state of the progress value
summary = {SUMMARY_INFOS: [], SUMMARY_WARNINGS: [], SUMMARY_ERRORS: []}     # structure containing the data for the summary message at the end of an export

def createDefaultConfiguration():
    logger.debug("creating default configuration")

    # create default configuration
    defaultConfiguration = {}

    # common attributes
    defaultConfiguration[CONF_VERSION_KEY] = CONF_VERSION_DEFAULT

    # export options
    defaultConfiguration[CONF_EXPORT_OPTIONS_TYPE_KEY] = CONF_EXPORT_OPTIONS_TYPE_DEFAULT
    defaultConfiguration[CONF_EXPORT_OPTIONS_EXCLUDE_COMPONENTS_KEY] = CONF_EXPORT_OPTIONS_EXCLUDE_COMPONENTS_DEFAULT
    defaultConfiguration[CONF_EXPORT_OPTIONS_EXCLUDE_LINKS_KEY] = CONF_EXPORT_OPTIONS_EXCLUDE_LINKS_DEFAULT

    # stl options
    defaultConfiguration[CONF_STL_STRUCTURE_KEY] = CONF_STL_STRUCTURE_DEFAULT
    defaultConfiguration[CONF_STL_REFINEMENT_KEY] = CONF_STL_REFINEMENT_DEFAULT
    defaultConfiguration[CONF_STL_SURFACE_DEVIATION_KEY] = CONF_STL_SURFACE_DEVIATION_DEFAULT
    defaultConfiguration[CONF_STL_NORMAL_DEVIATION_KEY] = CONF_STL_NORMAL_DEVIATION_DEFAULT
    defaultConfiguration[CONF_STL_MAX_EDGE_LENGTH_KEY] = CONF_STL_MAX_EDGE_LENGTH_DEFAULT
    defaultConfiguration[CONF_STL_ASPECT_RATIO_KEY] = CONF_STL_ASPECT_RATIO_DEFAULT
    
    # 3mf options
    defaultConfiguration[CONF_3MF_STRUCTURE_KEY] = CONF_3MF_STRUCTURE_DEFAULT
    defaultConfiguration[CONF_3MF_REFINEMENT_KEY] = CONF_3MF_REFINEMENT_DEFAULT
    defaultConfiguration[CONF_3MF_SURFACE_DEVIATION_KEY] = CONF_3MF_SURFACE_DEVIATION_DEFAULT
    defaultConfiguration[CONF_3MF_NORMAL_DEVIATION_KEY] = CONF_3MF_NORMAL_DEVIATION_DEFAULT
    defaultConfiguration[CONF_3MF_MAX_EDGE_LENGTH_KEY] = CONF_3MF_MAX_EDGE_LENGTH_DEFAULT
    defaultConfiguration[CONF_3MF_ASPECT_RATIO_KEY] = CONF_3MF_ASPECT_RATIO_DEFAULT

    # step options
    defaultConfiguration[CONF_STEP_STRUCTURE_KEY] = CONF_STEP_STRUCTURE_DEFAULT

    # f3d options
    defaultConfiguration[CONF_F3D_STRUCTURE_KEY] = CONF_F3D_STRUCTURE_DEFAULT

    # export directory options
    defaultConfiguration[CONF_EXPORT_DIRECTORY_CONFIGURE_KEY] = UI_EXPORT_DIRECTORY_CONFIGURE_DEFAULT_VALUE
    defaultConfiguration[CONF_EXPORT_DIRECTORY_KEY] = CONF_EXPORT_DIRECTORY_DEFAULT
    defaultConfiguration[CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_KEY] = CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_DEFAULT
    defaultConfiguration[CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_KEY] = CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_DEFAULT
    defaultConfiguration[CONF_EXPORT_DIRECTORY_ADD_DENSITY_NAME_KEY] = CONF_EXPORT_DIRECTORY_ADD_DENSITY_NAME_DEFAULT
    defaultConfiguration[CONF_EXPORT_DIRECTORY_ADD_EXPORT_TYPE_KEY] = CONF_EXPORT_DIRECTORY_ADD_EXPORT_TYPE_DEFAULT

    # filename options
    defaultConfiguration[CONF_FILENAME_ADD_PROJECT_NAME_KEY] = CONF_FILENAME_ADD_PROJECT_NAME_DEFAULT
    defaultConfiguration[CONF_FILENAME_ADD_DESIGN_NAME_KEY] = CONF_FILENAME_ADD_DESIGN_NAME_DEFAULT
    defaultConfiguration[CONF_FILENAME_ADD_CONFIGURATION_NAME_KEY] = CONF_FILENAME_ADD_CONFIGURATION_NAME_DEFAULT
    defaultConfiguration[CONF_FILENAME_REMOVE_VERSION_TAGS_KEY] = CONF_FILENAME_REMOVE_VERSION_TAGS_DEFAULT
    defaultConfiguration[CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_KEY] = CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_DEFAULT
    defaultConfiguration[CONF_FILENAME_ELEMENT_SEPERATOR_KEY] = CONF_FILENAME_ELEMENT_SEPERATOR_DEFAULT
    defaultConfiguration[CONF_FILENAME_REPLACE_SPACES_KEY] = CONF_FILENAME_REPLACE_SPACES_DEFAULT
    defaultConfiguration[CONF_FILENAME_REPLACE_SPACES_WITH_KEY] = CONF_FILENAME_REPLACE_SPACES_WITH_DEFAULT
    defaultConfiguration[CONF_FILENAME_USE_PART_NUMBER_KEY] = CONF_FILENAME_USE_PART_NUMBER_DEFAULT

    # common
    defaultConfiguration[CONF_SHOW_SUMMARY_FOR_KEY] = CONF_SHOW_SUMMARY_FOR_DEFAULT
    defaultConfiguration[CONF_AUTOSAVE_PROJECT_CONFIGURATION_KEY] = CONF_AUTOSAVE_PROJECT_CONFIGURATION_DEFAULT
    defaultConfiguration[CONF_AUTOSAVE_DESCRIPTION_KEY] = CONF_AUTOSAVE_DESCRIPTION_DEFAULT

    # check for updates configuration
    defaultConfiguration[CONF_VERSION_CHECK_INTERVAL_IN_DAYS_KEY] = CONF_VERSION_CHECK_INTERVAL_IN_DAYS_DEFAULT

    return defaultConfiguration

def initializeExcludeComponentList():
    rootComponent = AppObjects().design.rootComponent
    components = []
    exportObjects = getExportObjects(rootComponent, [], False)

    for exportObject in exportObjects:
        if not exportObject.get(REC_OCCURRENCE_PATH):
            continue

        if len(exportObject.get(REC_BODIES)) == 0:
            continue

        if not exportObject.get(REC_IS_UNIQUE):
            continue

        componentNameWidthPath = exportObject.get(REC_OCCURRENCE).name
        componentName = componentNameWidthPath.split(":")[0]
        components.append(componentName)

    configurationElements = getConfiguration(CONF_EXPORT_OPTIONS_EXCLUDE_COMPONENTS_KEY)
    newConfiguration = []
    isChanged = False
    
    for configElement in configurationElements:
        if configElement in components:
            newConfiguration.append(configElement) 
        else:
            logger.debug("Occurrences structure has changed, removing %s from the list", configElement)
            isChanged = True
    
    if isChanged:
        logger.info("Updating project configuration, because structure has changed")
        setConfiguration(CONF_EXPORT_OPTIONS_EXCLUDE_COMPONENTS_KEY, newConfiguration)

    return components

def initializeUi(inputs :adsk.core.CommandInputs, configurationOnly, checkForUpdates):
    logger.debug("not checkForUpdates %s", not checkForUpdates)
    # export
    addTab(inputs, UI_EXPORT_TAB_ID, UI_EXPORT_TAB_NAME, not checkForUpdates)

    # export options
    addGroupToTab(UI_EXPORT_TAB_ID, UI_EXPORT_OPTIONS_GROUP_ID, UI_EXPORT_OPTIONS_GROUP_NAME, True)

    # add selection command
    if not configurationOnly:
        # do not show in the configuration editor
        addSelectionCommandToInputs(UI_EXPORT_OPTIONS_GROUP_ID, UI_EXPORT_OPTIONS_BODIES_SELECTION_ID, UI_EXPORT_OPTIONS_BODIES_SELECTION_NAME, UI_EXPORT_OPTIONS_BODIES_SELECTION_VALUES)

    addCheckBoxDropDown(UI_EXPORT_OPTIONS_GROUP_ID, CONF_EXPORT_OPTIONS_TYPE_KEY, UI_EXPORT_OPTIONS_TYPE_NAME, UI_EXPORT_OPTIONS_TYPE_VALUES, getConfiguration(CONF_EXPORT_OPTIONS_TYPE_KEY))

    if not configurationOnly:
        addCheckBoxDropDown(UI_EXPORT_OPTIONS_GROUP_ID, CONF_EXPORT_OPTIONS_EXCLUDE_COMPONENTS_KEY, UI_EXPORT_OPTIONS_EXCLUDE_COMPONENTS_NAME, initializeExcludeComponentList(), getConfiguration(CONF_EXPORT_OPTIONS_EXCLUDE_COMPONENTS_KEY))

    addBoolInputToGroup(UI_EXPORT_OPTIONS_GROUP_ID, CONF_EXPORT_OPTIONS_EXCLUDE_LINKS_KEY, UI_EXPORT_OPTIONS_EXCLUDE_LINKS_NAME, getConfiguration(CONF_EXPORT_OPTIONS_EXCLUDE_LINKS_KEY))

    # stl export
    addGroupToTab(UI_EXPORT_TAB_ID, UI_STL_OPTIONS_GROUP_ID, UI_STL_OPTIONS_GROUP_NAME, True)
    addCheckBoxDropDown(UI_STL_OPTIONS_GROUP_ID, CONF_STL_STRUCTURE_KEY, UI_STL_STRUCTURE_NAME, UI_STL_STRUCTURE_VALUES, getConfiguration(CONF_STL_STRUCTURE_KEY))
    addCheckBoxDropDown(UI_STL_OPTIONS_GROUP_ID, CONF_STL_REFINEMENT_KEY, UI_STL_REFINEMENT_NAME, UI_STL_REFINEMENT_VALUES, getConfiguration(CONF_STL_REFINEMENT_KEY))

    addFloatInputSpinnerToGroup(UI_STL_OPTIONS_GROUP_ID, CONF_STL_SURFACE_DEVIATION_KEY, UI_STL_SURFACE_DEVIATION_NAME, "", UI_STL_SURFACE_DEVIATION_MIN, UI_STL_SURFACE_DEVIATION_MAX, UI_STL_SURFACE_DEVIATION_STEP, getConfiguration(CONF_STL_SURFACE_DEVIATION_KEY))
    addFloatInputSpinnerToGroup(UI_STL_OPTIONS_GROUP_ID, CONF_STL_NORMAL_DEVIATION_KEY, UI_STL_NORMAL_DEVIATION_NAME, "", UI_STL_NORMAL_DEVIATION_MIN, UI_STL_NORMAL_DEVIATION_MAX, UI_STL_NORMAL_DEVIATION_STEP,getConfiguration( CONF_STL_NORMAL_DEVIATION_KEY))
    addFloatInputSpinnerToGroup(UI_STL_OPTIONS_GROUP_ID, CONF_STL_MAX_EDGE_LENGTH_KEY, UI_STL_MAX_EDGE_LENGTH_NAME, "", UI_STL_MAX_EDGE_LENGTH_MIN, UI_STL_MAX_EDGE_LENGTH_MAX, UI_STL_MAX_EDGE_LENGTH_STEP, getConfiguration(CONF_STL_MAX_EDGE_LENGTH_KEY))
    addFloatInputSpinnerToGroup(UI_STL_OPTIONS_GROUP_ID, CONF_STL_ASPECT_RATIO_KEY, UI_STL_ASPECT_RATIO_NAME, "", UI_STL_ASPECT_RATIO_MIN, UI_STL_ASPECT_RATIO_MAX, UI_STL_ASPECT_RATIO_STEP, getConfiguration(CONF_STL_ASPECT_RATIO_KEY))

    # 3mf export
    addGroupToTab(UI_EXPORT_TAB_ID, UI_3MF_OPTIONS_GROUP_ID, UI_3MF_OPTIONS_GROUP_NAME, True)
    addCheckBoxDropDown(UI_3MF_OPTIONS_GROUP_ID, CONF_3MF_STRUCTURE_KEY, UI_3MF_STRUCTURE_NAME, UI_3MF_STRUCTURE_VALUES, getConfiguration(CONF_3MF_STRUCTURE_KEY))
    addCheckBoxDropDown(UI_3MF_OPTIONS_GROUP_ID, CONF_3MF_REFINEMENT_KEY, UI_3MF_REFINEMENT_NAME, UI_3MF_REFINEMENT_VALUES, getConfiguration(CONF_3MF_REFINEMENT_KEY))

    addFloatInputSpinnerToGroup(UI_3MF_OPTIONS_GROUP_ID, CONF_3MF_SURFACE_DEVIATION_KEY, UI_3MF_SURFACE_DEVIATION_NAME, "", UI_3MF_SURFACE_DEVIATION_MIN, UI_3MF_SURFACE_DEVIATION_MAX, UI_3MF_SURFACE_DEVIATION_STEP, getConfiguration(CONF_3MF_SURFACE_DEVIATION_KEY))
    addFloatInputSpinnerToGroup(UI_3MF_OPTIONS_GROUP_ID, CONF_3MF_NORMAL_DEVIATION_KEY, UI_3MF_NORMAL_DEVIATION_NAME, "", UI_3MF_NORMAL_DEVIATION_MIN, UI_3MF_NORMAL_DEVIATION_MAX, UI_3MF_NORMAL_DEVIATION_STEP,getConfiguration( CONF_3MF_NORMAL_DEVIATION_KEY))
    addFloatInputSpinnerToGroup(UI_3MF_OPTIONS_GROUP_ID, CONF_3MF_MAX_EDGE_LENGTH_KEY, UI_3MF_MAX_EDGE_LENGTH_NAME, "", UI_3MF_MAX_EDGE_LENGTH_MIN, UI_3MF_MAX_EDGE_LENGTH_MAX, UI_3MF_MAX_EDGE_LENGTH_STEP, getConfiguration(CONF_3MF_MAX_EDGE_LENGTH_KEY))
    addFloatInputSpinnerToGroup(UI_3MF_OPTIONS_GROUP_ID, CONF_3MF_ASPECT_RATIO_KEY, UI_3MF_ASPECT_RATIO_NAME, "", UI_3MF_ASPECT_RATIO_MIN, UI_3MF_ASPECT_RATIO_MAX, UI_3MF_ASPECT_RATIO_STEP, getConfiguration(CONF_3MF_ASPECT_RATIO_KEY))

    # step export
    addGroupToTab(UI_EXPORT_TAB_ID, UI_STEP_OPTIONS_GROUP_ID, UI_STEP_OPTIONS_GROUP_NAME, True)
    addCheckBoxDropDown(UI_STEP_OPTIONS_GROUP_ID, CONF_STEP_STRUCTURE_KEY, UI_STEP_STRUCTURE_NAME, UI_STEP_STRUCTURE_VALUES, getConfiguration(CONF_STEP_STRUCTURE_KEY))

    # f3d export
    addGroupToTab(UI_EXPORT_TAB_ID, UI_F3D_OPTIONS_GROUP_ID, UI_F3D_OPTIONS_GROUP_NAME, True)
    addCheckBoxDropDown(UI_F3D_OPTIONS_GROUP_ID, CONF_F3D_STRUCTURE_KEY, UI_F3D_STRUCTURE_NAME, UI_F3D_STRUCTURE_VALUES, getConfiguration(CONF_F3D_STRUCTURE_KEY))

    # location
    addTab(inputs, UI_LOCATION_TAB_ID, UI_LOCATION_TAB_ID, False)

    # export directory
    addGroupToTab(UI_LOCATION_TAB_ID, UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID, UI_EXPORT_DIRECTORY_OPTIONS_GROUP_NAME, True)

    if configurationOnly:
        addTextListDropDown(UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID, CONF_EXPORT_DIRECTORY_CONFIGURE_KEY, UI_EXPORT_DIRECTORY_CONFIGURE_NAME, UI_EXPORT_DIRECTORY_CONFIGURE_VALUES, getConfiguration(CONF_EXPORT_DIRECTORY_CONFIGURE_KEY))

    addStringInputToGroup(UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID, CONF_EXPORT_DIRECTORY_KEY, UI_EXPORT_DIRECTORY_NAME, getConfiguration(CONF_EXPORT_DIRECTORY_KEY), False)
    addBoolInputToGroup(UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID, UI_EXPORT_DIRECTORY_RESET_ID, UI_EXPORT_DIRECTORY_RESET_NAME, UI_EXPORT_DIRECTORY_RESET_DEFAULT)
    addBoolInputToGroup(UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID, CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_KEY, UI_EXPORT_DIRECTORY_ADD_PROJECT_NAME_NAME, getConfiguration(CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_KEY))
    addBoolInputToGroup(UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID, CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_KEY, UI_EXPORT_DIRECTORY_ADD_DESIGN_NAME_NAME, getConfiguration(CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_KEY))
    addBoolInputToGroup(UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID, CONF_EXPORT_DIRECTORY_ADD_EXPORT_TYPE_KEY, UI_EXPORT_DIRECTORY_EXPORT_TYPE_NAME, getConfiguration(CONF_EXPORT_DIRECTORY_ADD_EXPORT_TYPE_KEY))
    addBoolInputToGroup(UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID, CONF_EXPORT_DIRECTORY_ADD_DENSITY_NAME_KEY, UI_EXPORT_DIRECTORY_ADD_DENSITY_NAME_NAME, getConfiguration(CONF_EXPORT_DIRECTORY_ADD_DENSITY_NAME_KEY))

    # filename options
    addGroupToTab(UI_LOCATION_TAB_ID, UI_FILENAME_OPTIONS_GROUP_ID, UI_FILENAME_OPTIONS_GROUP_NAME, True)

    addBoolInputToGroup(UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_ADD_PROJECT_NAME_KEY, UI_FILENAME_ADD_PROJECT_NAME_NAME, getConfiguration(CONF_FILENAME_ADD_PROJECT_NAME_KEY))
    addBoolInputToGroup(UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_ADD_DESIGN_NAME_KEY, UI_FILENAME_ADD_DESIGN_NAME_NAME, getConfiguration(CONF_FILENAME_ADD_DESIGN_NAME_KEY))

    if AppObjects().design.isConfiguredDesign:
        addBoolInputToGroup(UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_ADD_CONFIGURATION_NAME_KEY,
                            UI_FILENAME_ADD_CONFIGURATION_NAME, getConfiguration(CONF_FILENAME_ADD_CONFIGURATION_NAME_KEY))

    addBoolInputToGroup(UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_REMOVE_VERSION_TAGS_KEY, UI_FILENAME_REMOVE_VERSION_TAGS_NAME, getConfiguration(CONF_FILENAME_REMOVE_VERSION_TAGS_KEY))
    addTextListDropDown(UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_ELEMENT_SEPERATOR_KEY, UI_FILENAME_ELEMENT_SEPERATOR_NAME, UI_FILENAME_ELEMENT_SEPERATOR_VALUES, getConfiguration(CONF_FILENAME_ELEMENT_SEPERATOR_KEY))
    addTextListDropDown(UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_KEY, UI_FILENAME_OCCURRENCE_ID_SEPERATOR_NAME, UI_FILENAME_OCCURRENCE_ID_SEPERATOR_VALUES, getConfiguration(CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_KEY))
    addBoolInputToGroup(UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_REPLACE_SPACES_KEY, UI_FILENAME_REPLACE_SPACES_NAME, getConfiguration(CONF_FILENAME_REPLACE_SPACES_KEY))
    addTextListDropDown(UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_REPLACE_SPACES_WITH_KEY, UI_FILENAME_REPLACE_SPACES_WITH_NAME, UI_FILENAME_REPLACE_SPACES_WITH_VALUES, getConfiguration(CONF_FILENAME_REPLACE_SPACES_WITH_KEY))
    
    addBoolInputToGroup(UI_FILENAME_OPTIONS_GROUP_ID, CONF_FILENAME_USE_PART_NUMBER_KEY, UI_FILENAME_USE_PART_NUMBER_NAME, getConfiguration(CONF_FILENAME_USE_PART_NUMBER_KEY))

    # location
    if configurationOnly or checkForUpdates:
        # add group for version information
        addTab(inputs, UI_MISC_TAB_ID, UI_MISC_TAB_ID, checkForUpdates)

    if configurationOnly:
        addGroupToTab(UI_MISC_TAB_ID, UI_COMMON_GROUP_ID, UI_COMMON_GROUP_NAME, True)
        addTextListDropDown(UI_COMMON_GROUP_ID, CONF_SHOW_SUMMARY_FOR_KEY, UI_SHOW_SUMMARY_FOR_NAME, UI_SHOW_SUMMARY_FOR_VALUES, getConfiguration(CONF_SHOW_SUMMARY_FOR_KEY))
        addBoolInputToGroup(UI_COMMON_GROUP_ID, CONF_AUTOSAVE_PROJECT_CONFIGURATION_KEY, UI_AUTOSAVE_PROJECT_CONFIGURATION_NAME, getConfiguration(CONF_AUTOSAVE_PROJECT_CONFIGURATION_KEY))
        addStringInputToGroup(UI_COMMON_GROUP_ID, CONF_AUTOSAVE_DESCRIPTION_KEY, UI_AUTOSAVE_DESCRIPTION_NAME, getConfiguration(CONF_AUTOSAVE_DESCRIPTION_KEY), True)

    if configurationOnly or checkForUpdates:
        # add group for version information
        addGroupToTab(UI_MISC_TAB_ID, UI_VERSION_GROUP_ID, UI_VERSION_GROUP_NAME, True)

    if configurationOnly:
        addIntergerInputSpinnerToGroup(UI_VERSION_GROUP_ID, CONF_VERSION_CHECK_INTERVAL_IN_DAYS_KEY, UI_VERSION_CHECK_INTERVAL_NAME, CONF_VERSION_CHECK_INTERVAL_IN_DAYS_MIN, CONF_VERSION_CHECK_INTERVAL_IN_DAYS_MAX, 1, getConfiguration(CONF_VERSION_CHECK_INTERVAL_IN_DAYS_KEY))

    if checkForUpdates:
        # add field that can show the download url for easy copy/past
        addinVersion, githubRemoteVersion, githubTitle, githubDescription, githubDownloadUrl = getGithubReleaseInformation()
        addStringInputToGroup(UI_VERSION_GROUP_ID, UI_VERSION_DOWNLOAD_URL_ID, UI_VERSION_DOWNLOAD_URL_NAME, githubDownloadUrl, True)

    showHideCustomStlSettings(inputs)
    showHideCustom3mfSettings(inputs)

def showHideCustomStlSettings(inputs):
    if UI_STL_REFINEMENT_CUSTOM_VALUE in getConfiguration(CONF_STL_REFINEMENT_KEY):
        # custom stl refinements are enabled. Show additional configuration fields
        showUiElement(inputs, CONF_STL_SURFACE_DEVIATION_KEY)
        showUiElement(inputs, CONF_STL_NORMAL_DEVIATION_KEY)
        showUiElement(inputs, CONF_STL_MAX_EDGE_LENGTH_KEY)
        showUiElement(inputs, CONF_STL_ASPECT_RATIO_KEY)
    else:
        # custom stl refinements are disabled. Hide additional configuration fields
        hideUiElement(inputs, CONF_STL_SURFACE_DEVIATION_KEY)
        hideUiElement(inputs, CONF_STL_NORMAL_DEVIATION_KEY)
        hideUiElement(inputs, CONF_STL_MAX_EDGE_LENGTH_KEY)
        hideUiElement(inputs, CONF_STL_ASPECT_RATIO_KEY)

def showHideCustom3mfSettings(inputs):
    if UI_3MF_REFINEMENT_CUSTOM_VALUE in getConfiguration(CONF_3MF_REFINEMENT_KEY):
        # custom 3mf refinements are enabled. Show additional configuration fields
        showUiElement(inputs, CONF_3MF_SURFACE_DEVIATION_KEY)
        showUiElement(inputs, CONF_3MF_NORMAL_DEVIATION_KEY)
        showUiElement(inputs, CONF_3MF_MAX_EDGE_LENGTH_KEY)
        showUiElement(inputs, CONF_3MF_ASPECT_RATIO_KEY)
    else:
        # custom 3mf refinements are disabled. Hide additional configuration fields
        hideUiElement(inputs, CONF_3MF_SURFACE_DEVIATION_KEY)
        hideUiElement(inputs, CONF_3MF_NORMAL_DEVIATION_KEY)
        hideUiElement(inputs, CONF_3MF_MAX_EDGE_LENGTH_KEY)
        hideUiElement(inputs, CONF_3MF_ASPECT_RATIO_KEY)

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

def validateCheckBoxDropDown(inputs, confKey, confDefaults):
    if len(getConfiguration(confKey)) == 0:
        values = getDefaultConfiguration(confKey, confDefaults)

        logger.warning("No items selected for %s. Resetting to defaults %s", confKey, values)

        selectDropDownItemByNames(inputs, confKey, values, True)
        setConfiguration(confKey, values)

def validateConfiguration(inputs):
    # check if any export type is selected
    validateCheckBoxDropDown(inputs, CONF_EXPORT_OPTIONS_TYPE_KEY, CONF_EXPORT_OPTIONS_TYPE_DEFAULT)

    # check stl settings
    if UI_EXPORT_TYPES_STL_VALUE in getConfiguration(CONF_EXPORT_OPTIONS_TYPE_KEY):
        # check if any export structure is selected
        validateCheckBoxDropDown(inputs, CONF_STL_STRUCTURE_KEY, CONF_STL_STRUCTURE_DEFAULT)
        # check if any refinement is selected
        validateCheckBoxDropDown(inputs, CONF_STL_REFINEMENT_KEY, CONF_STL_REFINEMENT_DEFAULT)

    # check 3mf settings
    if UI_EXPORT_TYPES_3MF_VALUE in getConfiguration(CONF_EXPORT_OPTIONS_TYPE_KEY):
        # check if any export structure is selected
        validateCheckBoxDropDown(inputs, CONF_3MF_STRUCTURE_KEY, CONF_3MF_STRUCTURE_DEFAULT)
        # check if any refinement is selected
        validateCheckBoxDropDown(inputs, CONF_3MF_REFINEMENT_KEY, CONF_3MF_REFINEMENT_DEFAULT)

    # check step settings
    if UI_EXPORT_TYPES_STEP_VALUE in getConfiguration(CONF_EXPORT_OPTIONS_TYPE_KEY):
        # check if any export structure is selected
        validateCheckBoxDropDown(inputs, CONF_STEP_STRUCTURE_KEY, CONF_STEP_STRUCTURE_DEFAULT)

    showHideCustomStlSettings(inputs)
    showHideCustom3mfSettings(inputs)

def validateExportDirectory():
    # check if export directory is defined
    while not getConfiguration(CONF_EXPORT_DIRECTORY_KEY):
        logger.warning('Exportdirecotry is not set. Opening requestor')

        exportPath, isValid = getExportDirectory()
        setConfiguration(CONF_EXPORT_DIRECTORY_KEY, exportPath)

def resetExportDirecotry(input_values):
    logger.warning('Resetting export directory. Opening requestor')

    exportPath, isValid = getExportDirectory()
    setConfiguration(CONF_EXPORT_DIRECTORY_KEY, exportPath)

def getReferencedOccurrences(occurrences):
    referencedOccurrences = []

    # process all occurrences
    for occurrence in occurrences:
        if occurrence.isReferencedComponent:
            # add referenced occurrence to result list
            referencedOccurrences.append(occurrence.name)

    return referencedOccurrences

def isReferenced(occurrence, referencedOccurrences):
    isReferenced = False
    pathElements = occurrence.fullPathName.split("+")

    # process elements of the occurrence path
    for element in pathElements:
        if element in referencedOccurrences:
            # path element is part of the occurrence's path, so mark this sub occurrence as referenced occurrence
            isReferenced = True
            logger.debug("isReferenced: %s", element)

    return isReferenced

def isExcludeComponent(occurrence):
    isExcluded = False
    pathName = occurrence.fullPathName.split("+")
    pathElements = pathName
    
    # process elements of the occurrence path
    for element in pathElements:
        elementWithoutOccurrenceId = element.split(':')[0]
        excludedComponents = getConfiguration(CONF_EXPORT_OPTIONS_EXCLUDE_COMPONENTS_KEY)

        if elementWithoutOccurrenceId in excludedComponents:
            # element is in the list of excluded occurrences, so exclude all sub occurrences
            isExcluded = True
            logger.debug("%s in path %s is excluded", elementWithoutOccurrenceId, pathName)
    
    return isExcluded

def getExportObjects(rootComponent :adsk.fusion.Component, selectedBodies, processExcludeComponents):
    exportObjects = []
    rootBodies = []
    uniqueComponents = []
    isReferencedComponent = False

    # if bodies folder is visible add all visible bodies to the list of visible objects
    if rootComponent.isBodiesFolderLightBulbOn:
        # get root bodies
        body = adsk.fusion.BRepBody.cast(None)

        for body in rootComponent.bRepBodies:
            if not body.isLightBulbOn:
                logger.info("body %s in %s is not visible", body.name, "root")
                continue

            if len(selectedBodies) > 0 and body not in selectedBodies:
                logger.info("body %s in %s is not selected", body.name, "root")
                continue

            # add visible body to the list of root bodies
            rootBodies.append(body)

        # if root component has bodies, add occurrence to the list of exportable objects
        if len(rootBodies) > 0:
            exportObjects.append({REC_OCCURRENCE: None, REC_OCCURRENCE_PATH: "", REC_BODIES: rootBodies})
        else:
            logger.info("%s has no bodies", "root")
    else:
        logger.info("%s has no visible bodies folder", "root")

    # get list of referenced occurrences
    referencedOccurrences = getReferencedOccurrences(rootComponent.allOccurrences)

    # add visible bodies of all occurrences to the list of visible objects
    for occurrence in rootComponent.allOccurrences:
        isUnique = False
        isTopLevel = False
        hasMeshBodies = False

        partNumber = ""
        occurrenceFullPathName = occurrence.fullPathName

        # check if occurrence is referencing a external component
        if isReferenced(occurrence, referencedOccurrences):
            if getConfiguration(CONF_EXPORT_OPTIONS_EXCLUDE_LINKS_KEY):
                logger.info("occurrence %s is excluded, because it's an external reference or part of an external reference", occurrenceFullPathName)
                continue

        # for getting list of UI elements it's not usefull to process excluded occurrences. This flag is used to control the behavior of the function
        if processExcludeComponents:
            # function should process excluded occurrences
            if isExcludeComponent(occurrence):
                logger.info("occurrence %s is excluded from the user", occurrenceFullPathName)
                continue

        # check if occurrence is visible. if not jump to next occurrence
        if not occurrence.isLightBulbOn:
            logger.info("%s is hidden", occurrenceFullPathName)
            continue

        # check if bodies folder in occurrence is visible.  if not jump to next occurrence
        if not occurrence.component.isBodiesFolderLightBulbOn:
            logger.info("bodies in %s are not visible", occurrenceFullPathName)
            continue

        # check if component is unique
        if not occurrence.component in uniqueComponents:
            uniqueComponents.append(occurrence.component)
            isUnique = True
            logger.info("%s is unique", occurrenceFullPathName)
       
        # check if occurrence is a top level component
        # if occurrenceFullPathName.count(":") == 1:
        if occurrence in rootComponent.occurrences:
            isTopLevel = True
            logger.info("component %s is a top level component", occurrenceFullPathName)

        if len(occurrence.component.meshBodies) > 0:
            logger.info("component %s has mesh bodies that might not be exported", occurrenceFullPathName)
            hasMeshBodies = True

        # get visible occurrence bodies
        occurrenceBodies = []
        for body in occurrence.bRepBodies:
            # check if body is visible. if not jump to next body
            if not body.isLightBulbOn:
                logger.info("body %s in %s is not visible", body.name, occurrenceFullPathName)
                continue

            if len(selectedBodies) > 0 and body not in selectedBodies:
                logger.info("body %s in %s is not selected", body.name, occurrenceFullPathName)
                continue

            # add visible body to the list of occurrence bodies
            occurrenceBodies.append(body)

        # check if occurrence has bodies. if not jump to next occurrence
        if len(occurrenceBodies) == 0 and not isTopLevel:
            logger.info("%s has no bodies", occurrenceFullPathName)
            continue

        if (occurrence.component.partNumber != occurrence.component.name):
            partNumber = occurrence.component.partNumber

        # if occurrence has bodies, add occurrence to the list of exportable objects
        exportObjects.append({REC_OCCURRENCE: occurrence, REC_OCCURRENCE_PATH: occurrenceFullPathName, REC_IS_UNIQUE: isUnique, REC_IS_TOP_LEVEL: isTopLevel, REC_IS_REFERENCED_COMPONENT: isReferencedComponent, REC_HAS_MESH_BODIES: hasMeshBodies, REC_BODIES: occurrenceBodies, REC_PART_NUMBER: partNumber})

    logger.debug(exportObjects)
    return exportObjects

def updateProgressDialog():
    global progressDialog
    global progressValue

    adsk.doEvents()

    # update internal progress counter
    progressValue = progressValue + 1

    if progressDialog.wasCancelled:
        # nothing to do, because the dialog is cancelled
        progressDialog.hide()
        return

    if not progressDialog.isShowing:
        # nothing to do, because the dialog is not visible
        return

    # update progress dialog
    progressDialog.progressValue = progressValue

def totalNumberOfObjects(exportObjects):
    components = 0
    componentBodies = 0
    occurrenceBodies = 0
    topLevelOccurrences = 0
    total = 0

    for exportObject in exportObjects:
        if exportObject.get(REC_IS_UNIQUE):
            components = components + 1
            componentBodies =  componentBodies + len(exportObject.get(REC_BODIES))

        if exportObject.get(REC_IS_TOP_LEVEL) and (len(exportObject.get(REC_BODIES)) > 0 or len(exportObject.get(REC_OCCURRENCE).childOccurrences) > 0):
            topLevelOccurrences = topLevelOccurrences + 1

        occurrenceBodies =  occurrenceBodies + len(exportObject.get(REC_BODIES))

    if UI_EXPORT_TYPES_F3D_VALUE in getConfiguration(CONF_EXPORT_OPTIONS_TYPE_KEY):
        if UI_STRUCTURE_ONE_FILE_VALUE in getConfiguration(CONF_F3D_STRUCTURE_KEY):
            total = total + 1

        if UI_STRUCTURE_ONE_FILE_PER_COMPONENT_VALUE in getConfiguration(CONF_F3D_STRUCTURE_KEY):
            total = total + components

    if UI_EXPORT_TYPES_STEP_VALUE in getConfiguration(CONF_EXPORT_OPTIONS_TYPE_KEY):
        if UI_STRUCTURE_ONE_FILE_VALUE in getConfiguration(CONF_STEP_STRUCTURE_KEY):
            total = total + 1

        if UI_STRUCTURE_ONE_FILE_PER_COMPONENT_VALUE in getConfiguration(CONF_STEP_STRUCTURE_KEY):
            total = total + components

    for refinement in getConfiguration(CONF_STL_REFINEMENT_KEY):
        if UI_EXPORT_TYPES_STL_VALUE in getConfiguration(CONF_EXPORT_OPTIONS_TYPE_KEY):
            if UI_STRUCTURE_ONE_FILE_VALUE in getConfiguration(CONF_STL_STRUCTURE_KEY):
                total = total + 1

            if UI_STRUCTURE_ONE_FILE_PER_BODY_IN_COMPONENT_VALUE in getConfiguration(CONF_STL_STRUCTURE_KEY):
                total = total + componentBodies

            if UI_STRUCTURE_ONE_FILE_PER_BODY_IN_OCCURRENCE_VALUE in getConfiguration(CONF_STL_STRUCTURE_KEY):
                total = total + occurrenceBodies

            if UI_STRUCTURE_ONE_FILE_PER_TOP_LEVEL_OCCURRENCE_VALUE in getConfiguration(CONF_STL_STRUCTURE_KEY):
                total = total + topLevelOccurrences

    for refinement in getConfiguration(CONF_3MF_REFINEMENT_KEY):
        if UI_EXPORT_TYPES_3MF_VALUE in getConfiguration(CONF_EXPORT_OPTIONS_TYPE_KEY):
            if UI_STRUCTURE_ONE_FILE_VALUE in getConfiguration(CONF_3MF_STRUCTURE_KEY):
                total = total + 1

            if UI_STRUCTURE_ONE_FILE_PER_BODY_IN_COMPONENT_VALUE in getConfiguration(CONF_3MF_STRUCTURE_KEY):
                total = total + componentBodies

            if UI_STRUCTURE_ONE_FILE_PER_BODY_IN_OCCURRENCE_VALUE in getConfiguration(CONF_3MF_STRUCTURE_KEY):
                total = total + occurrenceBodies

            if UI_STRUCTURE_ONE_FILE_PER_TOP_LEVEL_OCCURRENCE_VALUE in getConfiguration(CONF_3MF_STRUCTURE_KEY):
                total = total + topLevelOccurrences

    logger.debug("components: %s", components)
    logger.debug("componentBodies: %s", componentBodies)
    logger.debug("occurrenceBodies: %s", occurrenceBodies)
    logger.debug("topLevelOccurrences: %s", topLevelOccurrences)
    logger.debug("total: %s", total)

    return total

def removeVersionTag(name):
    if not getConfiguration(CONF_FILENAME_REMOVE_VERSION_TAGS_KEY):
        return name

    return re.sub(r' v[0-9]*', '', name)

def getExportName(projectName, designName, configurationName, occurrenceFullPathName, bodyName, forceAddDesignName, removeOccurrenceNumber, refinementName, suffix, partId):
    nameElements = []

    # create export directory path
    exportDirectory = getConfiguration(CONF_EXPORT_DIRECTORY_KEY) + "/"

    if getConfiguration(CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_KEY):
        exportDirectory = exportDirectory + projectName + "/"

    if getConfiguration(CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_KEY):
        exportDirectory = exportDirectory + removeVersionTag(designName) + "/"

    if getConfiguration(CONF_EXPORT_DIRECTORY_ADD_EXPORT_TYPE_KEY):
        exportDirectory = exportDirectory + suffix

        if getConfiguration(CONF_EXPORT_DIRECTORY_ADD_DENSITY_NAME_KEY) and refinementName and suffix == UI_EXPORT_TYPES_STL_VALUE:
            exportDirectory = exportDirectory + " - " + refinementName.lower()

        exportDirectory = exportDirectory + "/"

    os.makedirs(exportDirectory, 0o777, True)

    elementSeparator = getConfiguration(CONF_FILENAME_ELEMENT_SEPERATOR_KEY)

    # render filename prefix
    if getConfiguration(CONF_FILENAME_ADD_PROJECT_NAME_KEY) and projectName:
        nameElements.append(removeVersionTag(projectName))

    if (forceAddDesignName or getConfiguration(CONF_FILENAME_ADD_DESIGN_NAME_KEY)) and designName:
        nameElements.append(removeVersionTag(designName))

    if getConfiguration(CONF_FILENAME_ADD_CONFIGURATION_NAME_KEY) and configurationName:
        nameElements.append(configurationName)

    # render pathname
    if occurrenceFullPathName:
        # replace occurrence id
        pathName = occurrenceFullPathName
        if getConfiguration(CONF_FILENAME_USE_PART_NUMBER_KEY) and partId:
            pathName = partId
        elif removeOccurrenceNumber:
            pathName = re.sub(r':[0-9]*', '', pathName)
        else:
            pathName = pathName.replace(":", getConfiguration(CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_KEY))

        # replace occurrences separator
        pathName = pathName.replace("+", elementSeparator)

        nameElements.append(removeVersionTag(pathName))

    # add body's name
    if bodyName:
        nameElements.append(bodyName)

    # add refinement name
    if refinementName and (suffix == UI_EXPORT_TYPES_STL_VALUE or suffix == UI_EXPORT_TYPES_3MF_VALUE):
        nameElements.append(refinementName.lower())

    # assemble suffix name
    nameElements.append(suffix.lower())

    # assemble filename
    fileName = elementSeparator.join(nameElements)

    # remove spaces from filename
    if getConfiguration(CONF_FILENAME_REPLACE_SPACES_KEY):
        fileName = fileName.replace(" ", getConfiguration(CONF_FILENAME_REPLACE_SPACES_WITH_KEY))

    # assemble full path name
    fullFileName = exportDirectory + fileName

    logger.debug("fullPathName: %s", fullFileName)

    return fullFileName

def copyDesignToExportDocument(exportObjects):
    # create export document
    application = adsk.core.Application.get()
    fusionDocType = adsk.core.DocumentTypes.FusionDesignDocumentType
    document :adsk.fusion.FusionDocument = application.documents.add(fusionDocType)

    logger.debug("temporary document created")

    # set design type
    design :adsk.fusion.Design = document.design
    design.designType = adsk.fusion.DesignTypes.DirectDesignType

    # get root component
    rootComponent :adsk.fusion.Component = design.rootComponent

    logger.debug("temporary rootComponent created")

    # create 3d object wrapper for creation of occurrences
    matrix3d = adsk.core.Matrix3D.create()

    # create body manager for creating copies of bodies
    temporaryBRepManager = adsk.fusion.TemporaryBRepManager.get()

    # copy relevant occurrences to export document
    for exportObject in exportObjects:
        sourceOccurrence = exportObject.get(REC_OCCURRENCE)

        # create occurrences path for export object
        baseComponent = rootComponent

        if exportObject.get(REC_OCCURRENCE_PATH):
            pathElements = exportObject.get(REC_OCCURRENCE_PATH).split("+")

            for pathElement in pathElements:
                # get new component name and use the old instance id as part of it
                occurrenceInstanceId = pathElement.split(":")[-1]
                occurrenceName = pathElement.replace(":", getConfiguration(CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_KEY))

                foundOccurrence = rootComponent.allOccurrences.itemByName(occurrenceName + ":" + occurrenceInstanceId)

                # check if occurrence already exists
                if foundOccurrence:
                    # occurrences found, proceed with next element
                    baseComponent = foundOccurrence.component
                    continue

                # create new occurrence
                occurrence = baseComponent.occurrences.addNewComponent(matrix3d)
                component = occurrence.component

                # set component name
                component.name = occurrenceName
                logger.debug("occurrence %s created (part of %s)", occurrenceName, pathElements)

                # set new base
                baseComponent = component

        for body in exportObject.get(REC_BODIES):
            # copy body
            copiedBody = temporaryBRepManager.copy(body)

            # insert body into new document
            addedBody = baseComponent.bRepBodies.add(copiedBody)
            addedBody.name = body.name

            logger.debug("body %s added to %s", body.name, exportObject.get(REC_OCCURRENCE_PATH))

    return document, rootComponent

def addInfoToSummary(suffix, fullFileName):
    global summary
    filename = fullFileName

    if len(filename) > 50:
        filename = filename[0:10] + "..." + filename[-37:]

    summary[SUMMARY_INFOS].append("   " + suffix + ": " + filename)

def addWarningToSummary(suffix, errorType, objectPath):
    global summary
    path = objectPath

    if len(path) > 50:
        path = path[0:10] + "..." + path[-37:]

    summary[SUMMARY_WARNINGS].append("   " + suffix + ": (" + errorType + ") " + path)

def addErrorToSummary(suffix, errorType, objectPath):
    global summary
    path = objectPath

    if len(path) > 50:
        path = path[0:10] + "..." + path[-37:]
    
    summary[SUMMARY_ERRORS].append("   " + suffix + ": (" + errorType + ") " + path)

def getSummaryMessageFor(category, allEntries, maxEntries):
    numberOfEntries = len(allEntries)
    entries = allEntries
    message = category + ":\n"

    if numberOfEntries > maxEntries:
        lastEntry = entries[numberOfEntries - 1]
        entries = []
        entries = allEntries[0:maxEntries-3]
        entries.append('   ...')
        entries.append(lastEntry)

    message = message + "\n".join(entries)
    message = message + "\n"
    message = message + "\n"

    return message

def showSummary():
    global summary
    message = ""
    showMessage = False

    logger.debug("Process summary entries")

    if getConfiguration(CONF_SHOW_SUMMARY_FOR_KEY) == UI_SHOW_SUMMARY_FOR_INFO_VALUE:
        allEntries = summary.get(SUMMARY_INFOS)
        numberOfEntries = len(allEntries)
        
        if numberOfEntries > 0:
            logger.debug("Rendering summary info message(s)")

            showMessage = True
            message = message + getSummaryMessageFor("Infos", allEntries, 20)

    if getConfiguration(CONF_SHOW_SUMMARY_FOR_KEY) in [UI_SHOW_SUMMARY_FOR_INFO_VALUE, UI_SHOW_SUMMARY_FOR_WARNING_VALUE]:
        allEntries = summary.get(SUMMARY_WARNINGS)
        numberOfEntries = len(allEntries)
        
        if numberOfEntries > 0:
            logger.debug("Rendering summary info message(s)")

            showMessage = True
            message = message + getSummaryMessageFor("Warnings", allEntries, 20)

    if getConfiguration(CONF_SHOW_SUMMARY_FOR_KEY) in [UI_SHOW_SUMMARY_FOR_INFO_VALUE, UI_SHOW_SUMMARY_FOR_WARNING_VALUE, UI_SHOW_SUMMARY_FOR_ERROR_VALUE]:
        allEntries = summary.get(SUMMARY_ERRORS)
        numberOfEntries = len(allEntries)
        
        if numberOfEntries > 0:
            logger.debug("Rendering summary error message(s)")

            showMessage = True
            message = message + getSummaryMessageFor("Errors", allEntries, 20)

    if showMessage:
        logger.debug("Showing summary")
        ao = AppObjects()
        ao.ui.messageBox(message)

def documentHasMeshBodies(exportObjects):
    hasMeshBodies = False

    for exportObject in exportObjects:
        if exportObject.get(REC_HAS_MESH_BODIES):
            return True

    return False

def exportStepAsOneFile(projectName, designName, configurationName, rootComponent, exportObjects, ao):
    # create filename
    fullFileName = getExportName(projectName, designName, configurationName, "", "", True, True, "", UI_EXPORT_TYPES_STEP_VALUE, "")

    # get step export options
    stepExportOptions = ao.export_manager.createSTEPExportOptions(fullFileName, rootComponent)

    # export design as single step file
    exportResult = ao.export_manager.execute(stepExportOptions)
    
    # update summary
    hasMeshBodies = documentHasMeshBodies(exportObjects)

    if exportResult and not hasMeshBodies:
        addInfoToSummary(UI_EXPORT_TYPES_STEP_VALUE, fullFileName)
    else:
        if hasMeshBodies:
            addWarningToSummary(UI_EXPORT_TYPES_STEP_VALUE, "Mesh", fullFileName)
        else:
            addErrorToSummary(UI_EXPORT_TYPES_STEP_VALUE, "UK", fullFileName)

    updateProgressDialog()

def exportStepAsOneFilePerComponent(exportObjects, projectName, designName, configurationName, ao):
    # iterate over list of occurrences
    for exportObject in exportObjects:
        # check if component is unique
        if not exportObject.get(REC_IS_UNIQUE):
            continue

        hasMeshBodies = exportObject.get(REC_HAS_MESH_BODIES)

        # create filename
        fullFileName = getExportName(projectName, designName, configurationName, exportObject.get(REC_OCCURRENCE_PATH), "", False, True, "", UI_EXPORT_TYPES_STEP_VALUE, exportObject.get(REC_PART_NUMBER))

        if len(exportObject.get(REC_BODIES)) == 0 and hasMeshBodies:
            addWarningToSummary(UI_EXPORT_TYPES_STEP_VALUE, "Mesh", fullFileName)
            continue

        # Components with no bodies are REC_IS_TOP_LEVEL == True records with sub-components and no top level bodies. 
        # Those records are creating duplicated / unwanted files in this scenario and can be skipped
        if len(exportObject.get(REC_BODIES)) == 0:
            continue

        # get step export options
        stepExportOptions = ao.export_manager.createSTEPExportOptions(fullFileName, exportObject.get(REC_OCCURRENCE).component)

        # export component as single step file
        exportResult = ao.export_manager.execute(stepExportOptions)

        # update summary
        logger.debug("hasMeshBody: %s", hasMeshBodies)
        if exportResult and not hasMeshBodies:
            addInfoToSummary(UI_EXPORT_TYPES_STEP_VALUE, fullFileName)
        else:
            if hasMeshBodies:
                addWarningToSummary(UI_EXPORT_TYPES_STEP_VALUE, "Mesh", fullFileName)
            else:
                addErrorToSummary(UI_EXPORT_TYPES_STEP_VALUE, "UK", fullFileName)

        updateProgressDialog()

def exportF3dAsOneFile(projectName, designName, configurationName, rootComponent, ao):
    hasExternalLinks = False

    # create filename
    fullFileName = getExportName(projectName, designName, configurationName, "", "", True, True, "", UI_EXPORT_TYPES_F3D_VALUE, "")

    # check if design contains links to external components
    for occurrence in rootComponent.allOccurrences:
        if occurrence.isReferencedComponent:
            logger.warning("%s contains links to an external designs. Skipping export", designName)
            hasExternalLinks = True

    if not hasExternalLinks:
        # get f3d export options
        f3dExportOptions = ao.export_manager.createFusionArchiveExportOptions(fullFileName, rootComponent)

        # export design as single f3d file
        exportResult = ao.export_manager.execute(f3dExportOptions)

        # update summary
        if exportResult:
            addInfoToSummary(UI_EXPORT_TYPES_F3D_VALUE, fullFileName)
        else:
            addErrorToSummary(UI_EXPORT_TYPES_F3D_VALUE, "UK", fullFileName)
    else:
        # update external reference warning to summary
        addErrorToSummary(UI_EXPORT_TYPES_F3D_VALUE, "Link", designName)

    updateProgressDialog()

def exportF3dAsOneFilePerComponent(exportObjects, projectName, designName, configurationName, ao):
    hasExternalLinks = False

    # iterate over list of occurrences
    for exportObject in exportObjects:
        # check if component is unique
        if not exportObject.get(REC_IS_UNIQUE):
            continue

        # Components with no bodies are REC_IS_TOP_LEVEL == True records with sub-components and no top level bodies. 
        # Those records are creating duplicated / unwanted files in this scenario and can be skipped
        if len(exportObject.get(REC_BODIES)) == 0:
            continue

        # create filename
        fullFileName = getExportName(projectName, designName, configurationName, exportObject.get(REC_OCCURRENCE_PATH), "", False, True, "", UI_EXPORT_TYPES_F3D_VALUE, exportObject.get(REC_PART_NUMBER))

        if exportObject.get(REC_IS_REFERENCED_COMPONENT):
            logger.warning("%s is a links to an external designs. Skipping export", exportObject.get(REC_OCCURRENCE_PATH))
            hasExternalLinks = True

        if not hasExternalLinks:
            # get f3d export options
            f3dExportOptions = ao.export_manager.createFusionArchiveExportOptions (fullFileName, exportObject.get(REC_OCCURRENCE).component)

            # export component as single f3d file
            exportResult = ao.export_manager.execute(f3dExportOptions)

            # update summary
            if exportResult:
                addInfoToSummary(UI_EXPORT_TYPES_F3D_VALUE, fullFileName)
            else:
                addErrorToSummary(UI_EXPORT_TYPES_F3D_VALUE, "UK", fullFileName)
        else:
            # update external reference warning to summary
            addErrorToSummary(UI_EXPORT_TYPES_F3D_VALUE, "Link", exportObject.get(REC_OCCURRENCE_PATH))

        updateProgressDialog()

def getStlExportOptions(ao, geometry, fullFileName, refinement):
    # get stl export options
    stlExportOptions = ao.export_manager.createSTLExportOptions(geometry, fullFileName)

    # set export resolution
    if refinement == UI_STL_REFINEMENT_LOW_VALUE:
        stlExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementLow

    elif refinement == UI_STL_REFINEMENT_MEDIUM_VALUE:
        stlExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium

    elif refinement == UI_STL_REFINEMENT_HIGH_VALUE:
        stlExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh

    elif refinement == UI_STL_REFINEMENT_ULTRA_VALUE:
        stlExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementCustom
        # TODO Remove hardcoded values
        stlExportOptions.surfaceDeviation = 0.000508
        stlExportOptions.normalDeviation = 5.0000
    elif refinement == UI_STL_REFINEMENT_CUSTOM_VALUE:
        stlExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementCustom
        stlExportOptions.surfaceDeviation = float(getConfiguration(CONF_STL_SURFACE_DEVIATION_KEY))
        stlExportOptions.normalDeviation = float(getConfiguration(CONF_STL_NORMAL_DEVIATION_KEY))
        stlExportOptions.maximumEdgeLength = float(getConfiguration(CONF_STL_MAX_EDGE_LENGTH_KEY))
        stlExportOptions.aspectRatio = float(getConfiguration(CONF_STL_ASPECT_RATIO_KEY))

    return stlExportOptions

def exportStlAsOneFile(projectName, designName, configurationName, rootComponent, exportObjects, ao):
    for refinement in getConfiguration(CONF_STL_REFINEMENT_KEY):
        # cancel loop if user canceld the dialog
        if progressDialog.wasCancelled:
            progressDialog.hide()
            break

        refinementName = ""
        if len(getConfiguration(CONF_STL_REFINEMENT_KEY)) > 1:
            # set refinement name if more than one refinement is defined to keep the exportname unique
            refinementName = refinement

        # create filename
        fullFileName = getExportName(projectName, designName, configurationName, "", "", True, True, refinementName, UI_EXPORT_TYPES_STL_VALUE, "")

        # get stl export options
        stlExportOptions = getStlExportOptions(ao, rootComponent, fullFileName, refinement)

        # export design as single stl file
        exportResult = ao.export_manager.execute(stlExportOptions)

        # update summary
        hasMeshBodies = documentHasMeshBodies(exportObjects)

        if exportResult and not hasMeshBodies:
            addInfoToSummary(UI_EXPORT_TYPES_STL_VALUE, fullFileName)
        else:
            if hasMeshBodies:
                addWarningToSummary(UI_EXPORT_TYPES_STL_VALUE, "Mesh", fullFileName)
            else:
                addErrorToSummary(UI_EXPORT_TYPES_STL_VALUE, "UK", fullFileName)

        updateProgressDialog()

def exportStlAsOneFilePerBodyInComponent(exportObjects, projectName, designName, configurationName, ao):
    for refinement in getConfiguration(CONF_STL_REFINEMENT_KEY):
        # cancel loop if user canceld the dialog
        if progressDialog.wasCancelled:
            progressDialog.hide()
            break

        # set refinement name
        refinementName = ""
        if len(getConfiguration(CONF_STL_REFINEMENT_KEY)) > 1:
            # set refinement name if more than one refinement is defined to keep the exportname unique
            refinementName = refinement

        # iterate over list of occurrences
        for exportObject in exportObjects:
            # cancel loop if user canceld the dialog
            if progressDialog.wasCancelled:
                progressDialog.hide()
                break

            # check if component is unique
            if not exportObject.get(REC_IS_UNIQUE):
                continue

            hasMeshBodies = exportObject.get(REC_HAS_MESH_BODIES)

            if len(exportObject.get(REC_BODIES)) == 0 and hasMeshBodies:
                path = ""
                if exportObject.get(REC_OCCURRENCE) != "":
                    path = exportObject.get(REC_OCCURRENCE).name
                else:
                    path = "root"

                addWarningToSummary(UI_EXPORT_TYPES_STL_VALUE, "Mesh", path)
            
            # Components with no bodies are REC_IS_TOP_LEVEL == True records with sub-components and no top level bodies. 
            # Those records are creating duplicated / unwanted files in this scenario and can be skipped
            if len(exportObject.get(REC_BODIES)) == 0:
                continue

            # iterate over list of bodies
            for body in exportObject.get(REC_BODIES):
                # cancel loop if user canceld the dialog
                if progressDialog.wasCancelled:
                    progressDialog.hide()
                    break

                # create filename
                fullFileName = getExportName(projectName, designName, configurationName, exportObject.get(REC_OCCURRENCE_PATH), body.name, False, True, refinementName, UI_EXPORT_TYPES_STL_VALUE, "")

                # get stl export options
                stlExportOptions = getStlExportOptions(ao, body, fullFileName, refinement)

                # export body as single stl file
                exportResult = ao.export_manager.execute(stlExportOptions)

                # update summary
                if exportResult:
                    addInfoToSummary(UI_EXPORT_TYPES_STL_VALUE, fullFileName)
                else:
                    addErrorToSummary(UI_EXPORT_TYPES_STL_VALUE, "UK", fullFileName)

                updateProgressDialog()

def exportStlAsOneFilePerBodyInOccurrence(exportObjects, projectName, designName, configurationName, ao):
    # generate exports for each selected refinement
    for refinement in getConfiguration(CONF_STL_REFINEMENT_KEY):
        # cancel loop if user canceld the dialog
        if progressDialog.wasCancelled:
            progressDialog.hide()
            break
        # set refinement name

        refinementName = ""
        if len(getConfiguration(CONF_STL_REFINEMENT_KEY)) > 1:
            # set refinement name if more than one refinement is defined to keep the exportname unique
            refinementName = refinement

        # iterate over list of occurrences
        for exportObject in exportObjects:
            # cancel loop if user canceld the dialog
            if progressDialog.wasCancelled:
                progressDialog.hide()
                break

            # Components with no bodies are REC_IS_TOP_LEVEL == True records with sub-components and no top level bodies. 
            # Those records are creating duplicated / unwanted files in this scenario and can be skipped
            if len(exportObject.get(REC_BODIES)) == 0:
                continue

            hasMeshBodies = exportObject.get(REC_HAS_MESH_BODIES)

            if len(exportObject.get(REC_BODIES)) == 0 and hasMeshBodies:
                path = ""
                if exportObject.get(REC_OCCURRENCE) != "":
                    path = exportObject.get(REC_OCCURRENCE).name
                else:
                    path = "root"
                    
                addWarningToSummary(UI_EXPORT_TYPES_STL_VALUE, "Mesh", path)

            # iterate over list of bodies
            for body in exportObject.get(REC_BODIES):
                # cancel loop if user canceld the dialog
                if progressDialog.wasCancelled:
                    progressDialog.hide()
                    break

                # create filename but remove occurrence id unless they're part of the occurrence name in the temporary document
                fullFileName = getExportName(projectName, designName, configurationName, exportObject.get(REC_OCCURRENCE_PATH), body.name, False, True, refinementName, UI_EXPORT_TYPES_STL_VALUE, "")

                # get stl export options
                stlExportOptions = getStlExportOptions(ao, body, fullFileName, refinement)

                # export body as single stl file
                exportResult = ao.export_manager.execute(stlExportOptions)

                # update summary
                if exportResult:
                    addInfoToSummary(UI_EXPORT_TYPES_STL_VALUE, fullFileName)
                else:
                    addErrorToSummary(UI_EXPORT_TYPES_STL_VALUE, "UK", fullFileName)

                updateProgressDialog()

def exportStlAsOneFilePerTopOccurrence(exportObjects, projectName, designName, configurationName, ao):
    # generate exports for each selected refinement
    for refinement in getConfiguration(CONF_STL_REFINEMENT_KEY):
        # cancel loop if user canceld the dialog
        if progressDialog.wasCancelled:
            progressDialog.hide()
            break
        # set refinement name

        refinementName = ""
        if len(getConfiguration(CONF_STL_REFINEMENT_KEY)) > 1:
            # set refinement name if more than one refinement is defined to keep the exportname unique
            refinementName = refinement

        # iterate over list of occurrences
        for exportObject in exportObjects:
            try:
                # cancel loop if user canceld the dialog
                if progressDialog.wasCancelled:
                    progressDialog.hide()
                    break

                # check if component is unique+
                if not exportObject.get(REC_IS_TOP_LEVEL):
                    continue

                # create filename but remove occurrence id unless they're part of the occurrence name in the temporary document
                fullFileName = getExportName(projectName, designName, configurationName, exportObject.get(REC_OCCURRENCE_PATH), "", False, True, refinementName, UI_EXPORT_TYPES_STL_VALUE, "")

                # get stl export options
                stlExportOptions = getStlExportOptions(ao, exportObject.get(REC_OCCURRENCE), fullFileName, refinement)

                # export body as single stl file
                exportResult = ao.export_manager.execute(stlExportOptions)

                # update summary
                if exportResult:
                    addInfoToSummary(UI_EXPORT_TYPES_STL_VALUE, fullFileName)
                else:
                    addErrorToSummary(UI_EXPORT_TYPES_STL_VALUE, "UK", fullFileName)

                updateProgressDialog()
            except:
                logger.error(traceback.format_exc())

def get3mfExportOptions(ao, geometry, fullFileName, refinement):
    # get 3mf export options
    c3mfExportOptions = ao.export_manager.createC3MFExportOptions(geometry, fullFileName)

    # set export resolution
    if refinement == UI_3MF_REFINEMENT_LOW_VALUE:
        c3mfExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementLow

    elif refinement == UI_3MF_REFINEMENT_MEDIUM_VALUE:
        c3mfExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementMedium

    elif refinement == UI_3MF_REFINEMENT_HIGH_VALUE:
        c3mfExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementHigh

    elif refinement == UI_3MF_REFINEMENT_ULTRA_VALUE:
        c3mfExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementCustom
        c3mfExportOptions.surfaceDeviation = 0.000508
        c3mfExportOptions.normalDeviation = 5.0000
    elif refinement == UI_3MF_REFINEMENT_CUSTOM_VALUE:
        c3mfExportOptions.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementCustom
        c3mfExportOptions.surfaceDeviation = float(getConfiguration(CONF_3MF_SURFACE_DEVIATION_KEY))
        c3mfExportOptions.normalDeviation = float(getConfiguration(CONF_3MF_NORMAL_DEVIATION_KEY))
        c3mfExportOptions.maximumEdgeLength = float(getConfiguration(CONF_3MF_MAX_EDGE_LENGTH_KEY))
        c3mfExportOptions.aspectRatio = float(getConfiguration(CONF_3MF_ASPECT_RATIO_KEY))

    return c3mfExportOptions

def export3mfAsOneFile(projectName, designName, configurationName, rootComponent, exportObjects, ao):
    for refinement in getConfiguration(CONF_3MF_REFINEMENT_KEY):
        # cancel loop if user canceld the dialog
        if progressDialog.wasCancelled:
            progressDialog.hide()
            break

        refinementName = ""
        if len(getConfiguration(CONF_3MF_REFINEMENT_KEY)) > 1:
            # set refinement name if more than one refinement is defined to keep the exportname unique
            refinementName = refinement

        # create filename
        fullFileName = getExportName(projectName, designName, configurationName, "", "", True, True, refinementName, UI_EXPORT_TYPES_3MF_VALUE, "")

        # get 3mf export options
        c3mfExportOptions = get3mfExportOptions(ao, rootComponent, fullFileName, refinement)

        # export design as single 3mf file
        exportResult = ao.export_manager.execute(c3mfExportOptions)

        # update summary
        hasMeshBodies = documentHasMeshBodies(exportObjects)

        if exportResult and not hasMeshBodies:
            addInfoToSummary(UI_EXPORT_TYPES_3MF_VALUE, fullFileName)
        else:
            if hasMeshBodies:
                addWarningToSummary(UI_EXPORT_TYPES_3MF_VALUE, "Mesh", fullFileName)
            else:
                addErrorToSummary(UI_EXPORT_TYPES_3MF_VALUE, "UK", fullFileName)

        updateProgressDialog()

def export3mfAsOneFilePerBodyInComponent(exportObjects, projectName, designName, configurationName, ao):
    for refinement in getConfiguration(CONF_3MF_REFINEMENT_KEY):
        # cancel loop if user canceld the dialog
        if progressDialog.wasCancelled:
            progressDialog.hide()
            break

        # set refinement name
        refinementName = ""
        if len(getConfiguration(CONF_3MF_REFINEMENT_KEY)) > 1:
            # set refinement name if more than one refinement is defined to keep the exportname unique
            refinementName = refinement

        # iterate over list of occurrences
        for exportObject in exportObjects:
            # cancel loop if user canceld the dialog
            if progressDialog.wasCancelled:
                progressDialog.hide()
                break

            # check if component is unique
            if not exportObject.get(REC_IS_UNIQUE):
                continue

            hasMeshBodies = exportObject.get(REC_HAS_MESH_BODIES)

            if len(exportObject.get(REC_BODIES)) == 0 and hasMeshBodies:
                path = ""
                if exportObject.get(REC_OCCURRENCE) != "":
                    path = exportObject.get(REC_OCCURRENCE).name
                else:
                    path = "root"

                addWarningToSummary(UI_EXPORT_TYPES_3MF_VALUE, "Mesh", path)
            
            # Components with no bodies are REC_IS_TOP_LEVEL == True records with sub-components and no top level bodies. 
            # Those records are creating duplicated / unwanted files in this scenario and can be skipped
            if len(exportObject.get(REC_BODIES)) == 0:
                continue

            # iterate over list of bodies
            for body in exportObject.get(REC_BODIES):
                # cancel loop if user canceld the dialog
                if progressDialog.wasCancelled:
                    progressDialog.hide()
                    break

                # create filename
                fullFileName = getExportName(projectName, designName, configurationName, exportObject.get(REC_OCCURRENCE_PATH), body.name, False, True, refinementName, UI_EXPORT_TYPES_3MF_VALUE, "")

                # get 3mf export options
                c3mfExportOptions = get3mfExportOptions(ao, body, fullFileName, refinement)

                # export body as single 3mf file
                exportResult = ao.export_manager.execute(c3mfExportOptions)

                # update summary
                if exportResult:
                    addInfoToSummary(UI_EXPORT_TYPES_3MF_VALUE, fullFileName)
                else:
                    addErrorToSummary(UI_EXPORT_TYPES_3MF_VALUE, "UK", fullFileName)

                updateProgressDialog()

def export3mfAsOneFilePerBodyInOccurrence(exportObjects, projectName, designName, configurationName, ao):
    # generate exports for each selected refinement
    for refinement in getConfiguration(CONF_3MF_REFINEMENT_KEY):
        # cancel loop if user canceld the dialog
        if progressDialog.wasCancelled:
            progressDialog.hide()
            break
        # set refinement name

        refinementName = ""
        if len(getConfiguration(CONF_3MF_REFINEMENT_KEY)) > 1:
            # set refinement name if more than one refinement is defined to keep the exportname unique
            refinementName = refinement

        # iterate over list of occurrences
        for exportObject in exportObjects:
            # cancel loop if user canceld the dialog
            if progressDialog.wasCancelled:
                progressDialog.hide()
                break

            # Components with no bodies are REC_IS_TOP_LEVEL == True records with sub-components and no top level bodies. 
            # Those records are creating duplicated / unwanted files in this scenario and can be skipped
            if len(exportObject.get(REC_BODIES)) == 0:
                continue

            hasMeshBodies = exportObject.get(REC_HAS_MESH_BODIES)

            if len(exportObject.get(REC_BODIES)) == 0 and hasMeshBodies:
                path = ""
                if exportObject.get(REC_OCCURRENCE) != "":
                    path = exportObject.get(REC_OCCURRENCE).name
                else:
                    path = "root"
                    
                addWarningToSummary(UI_EXPORT_TYPES_3MF_VALUE, "Mesh", path)

            # iterate over list of bodies
            for body in exportObject.get(REC_BODIES):
                # cancel loop if user canceld the dialog
                if progressDialog.wasCancelled:
                    progressDialog.hide()
                    break

                # create filename but remove occurrence id unless they're part of the occurrence name in the temporary document
                fullFileName = getExportName(projectName, designName, configurationName, exportObject.get(REC_OCCURRENCE_PATH), body.name, False, True, refinementName, UI_EXPORT_TYPES_3MF_VALUE, "")

                # get 3mf export options
                c3mfExportOptions = get3mfExportOptions(ao, body, fullFileName, refinement)

                # export body as single 3mf file
                exportResult = ao.export_manager.execute(c3mfExportOptions)

                # update summary
                if exportResult:
                    addInfoToSummary(UI_EXPORT_TYPES_3MF_VALUE, fullFileName)
                else:
                    addErrorToSummary(UI_EXPORT_TYPES_3MF_VALUE, "UK", fullFileName)

                updateProgressDialog()

def export3mfAsOneFilePerTopOccurrence(exportObjects, projectName, designName, configurationName, ao):
    # generate exports for each selected refinement
    for refinement in getConfiguration(CONF_3MF_REFINEMENT_KEY):
        # cancel loop if user canceld the dialog
        if progressDialog.wasCancelled:
            progressDialog.hide()
            break
        # set refinement name

        refinementName = ""
        if len(getConfiguration(CONF_3MF_REFINEMENT_KEY)) > 1:
            # set refinement name if more than one refinement is defined to keep the exportname unique
            refinementName = refinement

        # iterate over list of occurrences
        for exportObject in exportObjects:
            try:
                # cancel loop if user canceld the dialog
                if progressDialog.wasCancelled:
                    progressDialog.hide()
                    break

                # check if component is unique+
                if not exportObject.get(REC_IS_TOP_LEVEL):
                    continue

                # create filename but remove occurrence id unless they're part of the occurrence name in the temporary document
                fullFileName = getExportName(projectName, designName, configurationName, exportObject.get(REC_OCCURRENCE_PATH), "", False, True, refinementName, UI_EXPORT_TYPES_3MF_VALUE, "")

                # get 3mf export options
                c3mfExportOptions = get3mfExportOptions(ao, exportObject.get(REC_OCCURRENCE), fullFileName, refinement)

                # export body as single 3mf file
                exportResult = ao.export_manager.execute(c3mfExportOptions)

                # update summary
                if exportResult:
                    addInfoToSummary(UI_EXPORT_TYPES_3MF_VALUE, fullFileName)
                else:
                    addErrorToSummary(UI_EXPORT_TYPES_3MF_VALUE, "UK", fullFileName)

                updateProgressDialog()
            except:
                logger.error(traceback.format_exc())

def resetData():
    global progressDialog
    global progressValue
    global summary

    # reset configuration
    resetConfiguration()

    # reset progress dialog
    progressDialog = adsk.core.ProgressDialog.cast(None)
    progressValue = 0

    # reset summary data
    summary = {SUMMARY_INFOS: [], SUMMARY_WARNINGS: [], SUMMARY_ERRORS: []}

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

            # reset configuration
            resetData()

        except:
            logger.info("--------------------------------------------------------------------------------")
            logger.info("Finished")
            logger.info("--------------------------------------------------------------------------------")

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input, input_values):
        logger.debug("changed_input.objectType: %s", changed_input.objectType)
        
        # process changed element
        if changed_input.objectType == 'adsk::core::CommandInput':
            pass
        elif changed_input.objectType == 'adsk::core::SelectionCommandInput':
            pass
        elif type(input_values[changed_input.id]) == adsk.core.ListItems:
            # element supports a list of selections. Process all selected elements
            setConfiguration(changed_input.id, getSelectedDropDownItems(inputs, changed_input.id))
        else:
            # element is a single element
            setConfiguration(changed_input.id, input_values[changed_input.id])

        # check if the integrity between configured parameters are still valid
        validateConfiguration(inputs)

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        try:
            ao = AppObjects()
            rootComponent = ao.design.rootComponent
            designName = rootComponent.name
            activeDocument = ao.app.activeDocument
            projectName = activeDocument.dataFile.parentProject.name

            if ao.design.isConfiguredDesign:
                configurationName = ao.design.configurationTopTable.activeRow.name
            else:
                configurationName = None
 
            logger.info("--------------------------------------------------------------------------------")
            logger.info("Starting processing of %s - %s", projectName, designName)
            logger.info("--------------------------------------------------------------------------------")

            if input_values.get(UI_EXPORT_DIRECTORY_RESET_ID) or getConfiguration(CONF_EXPORT_DIRECTORY_CONFIGURE_KEY) == UI_EXPORT_DIRECTORY_CONFIGURE_ALWAYS_VALUE:
                resetExportDirecotry(input_values)
            
            validateExportDirectory()

            # print configuration to the log file
            logConfiguration()

            # write configuration to document because some settings might loose link to this document
            ao = AppObjects()
            writeConfiguration(ao.document, CONF_PROJECT_ATTRIBUTE_GROUP, CONF_PROJECT_ATTRIBUTE_KEY)

            # create progress dialog
            global progressDialog
            global progressValue

            logger.debug("Initializing progressDialog")

            progressDialog = ao.ui.createProgressDialog()
            progressDialog.cancelButtonText = 'Cancel'
            progressDialog.isBackgroundTranslucent = False
            progressDialog.isCancelButtonShown = True
            progressValue = 0

            # get list of occurrences and bodies
            logger.debug("getting list of export objects")
            exportObjects = getExportObjects(rootComponent, input_values.get(UI_EXPORT_OPTIONS_BODIES_SELECTION_ID), True)

            # Show progress dialog
            logger.debug("Showing progressDialog")
            
            numberOfExportObjects = totalNumberOfObjects(exportObjects) * len(configList)
            
            try:
                progressDialog.show('ExportIt', 'Exports created: %v of %m' , 0, numberOfExportObjects, 0)
            except:
                pass

            tmpExportObjects = []

            if not progressDialog.wasCancelled and UI_EXPORT_TYPES_F3D_VALUE in getConfiguration(CONF_EXPORT_OPTIONS_TYPE_KEY):
                # export design as one step file
                if  not progressDialog.wasCancelled and UI_STRUCTURE_ONE_FILE_VALUE in getConfiguration(CONF_F3D_STRUCTURE_KEY):
                    exportF3dAsOneFile(projectName, designName, configurationName, rootComponent, ao)

                # export each component as individual step files
                if  not progressDialog.wasCancelled and UI_STRUCTURE_ONE_FILE_PER_COMPONENT_VALUE in getConfiguration(CONF_F3D_STRUCTURE_KEY):
                    exportF3dAsOneFilePerComponent(exportObjects, projectName, designName, configurationName, ao)

            if  not progressDialog.wasCancelled and UI_EXPORT_TYPES_STEP_VALUE in getConfiguration(CONF_EXPORT_OPTIONS_TYPE_KEY):
                # export design as one step file
                if  not progressDialog.wasCancelled and UI_STRUCTURE_ONE_FILE_VALUE in getConfiguration(CONF_STEP_STRUCTURE_KEY):
                    exportStepAsOneFile(projectName, designName, configurationName,
                                        rootComponent, exportObjects, ao)

                # export each component as individual step files
                if  not progressDialog.wasCancelled and UI_STRUCTURE_ONE_FILE_PER_COMPONENT_VALUE in getConfiguration(CONF_STEP_STRUCTURE_KEY):
                    exportStepAsOneFilePerComponent(exportObjects, projectName, designName, configurationName, ao)

            if not progressDialog.wasCancelled and UI_EXPORT_TYPES_STL_VALUE in getConfiguration(CONF_EXPORT_OPTIONS_TYPE_KEY):
                # export design as one stl file
                if  not progressDialog.wasCancelled and UI_STRUCTURE_ONE_FILE_VALUE in getConfiguration(CONF_STL_STRUCTURE_KEY):
                    exportStlAsOneFile(projectName, designName, configurationName, rootComponent, exportObjects, ao)

                # export each body in component as individual stl files
                if not progressDialog.wasCancelled and UI_STRUCTURE_ONE_FILE_PER_BODY_IN_COMPONENT_VALUE in getConfiguration(CONF_STL_STRUCTURE_KEY):
                    exportStlAsOneFilePerBodyInComponent(
                        exportObjects, projectName, designName, configurationName, ao)

                if not progressDialog.wasCancelled and (UI_STRUCTURE_ONE_FILE_PER_BODY_IN_OCCURRENCE_VALUE in getConfiguration(CONF_STL_STRUCTURE_KEY)
                    or UI_STRUCTURE_ONE_FILE_PER_TOP_LEVEL_OCCURRENCE_VALUE in getConfiguration(CONF_STL_STRUCTURE_KEY)):
                    # copy exportObjects into a temporary document and convert all occurrences into unique components.
                    tmpDocument, tmpRootComponent = copyDesignToExportDocument(exportObjects)

                    # regenerate list of export objects based
                    tmpExportObjects = getExportObjects(tmpRootComponent, [], False)

                    # export each body in occurrence as individual stl files
                    if not progressDialog.wasCancelled and UI_STRUCTURE_ONE_FILE_PER_BODY_IN_OCCURRENCE_VALUE in getConfiguration(CONF_STL_STRUCTURE_KEY):
                        exportStlAsOneFilePerBodyInOccurrence(tmpExportObjects, projectName, designName, configurationName, ao)

                    # export each top level occurrence as individual stl files
                    if not progressDialog.wasCancelled and UI_STRUCTURE_ONE_FILE_PER_TOP_LEVEL_OCCURRENCE_VALUE in getConfiguration(CONF_STL_STRUCTURE_KEY):
                        exportStlAsOneFilePerTopOccurrence(tmpExportObjects, projectName, designName, configurationName, ao)

            if not progressDialog.wasCancelled and UI_EXPORT_TYPES_3MF_VALUE in getConfiguration(CONF_EXPORT_OPTIONS_TYPE_KEY):
                # export design as one 3mf file
                if  not progressDialog.wasCancelled and UI_STRUCTURE_ONE_FILE_VALUE in getConfiguration(CONF_3MF_STRUCTURE_KEY):
                    export3mfAsOneFile(projectName, designName, configurationName, rootComponent, exportObjects, ao)

                # export each body in component as individual 3mf files
                if not progressDialog.wasCancelled and UI_STRUCTURE_ONE_FILE_PER_BODY_IN_COMPONENT_VALUE in getConfiguration(CONF_3MF_STRUCTURE_KEY):
                    export3mfAsOneFilePerBodyInComponent(exportObjects, projectName, designName, configurationName, ao)

                if not progressDialog.wasCancelled and (UI_STRUCTURE_ONE_FILE_PER_BODY_IN_OCCURRENCE_VALUE in getConfiguration(CONF_3MF_STRUCTURE_KEY)
                    or UI_STRUCTURE_ONE_FILE_PER_TOP_LEVEL_OCCURRENCE_VALUE in getConfiguration(CONF_3MF_STRUCTURE_KEY)):

                    if not tmpExportObjects:
                        # copy exportObjects into a temporary document and convert all occurrences into unique components.
                        tmpDocument, tmpRootComponent = copyDesignToExportDocument(exportObjects)

                        # regenerate list of export objects based
                        tmpExportObjects = getExportObjects(tmpRootComponent, [], False)

                    # export each body in occurrence as individual 3mf files
                    if not progressDialog.wasCancelled and UI_STRUCTURE_ONE_FILE_PER_BODY_IN_OCCURRENCE_VALUE in getConfiguration(CONF_3MF_STRUCTURE_KEY):
                        export3mfAsOneFilePerBodyInOccurrence(tmpExportObjects, projectName, designName, configurationName, ao)

                    # export each top level occurrence as individual 3mf files
                    if not progressDialog.wasCancelled and UI_STRUCTURE_ONE_FILE_PER_TOP_LEVEL_OCCURRENCE_VALUE in getConfiguration(CONF_3MF_STRUCTURE_KEY):
                        export3mfAsOneFilePerTopOccurrence(tmpExportObjects, projectName, designName, configurationName, ao)

            # hide progress dialog
            if progressDialog.isShowing:
                logger.debug("Hiding progressDialog")
                progressDialog.progressValue = numberOfExportObjects
                progressDialog.hide()

            # write modified configuration
            writeConfiguration(ao.document, CONF_PROJECT_ATTRIBUTE_GROUP, CONF_PROJECT_ATTRIBUTE_KEY)
            
            if getConfiguration(CONF_AUTOSAVE_PROJECT_CONFIGURATION_KEY):
                saveConfigurationInDocument(activeDocument, getConfiguration(CONF_AUTOSAVE_DESCRIPTION_KEY))
            else:
                showSaveConfigWarning()

            # show summary
            showSummary()

        except:
            logger.error(traceback.format_exc())

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
            resetData()
            initializeConfiguration(ao.document, CONF_PROJECT_ATTRIBUTE_GROUP, CONF_PROJECT_ATTRIBUTE_KEY, createDefaultConfiguration())

            #print configuration to the log file
            logConfiguration()

            # check for new version
            isCheckOverdue = checkForUpdates()
            logger.debug("isCheckOverdue %s", isCheckOverdue)
            showReleaseNotes(isCheckOverdue, ao)

            # create UI elements and populate configuration to the fields
            initializeUi(inputs, False, isCheckOverdue)

            # check if the integrity between configured parameters are still valid
            validateConfiguration(inputs)

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

            logger.error(traceback.format_exc())
