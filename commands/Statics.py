import logging

# log settings
LOG_FORMAT = '%(levelname)-7s; %(funcName)-26s; %(lineno)3d; %(message)s'                   # format of the log messages
LOG_LEVEL = logging.DEBUG                                                                   # logging level

# user interface - export directory
UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID = 'ExportDirectoryOptions'                             # group id that contains the export directory UI elements
UI_EXPORT_DIRECTORY_OPTIONS_GROUP_NAME = 'Export Directory Options'                         # name of the group that contains the export directory UI elements

UI_EXPORT_DIRECTORY_NAME = 'Export Directory'                                               # base path for the export process

UI_EXPORT_DIRECTORY_ADD_PROJECT_NAME_NAME = 'Add Project Name'                              # True if the name of the project should be added to the export directory otherwise False
UI_EXPORT_DIRECTORY_ADD_DESIGN_NAME_NAME = 'Add Design Name'                                # True if the name of the design should be added to the export directory otherwise False

# user interface - common
UI_STRUCTURE_ONE_FILE_VALUE = 'One File'                                                    # Export as one file
UI_STRUCTURE_ONE_FILE_PER_BODY_IN_COMPONENT_VALUE = 'One File Per Body In Component'        # Export as one file per body in unique component
UI_STRUCTURE_ONE_FILE_PER_BODY_IN_OCCURRENCE_VALUE = 'One File Per Body In Occurrence'      # Export as one file per body in unique occurrence

# user interface - stl options
UI_STL_OPTIONS_GROUP_ID = 'StlOptions'                                                      # group id that contains the stl options UI elements
UI_STL_OPTIONS_GROUP_NAME = 'STL Options'                                                   # name of the group that contains the stl options UI elements

UI_STL_STRUCTURE_NAME = 'Structure'                                                         # Export bodies as one file, file per body etc.
UI_STL_STRUCTURE_VALUES = [UI_STRUCTURE_ONE_FILE_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_BODY_IN_COMPONENT_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_BODY_IN_OCCURRENCE_VALUE]             # Elements of the dropdown list

UI_STL_REFINEMENT_NAME = 'Refinement'                                                       # refinement (resolution / density) for stl exports
UI_STL_REFINEMENT_ULTRA_VALUE = 'Ultra'                                                     # refinement ultra
UI_STL_REFINEMENT_HIGH_VALUE = 'High'                                                       # refinement high
UI_STL_REFINEMENT_MEDIUM_VALUE = 'Medium'                                                   # refinement medium
UI_STL_REFINEMENT_LOW_VALUE = 'Low'                                                         # refinement low

UI_STL_REFINEMENT_VALUES = [UI_STL_REFINEMENT_ULTRA_VALUE,
                            UI_STL_REFINEMENT_HIGH_VALUE,
                            UI_STL_REFINEMENT_MEDIUM_VALUE,
                            UI_STL_REFINEMENT_LOW_VALUE]                                    # Elements of the dropdown list

# user interface - filename options
UI_FILENAME_OPTIONS_GROUP_ID = 'FilenameOptions'                                            # group id that contains the filename options UI elements
UI_FILENAME_OPTIONS_GROUP_NAME = 'Filename Options'                                         # name of the group that contains the filename options UI elements

UI_FILENAME_ADD_PROJECT_NAME_NAME = 'Add Project Name'                                      # True if the name of the project should be added to the export name otherwise False
UI_FILENAME_ADD_DESIGN_NAME_NAME = 'Add Design Name'                   	                    # True if the name of the design should be added to the export name otherwise False

UI_FILENAME_REMOVE_VERSION_TAGS_NAME = 'Remove Version Tags'                                # True if version tags should be removed otherwise False

UI_FILENAME_ELEMENT_SEPERATOR_NAME = 'Element Separator'                                    # character that separates e.g. project name, occurrence name and body name in an export name
UI_FILENAME_ELEMENT_SEPERATOR_VALUES = ['.', '-', '_']                                      # list of valid characters

