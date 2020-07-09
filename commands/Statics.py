import logging

# log settings
LOG_FORMAT = '%(levelname)-7s; %(funcName)-26s; %(lineno)3d; %(message)s'                   # format of the log messages
LOG_LEVEL = logging.DEBUG                                                                   # logging level

# configuration - common
CONF_DEFAULT_CONFIG_NAME = 'Defaults.json'                                                  # name of the configuration file that stores the default configuration
CONF_PROJECT_ATTRIBUTE_GROUP = 'ExportIt'                                                   # name of the attribute group that stores the project specific data
CONF_PROJECT_ATTRIBUTE_KEY = 'projectConfiguration'                                         # key of the key that contains the project specific configuration (delta to default configuration)
CONF_VERSION_KEY = 'version'                                                                # key of the element that contains the version of the default configuration
CONF_VERSION_DEFAULT = '0.1.0'                                                              # default version of the default configuration

# configuration - export directory
CONF_EXPORT_DIRECTORY_KEY = 'exportDirectory'                                               # key of the element that contains the export directory
CONF_EXPORT_DIRECTORY_DEFAULT = ''                                                          # value that's used to initialize the export directory
