import logging

# log settings
LOG_FORMAT = '%(levelname)-7s; %(funcName)-37s; %(lineno)3d; %(message)s'                   # format of the log messages
LOG_LEVEL = logging.DEBUG                                                                   # logging level

# user interface - common
UI_STRUCTURE_ONE_FILE_VALUE = 'One File'                                                    # Export as one file
UI_STRUCTURE_ONE_FILE_PER_BODY_IN_COMPONENT_VALUE = 'One File Per Body In Component'        # Export one file per body in unique component
UI_STRUCTURE_ONE_FILE_PER_BODY_IN_OCCURRENCE_VALUE = 'One File Per Body In Occurrence'      # Export one file per body in unique occurrence
UI_STRUCTURE_ONE_FILE_PER_COMPONENT_VALUE = 'One File Component'                            # Export one file per unique component
UI_STL_REFINEMENT_NAME = 'Refinement'                                                       # refinement (resolution / density) for stl exports
UI_STL_REFINEMENT_ULTRA_VALUE = 'Ultra'                                                     # refinement ultra
UI_STL_REFINEMENT_HIGH_VALUE = 'High'                                                       # refinement high
UI_STL_REFINEMENT_MEDIUM_VALUE = 'Medium'                                                   # refinement medium
UI_STL_REFINEMENT_LOW_VALUE = 'Low'                                                         # refinement low
UI_SELECTION_FILTER_BODY_VALUE = 'SolidBodies'                                              # Filter name Solid Body
UI_EXPORT_TYPES_STL_VALUE = 'stl'                                                           # STL format
UI_EXPORT_TYPES_STEP_VALUE = 'step'                                                         # STEP format
UI_EXPORT_TYPES_F3D_VALUE = 'f3d'                                                           # F3D / Fusion Archive format
UI_SHOW_SUMMARY_FOR_INFO_VALUE = 'Info'                                                     # Show info, warning and error messages
UI_SHOW_SUMMARY_FOR_WARNING_VALUE = 'Warning'                                               # Show warning and error messages
UI_SHOW_SUMMARY_FOR_ERROR_VALUE= 'Error'                                                    # Show error messages

# user interface - export
UI_EXPORT_TAB_ID = 'Export'
UI_EXPORT_TAB_NAME = 'Export'

# user interface - export options
UI_EXPORT_OPTIONS_GROUP_ID = 'ExportOptions'                                                # group id that contains the export options UI elements
UI_EXPORT_OPTIONS_GROUP_NAME = 'Export Options'                                             # name of the group that contains the export options UI elements

UI_EXPORT_OPTIONS_BODIES_SELECTION_ID = 'selectedBodiesAndOccurrencesId'                    # Id of the Occurrences selection command
UI_EXPORT_OPTIONS_BODIES_SELECTION_NAME = 'Export Bodies'                                   # Label for the occurrences selection command
UI_EXPORT_OPTIONS_BODIES_SELECTION_VALUES = [UI_SELECTION_FILTER_BODY_VALUE]                # List of applied filters
UI_EXPORT_OPTIONS_TYPE_NAME = 'Export Types'                                                # Name of the field that contains the export types
UI_EXPORT_OPTIONS_TYPE_VALUES = [UI_EXPORT_TYPES_STL_VALUE,
                                    UI_EXPORT_TYPES_STEP_VALUE,
                                    UI_EXPORT_TYPES_F3D_VALUE]                              # Elements of the dropdown list

# user interface - stl options
UI_STL_OPTIONS_GROUP_ID = 'StlOptions'                                                      # group id that contains the stl options UI elements
UI_STL_OPTIONS_GROUP_NAME = 'STL Options'                                                   # name of the group that contains the stl options UI elements

UI_STL_STRUCTURE_NAME = 'Structure'                                                         # Export bodies as one file, file per body etc.
UI_STL_STRUCTURE_VALUES = [UI_STRUCTURE_ONE_FILE_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_BODY_IN_COMPONENT_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_BODY_IN_OCCURRENCE_VALUE]             # Elements of the dropdown list
UI_STL_REFINEMENT_VALUES = [UI_STL_REFINEMENT_ULTRA_VALUE,
                            UI_STL_REFINEMENT_HIGH_VALUE,
                            UI_STL_REFINEMENT_MEDIUM_VALUE,
                            UI_STL_REFINEMENT_LOW_VALUE]                                    # Elements of the dropdown list

# user interface - step options
UI_STEP_OPTIONS_GROUP_ID = 'StepOptions'                                                    # group id that contains the step options UI elements
UI_STEP_OPTIONS_GROUP_NAME = 'STEP Options'                                                 # name of the group that contains the step options UI elements

