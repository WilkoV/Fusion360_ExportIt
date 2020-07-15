import adsk.core
import os, json

from json import encoder
from .BaseLogger import logger
from .Statics import *

# set format of float values
encoder.FLOAT_REPR = lambda o: format(o, '.6f')

defaultConfiguration = {}           # contains the default configuration
projectConfiguration = {}           # changed parameters in comperasion to the default configuration (so only the delta)
configurationChanged = False        # indicator if the configuration has changed
editDefaultsMode = False            # true if only defaults should be edited otherwise false

def getConfigurationDirectory():
    # render path name
    appPath = os.path.dirname(os.path.abspath(__file__))
    configPath = os.path.join(appPath, 'config')

    # create directory
    os.makedirs(configPath, 0o777, True)

    # return path name
    return configPath

def writeDefaultConfiguration():
    global defaultConfiguration

    with open(os.path.join(getConfigurationDirectory(), CONF_DEFAULT_CONFIG_NAME), 'w') as jsonOutFile:
        # write pretty printed json file
        json.dump(defaultConfiguration, jsonOutFile, indent=4)
        jsonOutFile.flush()
        jsonOutFile.close()

    logger.info('Configuration written to %s', CONF_DEFAULT_CONFIG_NAME)

def getDefaultConfiguration(key, staticValue):
    global defaultConfiguration

    # get default value
    value = defaultConfiguration.get(key)
    logger.debug("default value: %s", value)

    # check if default is available
    if not value:
        # use static value because default configuration is broken
        value = staticValue
        logger.debug("static value: %s", value)

    return value

def writeConfiguration(document, group, key):
    global editDefaultsMode
    global projectConfiguration
    global configurationChanged

    if not editDefaultsMode:
        if configurationChanged:
            logger.info("Adding configuration to document attribute. User has to save the desgin")

            # render json string
            jsonData = json.dumps(projectConfiguration, indent=4)

            # write json data to document
            document.attributes.add(group, key, jsonData)
    else:
        logger.debug("editDefaultsMode is enabled: redirect to writeDefaultConfiguration()")
        writeDefaultConfiguration()

def getConfiguration(key):
    global defaultConfiguration
    global projectConfiguration
    global editDefaultsMode

    value = None

    if not editDefaultsMode:
        try:
            # try to get value from recent changes
            value = projectConfiguration[key]
            # logger.debug("%s -> %s (project configuration)", key, value)
        except:
            # use default values
            value = defaultConfiguration.get(key, '')
            # logger.debug("%s -> %s (default configuration)", key, value)
    else:
       logger.debug("editDefaultsMode is enabled: default settings are used")
       value = defaultConfiguration.get(key, '')

    return value

def setDefaultConfiguration(key, value):
    global defaultConfiguration

    logger.debug('setting default for %s from >%s< to >%s<', key, getConfiguration(key), value)
    defaultConfiguration[key] = value

def setConfiguration(key, value):
    global editDefaultsMode
    global projectConfiguration
    global configurationChanged

    if not editDefaultsMode:
        logger.debug('setting %s from >%s< to >%s<', key, getConfiguration(key), value)

        projectConfiguration[key] = value
        configurationChanged = True
    else:
        logger.debug("editDefaultsMode is enabled: redirect to setDefaultConfiguration(key,value)")
        setDefaultConfiguration(key, value)

def resetConfiguration():
    global defaultConfiguration
    global configurationChanged
    global projectConfiguration
    global editDefaultsMode

    # reset data from last run
    defaultConfiguration = {}           # contains the default configuration
    projectConfiguration = {}           # changed parameters in comperasion to the default configuration (so only the delta)
    configurationChanged = False        # indicator if the configuration has changed
    editDefaultsMode = False            # true if only defaults should be edited otherwise false

def initializeConfiguration(document, attributeGroup, attributeKey, generatedConfiguration):
    # configuration dictionaries
    global defaultConfiguration
    global projectConfiguration
    global configurationChanged
    global editDefaultsMode

    resetConfiguration()

    # load default configuration
    logger.debug('loading defaults')

    jsonData = {}

    try:
        # open file with read access
        with open(os.path.join(getConfigurationDirectory(), CONF_DEFAULT_CONFIG_NAME)) as jsonFile:
            # read json file
            defaultConfiguration = json.load(jsonFile)

        logger.debug('default configuration loaded from%s in direcotry %s', CONF_DEFAULT_CONFIG_NAME, getConfigurationDirectory())
    except:
        logger.warning('Could not find or load %s in direcotry %s', CONF_DEFAULT_CONFIG_NAME, getConfigurationDirectory())

    # no defaults found?
    if len(defaultConfiguration) == 0:
        defaultConfiguration = generatedConfiguration
        writeDefaultConfiguration()

        logger.info('New %s file create in %s', CONF_DEFAULT_CONFIG_NAME, os.path.join(getConfigurationDirectory()))

    # check if new default version is available
    generatedVersion = generatedConfiguration.get(CONF_VERSION_KEY)
    logger.debug("generateVersion: %s", generatedVersion)
    logger.debug("defaultConfiguration.get(CONF_VERSION_KEY): %s", defaultConfiguration.get(CONF_VERSION_KEY))

    if not generatedVersion == defaultConfiguration.get(CONF_VERSION_KEY):
        logger.info("Default configuration is outdated")

        modified = False

        for key in generatedConfiguration:
            try:
                # try to find the key from the generatedConfiguration in the stored configuration
                defaultConfiguration[key]

                if key == CONF_VERSION_KEY:
                    modified = True
                    setDefaultConfiguration(key,generatedConfiguration.get(key))
                else:
                    logger.debug("%s found in default configuration", key)
            except:
                # key from generated configuration couldn't be found in stored configuration. Add it
                modified = True
                setDefaultConfiguration(key, generatedConfiguration[key])

                logger.debug("%s = %s added to default configuration", key, generatedConfiguration[key])

        if modified:
            writeDefaultConfiguration()

    if document:
        # load project configuration
        projectConfiguration = {}
        attribute = document.attributes.itemByName(attributeGroup, attributeKey)

        try:
            projectConfiguration = json.loads(attribute.value)
        except:
            pass

        if len(projectConfiguration) == 0:
            projectConfiguration = defaultConfiguration
            configurationChanged = True

            logger.info('No project configuration found. Defaults copied to project configuration')

        try:
            projectConfiguration = json.loads(attribute.value)
            logger.debug("project configuration loaded")
        except:
            projectConfiguration = {}
            logger.debug("no project configuration found")
    else:
        editDefaultsMode = True
        logger.debug("Edit defaults mode enabled")

def logConfiguration():
    global projectConfiguration

    # Get the project value for each key in the default configuration. If no project value is defined, defaults are used
    for key in defaultConfiguration:
        logger.info('%s = %s', key, getConfiguration(key))

def showSaveConfigWarning():
    global configurationChanged

    if configurationChanged:
        app = adsk.core.Application.get()
        ui = app.userInterface

        ui.messageBox("ExportIt's configuration has changed.\nSave your design to persist the changes or use the undo function to discard the changes")
        logger.info("ExportIt's configuration has changed. Save your design to persist the changes or use the undo function to discard the changes")

    configurationChanged = False