UI_FILENAME_OCCURRENCE_ID_SEPERATOR_NAME = 'Occurrence ID Separator'                        # character that separates the occurrence name and the instance id
UI_FILENAME_OCCURRENCE_ID_SEPERATOR_VALUES = ['.', '-', '_']                                # list of valid characters

# configuration - common
CONF_DEFAULT_CONFIG_NAME = 'Defaults.json'                                                  # name of the configuration file that stores the default configuration
CONF_PROJECT_ATTRIBUTE_GROUP = 'ExportIt'                                                   # name of the attribute group that stores the project specific data
CONF_PROJECT_ATTRIBUTE_KEY = 'projectConfiguration'                                         # key of the key that contains the project specific configuration (delta to default configuration)
CONF_VERSION_KEY = 'version'                                                                # key of the element that contains the version of the default configuration
CONF_VERSION_DEFAULT = '0.1.0'                                                              # default version of the default configuration

# configuration - export directory
CONF_EXPORT_DIRECTORY_KEY = 'exportDirectory'                                               # key of the element that contains the export directory
CONF_EXPORT_DIRECTORY_DEFAULT = ''                                                          # value that's used to initialize the export directory

CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_KEY = 'addProjectNameToDirectory'                    # True if the name of the project should be added to the export directory otherwise False
CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_DEFAULT = True                                       # valid values for the default: True, False

CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_KEY = 'addDesignNameToDirectory'                      # True if the name of the design should be added to the export directory otherwise False
CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_DEFAULT = True                                        # valid values for the default: True, False

# configuration - stl options
CONF_STL_STRUCTURE_KEY = 'StlStructure'                                                     # name of the element that contains the stl refinement
CONF_STL_STRUCTURE_DEFAULT = [UI_STRUCTURE_ONE_FILE_VALUE]                                  # valid values 'One File', 'One File Per Body In Component, 'One File Per Body In Occurrence'

CONF_STL_REFINEMENT_KEY = 'StlRefinement'                                                   # name of the element that contains the stl refinement
CONF_STL_REFINEMENT_DEFAULT = [UI_STL_REFINEMENT_LOW_VALUE]                                 # valid values 'Low', 'Medium', 'Hight', 'Ultra'

# configuration - filename options
CONF_FILENAME_ADD_PROJECT_NAME_KEY = 'addProjectNameToFilename'                             # True if the name of the project should be added to the export name otherwise False
CONF_FILENAME_ADD_PROJECT_NAME_DEFAULT = False                                              # valid values for the default: True, False

CONF_FILENAME_ADD_DESIGN_NAME_KEY = 'addDesignNameToFilename'         	                    # True if the name of the design should be added to the export name otherwise False
CONF_FILENAME_ADD_DESIGN_NAME_DEFAULT = True                                                # valid values for the default: True, False

CONF_FILENAME_REMOVE_VERSION_TAGS_KEY = 'removeVersionTags'                                 # True if version tags should be removed otherwise False
CONF_FILENAME_REMOVE_VERSION_TAGS_DEFAULT = True                                            # valid values for the default: True, False

CONF_FILENAME_ELEMENT_SEPERATOR_KEY = 'elementSeparator'                                    # character that separates e.g. project name, occurrence name and body name in an export name
CONF_FILENAME_ELEMENT_SEPERATOR_DEFAULT = '.'                                               # valid values for the default: '.', '-', '_'

CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_KEY = 'occurrenceIdSeparator'                         # character that separates the occurrence name and the instance id
CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_DEFAULT = '_'                                         # valid values for the default: '.', '-', '_'

# internal structure of export objects
REC_OCCURRENCE_PATH = 'occurrencePath'                                                      # full path name of the occurrence
REC_BODIES = 'bodies'                                                                       # BREP Body
REC_OCCURRENCE = 'occurrence'                                                               # Occurrence
REC_IS_UNIQUE = 'isUnique'                                                                  # Marker if this record should be used, if all components (not occurrences) should be exported