UI_STEP_STRUCTURE_NAME = 'Structure'                                                        # Export bodies as one file, file per body etc.
UI_STEP_STRUCTURE_VALUES = [UI_STRUCTURE_ONE_FILE_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_COMPONENT_VALUE]                      # Elements of the dropdown list

# user interface - f3d options
UI_F3D_OPTIONS_GROUP_ID = 'f3dOptions'                                                      # group id that contains the f3d options UI elements
UI_F3D_OPTIONS_GROUP_NAME = 'F3D Options'                                                   # name of the group that contains the f3d options UI elements

UI_F3D_STRUCTURE_NAME = 'Structure'                                                         # Export bodies as one file, file per body etc.
UI_F3D_STRUCTURE_VALUES = [UI_STRUCTURE_ONE_FILE_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_COMPONENT_VALUE]                      # Elements of the dropdown list

# user interface - location
UI_LOCATION_TAB_ID = 'Location'
UI_LOCATION_TAB_NAME = 'Location'

# user interface - export directory
UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID = 'ExportDirectoryOptions'                             # group id that contains the export directory UI elements
UI_EXPORT_DIRECTORY_OPTIONS_GROUP_NAME = 'Export Directory Options'                         # name of the group that contains the export directory UI elements

UI_EXPORT_DIRECTORY_NAME = 'Export Directory'                                               # base path for the export process
UI_EXPORT_DIRECTORY_ADD_PROJECT_NAME_NAME = 'Add Project Name'                              # True if the name of the project should be added to the export directory otherwise False
UI_EXPORT_DIRECTORY_ADD_DESIGN_NAME_NAME = 'Add Design Name'                                # True if the name of the design should be added to the export directory otherwise False
UI_EXPORT_DIRECTORY_EXPORT_TYPE_NAME = 'Add Export Type'                                    # True if the name of the export type should be added to the export directory otherwise False

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

# user interface - misc
UI_MISC_TAB_ID = 'Misc'
UI_MISC_TAB_NAME = 'Misc'

# user interface - common
UI_COMMON_GROUP_ID = 'Common'                                                               # group id that contains common settings
UI_COMMON_GROUP_NAME = 'Common'                                                             # name of the group that contains common settings

UI_SHOW_SUMMARY_FOR_NAME = 'Show Summary For'                                               # Show export summary for infos, warnings or errors
UI_SHOW_SUMMARY_FOR_VALUES = [UI_SHOW_SUMMARY_FOR_INFO_VALUE, 
                                UI_SHOW_SUMMARY_FOR_WARNING_VALUE,
                                UI_SHOW_SUMMARY_FOR_ERROR_VALUE]                            # Show warnings and errors

UI_AUTOSAVE_PROJECT_CONFIGURATION_NAME = 'Autos Save'                                       # Auto save project configuration
UI_AUTOSAVE_DESCRIPTION_NAME = 'Auto Save Message'                                          # Message for the auto save action
# user interface - version information
UI_VERSION_GROUP_ID = 'VersionInfo'                                                         # group id that contains version information
UI_VERSION_GROUP_NAME = 'Version Info'                                                      # name of the group that contains version information

UI_VERSION_CHECK_INTERVAL_NAME = 'Version Check Interval'                                   # name of the field that contains the check interval
UI_VERSION_DOWNLOAD_URL_ID = 'downloadUrl'                                                  # id of the field the contains the new version
UI_VERSION_DOWNLOAD_URL_NAME = 'Download URL'                                               # name of the field that contains the new version

# configuration - common
CONF_DEFAULT_CONFIG_NAME = 'Defaults.json'                                                  # name of the configuration file that stores the default configuration
CONF_PROJECT_ATTRIBUTE_GROUP = 'ExportIt'                                                   # name of the attribute group that stores the project specific data
CONF_PROJECT_ATTRIBUTE_KEY = 'projectConfiguration'                                         # key of the key that contains the project specific configuration (delta to default configuration)
CONF_VERSION_KEY = 'version'                                                                # key of the element that contains the version of the default configuration
CONF_VERSION_DEFAULT = '0.4.0'                                                              # default version of the default configuration

# configuration - export options
CONF_EXPORT_OPTIONS_TYPE_KEY = 'exportTypes'                                                # name of the element that contains the stl refinement
CONF_EXPORT_OPTIONS_TYPE_DEFAULT = [UI_EXPORT_TYPES_STL_VALUE, UI_EXPORT_TYPES_STEP_VALUE]  # valid values STEP, STL

# configuration - stl options
CONF_STL_STRUCTURE_KEY = 'StlStructure'                                                     # name of the element that contains the stl refinement
CONF_STL_STRUCTURE_DEFAULT = [UI_STRUCTURE_ONE_FILE_VALUE]                                  # valid values 'One File', 'One File Per Body In Component, 'One File Per Body In Occurrence'
CONF_STL_REFINEMENT_KEY = 'StlRefinement'                                                   # name of the element that contains the stl refinement
CONF_STL_REFINEMENT_DEFAULT = [UI_STL_REFINEMENT_LOW_VALUE]                                 # valid values 'Low', 'Medium', 'Hight', 'Ultra'

# configuration - step options
CONF_STEP_STRUCTURE_KEY = 'stepStructure'                                                   # name of the element that contains the f3d structure
CONF_STEP_STRUCTURE_DEFAULT = [UI_STRUCTURE_ONE_FILE_VALUE]                                 # valid values 'One File', 'One File Per Component

# configuration - f3d options
CONF_F3D_STRUCTURE_KEY = 'f3dStructure'                                                     # name of the element that contains the f3d structure
CONF_F3D_STRUCTURE_DEFAULT = [UI_STRUCTURE_ONE_FILE_VALUE]                                  # valid values 'One File', 'One File Per Component

# configuration - export directory
CONF_EXPORT_DIRECTORY_KEY = 'exportDirectory'                                               # key of the element that contains the export directory
CONF_EXPORT_DIRECTORY_DEFAULT = ''                                                          # value that's used to initialize the export directory
CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_KEY = 'addProjectNameToDirectory'                    # True if the name of the project should be added to the export directory otherwise False
CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_DEFAULT = False                                      # valid values for the default: True, False
CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_KEY = 'addDesignNameToDirectory'                      # True if the name of the design should be added to the export directory otherwise False
CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_DEFAULT = True                                        # valid values for the default: True, False
CONF_EXPORT_DIRECTORY_ADD_EXPORT_TYPE_KEY = 'addExportTypeToDirectory'                      # True if the name of the export type should be added to the export directory otherwise False
CONF_EXPORT_DIRECTORY_ADD_EXPORT_TYPE_DEFAULT = True                                        # valid values for the default: True, False

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

# configuration - common
CONF_SHOW_SUMMARY_FOR_KEY = 'showSummaryFor'                                                # Show export summary for infos, warnings or errors
CONF_SHOW_SUMMARY_FOR_DEFAULT = UI_SHOW_SUMMARY_FOR_WARNING_VALUE                           # Show warnings and errors
CONF_AUTOSAVE_PROJECT_CONFIGURATION_KEY = 'autoSaveProjectConfiguration'                    # Key that contains the auto save project configuration
CONF_AUTOSAVE_PROJECT_CONFIGURATION_DEFAULT = False                                         # rue if project configurations should be saved automatically, otherwise False
CONF_AUTOSAVE_DESCRIPTION_KEY = 'autoSaveMessage'                                           # Key that contains the version description
CONF_AUTOSAVE_DESCRIPTION_DEFAULT = 'ExportIt configuration changed'                        # Description for the version 

# configuration - check for updates
CONF_VERSION_CHECK_INTERVAL_IN_DAYS_KEY = 'checkVersionFrequencyInDays'                     # key that contains the frequency
CONF_VERSION_CHECK_INTERVAL_IN_DAYS_DEFAULT = 1                                             # default value for the polling interval
CONF_VERSION_CHECK_INTERVAL_IN_DAYS_MIN = 1                                                 # min value for the polling interval
CONF_VERSION_CHECK_INTERVAL_IN_DAYS_MAX = 30                                                # max value for the polling interval

# internal structure of export objects
REC_OCCURRENCE_PATH = 'occurrencePath'                                                      # full path name of the occurrence
REC_BODIES = 'bodies'                                                                       # BREP Body
REC_OCCURRENCE = 'occurrence'                                                               # Occurrence
REC_IS_UNIQUE = 'isUnique'                                                                  # Marker if this record should be used, if all components (not occurrences) should be exported
REC_IS_REFERENCED_COMPONENT = 'isReferencedComponent'                                       # True if this occurrence is referencing an external component otherwise false

# internal structure of summary
SUMMARY_INFOS = 'info'                                                                      # list of info messages
SUMMARY_WARNINGS = 'warnings'                                                               # list of warnings messages
SUMMARY_ERRORS = 'errors'                                                                   # list of error messages

# internal attributes version check
VERSION_LAST_CHECKED_FILENAME = "VersionCheck.json"                                         # name of the file that contains the date of the last check.
VERSION_API_URL = 'https://api.github.com/repos/WilkoV/Fusion360_ExportIt/releases/latest'  # api ULR to get the latest release information
