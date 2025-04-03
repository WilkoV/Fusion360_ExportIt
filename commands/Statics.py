import logging

# log settings
LOG_FORMAT = '%(levelname)-7s; %(funcName)-37s; %(lineno)3d; %(message)s'                   # Format of the log messages
LOG_LEVEL = logging.DEBUG                                                                   # Logging level

# user interface - common
UI_STRUCTURE_ONE_FILE_VALUE = 'One File'                                                    # Export as one file
UI_STRUCTURE_ONE_FILE_PER_BODY_IN_COMPONENT_VALUE = 'One File Per Body In Component'        # Export one file per body in unique component
UI_STRUCTURE_ONE_FILE_PER_BODY_IN_OCCURRENCE_VALUE = 'One File Per Body In Occurrence'      # Export one file per body in unique occurrence
UI_STRUCTURE_ONE_FILE_PER_COMPONENT_VALUE = 'One File Per Component'                        # Export one file per unique component
UI_STRUCTURE_ONE_FILE_PER_COMPONENT_VALUE_DEPRECATED = 'One File Component'                 # Deprecated
UI_STRUCTURE_ONE_FILE_PER_TOP_LEVEL_OCCURRENCE_VALUE = 'One File Per Top Level Occurrence'  # Export one file per top level (below root) occurrence
UI_STL_REFINEMENT_NAME = 'Refinement'                                                       # refinement (resolution / density) for stl exports
UI_STL_REFINEMENT_ULTRA_VALUE = 'Ultra'                                                     # refinement ultra
UI_STL_REFINEMENT_HIGH_VALUE = 'High'                                                       # refinement high
UI_STL_REFINEMENT_MEDIUM_VALUE = 'Medium'                                                   # refinement medium
UI_STL_REFINEMENT_LOW_VALUE = 'Low'                                                         # refinement low
UI_STL_REFINEMENT_CUSTOM_VALUE = 'Custom'                                                   # refinement custom
UI_3MF_REFINEMENT_NAME = '3mfRefinement'                                                    # 3mf refinement (resolution / density) for stl exports
UI_3MF_REFINEMENT_ULTRA_VALUE = 'Ultra'                                                     # 3mf refinement ultra
UI_3MF_REFINEMENT_HIGH_VALUE = 'High'                                                       # 3mf refinement high
UI_3MF_REFINEMENT_MEDIUM_VALUE = 'Medium'                                                   # 3mf refinement medium
UI_3MF_REFINEMENT_LOW_VALUE = 'Low'                                                         # 3mf refinement low
UI_3MF_REFINEMENT_CUSTOM_VALUE = 'Custom'                                                   # 3mf refinement custom
UI_SELECTION_FILTER_BODY_VALUE = 'SolidBodies'                                              # Filter name Solid Body
UI_EXPORT_TYPES_STL_VALUE = 'stl'                                                           # STL format
UI_EXPORT_TYPES_STEP_VALUE = 'step'                                                         # STEP format
UI_EXPORT_TYPES_F3D_VALUE = 'f3d'                                                           # F3D / Fusion Archive format
UI_EXPORT_TYPES_3MF_VALUE = '3mf'                                                           # 3MF format
UI_SHOW_SUMMARY_FOR_INFO_VALUE = 'Info'                                                     # Show info, warning and error messages
UI_SHOW_SUMMARY_FOR_WARNING_VALUE = 'Warning'                                               # Show warning and error messages
UI_SHOW_SUMMARY_FOR_ERROR_VALUE= 'Error'                                                    # Show error messages
UI_EXPORT_DIRECTORY_CONFIGURE_DEFAULT_VALUE = 'As Base Directory'                           # Configure export directory as base directory in the default configuration command
UI_EXPORT_DIRECTORY_CONFIGURE_NEW_DESIGN_VALUE = 'When Exporting A New Design'              # Configure export directory in the export design command on the first export
UI_EXPORT_DIRECTORY_CONFIGURE_ALWAYS_VALUE = 'For Each Export'                              # Configure export directory in the export design command on every export

# user interface - export
UI_EXPORT_TAB_ID = 'Export'
UI_EXPORT_TAB_NAME = 'Export'

# user interface - export options
UI_EXPORT_OPTIONS_GROUP_ID = 'ExportOptions'                                                # Group id that contains the export options UI elements
UI_EXPORT_OPTIONS_GROUP_NAME = 'Export Options'                                             # Name of the group that contains the export options UI elements

UI_EXPORT_OPTIONS_BODIES_SELECTION_ID = 'selectedBodiesAndOccurrencesId'                    # Id of the Occurrences selection command
UI_EXPORT_OPTIONS_BODIES_SELECTION_NAME = 'Export Bodies'                                   # Label for the occurrences selection command
UI_EXPORT_OPTIONS_BODIES_SELECTION_VALUES = [UI_SELECTION_FILTER_BODY_VALUE]                # List of applied filters
UI_EXPORT_OPTIONS_TYPE_NAME = 'Export Types'                                                # Name of the field that contains the export types
UI_EXPORT_OPTIONS_TYPE_VALUES = [UI_EXPORT_TYPES_STL_VALUE,
                                    UI_EXPORT_TYPES_3MF_VALUE,
                                    UI_EXPORT_TYPES_STEP_VALUE,
                                    UI_EXPORT_TYPES_F3D_VALUE]                              # Elements of the dropdown list
UI_EXPORT_OPTIONS_EXCLUDE_LINKS_NAME = 'Exclude Links'                                      # Name of the field that contains the option to exclude external links from the export
UI_EXPORT_OPTIONS_EXCLUDE_COMPONENTS_NAME = 'Exclude Components'                            # List of occurrences that should be excluded

# user interface - stl options
UI_STL_OPTIONS_GROUP_ID = 'StlOptions'                                                      # Group id that contains the stl options UI elements
UI_STL_OPTIONS_GROUP_NAME = 'STL Options'                                                   # Name of the group that contains the stl options UI elements

UI_STL_STRUCTURE_NAME = 'Structure'                                                         # Export bodies as one file, file per body etc.
UI_STL_STRUCTURE_VALUES = [UI_STRUCTURE_ONE_FILE_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_BODY_IN_COMPONENT_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_BODY_IN_OCCURRENCE_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_TOP_LEVEL_OCCURRENCE_VALUE]           # Elements of the dropdown list
UI_STL_REFINEMENT_VALUES = [UI_STL_REFINEMENT_ULTRA_VALUE,
                            UI_STL_REFINEMENT_HIGH_VALUE,
                            UI_STL_REFINEMENT_MEDIUM_VALUE,
                            UI_STL_REFINEMENT_LOW_VALUE, 
                            UI_STL_REFINEMENT_CUSTOM_VALUE]                                 # Elements of the dropdown list
UI_STL_SURFACE_DEVIATION_NAME = 'Surface Deviation'                                         # Element that contains the custom surface deviation
UI_STL_SURFACE_DEVIATION_MIN =  0.000640                                                    # Min value for the custom surface deviation
UI_STL_SURFACE_DEVIATION_MAX =  0.064031                                                    # Max value for the custom surface deviation
UI_STL_SURFACE_DEVIATION_STEP = 0.005000                                                    # Step size value for the custom surface deviation
UI_STL_NORMAL_DEVIATION_NAME = 'Normal Deviation'                                           # Element that contains the custom normal deviation
UI_STL_NORMAL_DEVIATION_MIN = 1.0                                                           # Min value for the custom normal deviation
UI_STL_NORMAL_DEVIATION_MAX = 41.0                                                          # Max value for the custom normal deviation
UI_STL_NORMAL_DEVIATION_STEP = 1.00                                                         # Step size value for the custom normal deviation
UI_STL_MAX_EDGE_LENGTH_NAME = 'Maximum Edge Length'                                         # Element that contains the custom max edge length
UI_STL_MAX_EDGE_LENGTH_MIN = 0.06403                                                        # Min value for the custom edge length
UI_STL_MAX_EDGE_LENGTH_MAX = 64.03124                                                       # Max value for the custom edge length
UI_STL_MAX_EDGE_LENGTH_STEP = 0.50                                                          # Step size value for the custom edge length
UI_STL_ASPECT_RATIO_NAME = 'Aspect Ratio'                                                   # Element that contains the custom aspect ratio
UI_STL_ASPECT_RATIO_MIN = 0.06403                                                           # Min value for the custom aspect ratio
UI_STL_ASPECT_RATIO_MAX = 64.03124                                                          # Max value for the custom aspect ratio
UI_STL_ASPECT_RATIO_STEP = 0.50                                                             # Step size value for the custom aspect ratio

# user interface - 3mf options
UI_3MF_OPTIONS_GROUP_ID = '3mfOptions'                                                      # Group id that contains the 3mf options UI elements
UI_3MF_OPTIONS_GROUP_NAME = '3MF Options'                                                   # Name of the group that contains the 3mf options UI elements

UI_3MF_STRUCTURE_NAME = 'Structure'                                                         # Export bodies as one file, file per body etc.
UI_3MF_STRUCTURE_VALUES = [UI_STRUCTURE_ONE_FILE_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_BODY_IN_COMPONENT_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_BODY_IN_OCCURRENCE_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_TOP_LEVEL_OCCURRENCE_VALUE]           # Elements of the dropdown list
UI_3MF_REFINEMENT_VALUES = [UI_3MF_REFINEMENT_ULTRA_VALUE,
                            UI_3MF_REFINEMENT_HIGH_VALUE,
                            UI_3MF_REFINEMENT_MEDIUM_VALUE,
                            UI_3MF_REFINEMENT_LOW_VALUE, 
                            UI_3MF_REFINEMENT_CUSTOM_VALUE]                                 # Elements of the dropdown list
UI_3MF_SURFACE_DEVIATION_NAME = 'Surface Deviation'                                         # Element that contains the custom surface deviation
UI_3MF_SURFACE_DEVIATION_MIN =  0.000640                                                    # Min value for the custom surface deviation
UI_3MF_SURFACE_DEVIATION_MAX =  0.064031                                                    # Max value for the custom surface deviation
UI_3MF_SURFACE_DEVIATION_STEP = 0.005000                                                    # Step size value for the custom surface deviation
UI_3MF_NORMAL_DEVIATION_NAME = 'Normal Deviation'                                           # Element that contains the custom normal deviation
UI_3MF_NORMAL_DEVIATION_MIN = 1.0                                                           # Min value for the custom normal deviation
UI_3MF_NORMAL_DEVIATION_MAX = 41.0                                                          # Max value for the custom normal deviation
UI_3MF_NORMAL_DEVIATION_STEP = 1.00                                                         # Step size value for the custom normal deviation
UI_3MF_MAX_EDGE_LENGTH_NAME = 'Maximum Edge Length'                                         # Element that contains the custom max edge length
UI_3MF_MAX_EDGE_LENGTH_MIN = 0.06403                                                        # Min value for the custom edge length
UI_3MF_MAX_EDGE_LENGTH_MAX = 64.03124                                                       # Max value for the custom edge length
UI_3MF_MAX_EDGE_LENGTH_STEP = 0.50                                                          # Step size value for the custom edge length
UI_3MF_ASPECT_RATIO_NAME = 'Aspect Ratio'                                                   # Element that contains the custom aspect ratio
UI_3MF_ASPECT_RATIO_MIN = 0.06403                                                           # Min value for the custom aspect ratio
UI_3MF_ASPECT_RATIO_MAX = 64.03124                                                          # Max value for the custom aspect ratio
UI_3MF_ASPECT_RATIO_STEP = 0.50                                                             # Step size value for the custom aspect ratio

# user interface - step options
UI_STEP_OPTIONS_GROUP_ID = 'StepOptions'                                                    # Group id that contains the step options UI elements
UI_STEP_OPTIONS_GROUP_NAME = 'STEP Options'                                                 # Name of the group that contains the step options UI elements

UI_STEP_STRUCTURE_NAME = 'Structure'                                                        # Export bodies as one file, file per body etc.
UI_STEP_STRUCTURE_VALUES = [UI_STRUCTURE_ONE_FILE_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_COMPONENT_VALUE]                      # Elements of the dropdown list

# user interface - f3d options
UI_F3D_OPTIONS_GROUP_ID = 'f3dOptions'                                                      # Group id that contains the f3d options UI elements
UI_F3D_OPTIONS_GROUP_NAME = 'F3D Options'                                                   # Name of the group that contains the f3d options UI elements

UI_F3D_STRUCTURE_NAME = 'Structure'                                                         # Export bodies as one file, file per body etc.
UI_F3D_STRUCTURE_VALUES = [UI_STRUCTURE_ONE_FILE_VALUE,
                            UI_STRUCTURE_ONE_FILE_PER_COMPONENT_VALUE]                      # Elements of the dropdown list

# user interface - location
UI_LOCATION_TAB_ID = 'Location'
UI_LOCATION_TAB_NAME = 'Location'

# user interface - export directory
UI_EXPORT_DIRECTORY_OPTIONS_GROUP_ID = 'ExportDirectoryOptions'                             # Group id that contains the export directory UI elements
UI_EXPORT_DIRECTORY_OPTIONS_GROUP_NAME = 'Export Directory Options'                         # Name of the group that contains the export directory UI elements

UI_EXPORT_DIRECTORY_CONFIGURE_NAME = 'Configure Export Directory'                           # Name of the element that contains the configuration of the export directory
UI_EXPORT_DIRECTORY_CONFIGURE_VALUES = [UI_EXPORT_DIRECTORY_CONFIGURE_DEFAULT_VALUE,
                                        UI_EXPORT_DIRECTORY_CONFIGURE_NEW_DESIGN_VALUE,
                                        UI_EXPORT_DIRECTORY_CONFIGURE_ALWAYS_VALUE]         # Elements of the dropdown list
UI_EXPORT_DIRECTORY_NAME = 'Export Directory'                                               # Base path for the export process
UI_EXPORT_DIRECTORY_RESET_ID = 'resetExportDirectory'                                       # Id of the check box that triggers the reset of the export directory
UI_EXPORT_DIRECTORY_RESET_NAME = 'Reset Export Directory'                                   # Name of the check box that triggers the reset of the export directory
UI_EXPORT_DIRECTORY_RESET_DEFAULT = False                                                   # True to trigger the reset of the export directory otherwise False
UI_EXPORT_DIRECTORY_ADD_PROJECT_NAME_NAME = 'Add Project Name'                              # True if the name of the project should be added to the export directory otherwise False
UI_EXPORT_DIRECTORY_ADD_DESIGN_NAME_NAME = 'Add Design Name'                                # True if the name of the design should be added to the export directory otherwise False
UI_EXPORT_DIRECTORY_ADD_DENSITY_NAME_NAME = 'Add Refinement Name'                           # Add density name to the export directory (stl only)
UI_EXPORT_DIRECTORY_EXPORT_TYPE_NAME = 'Add Export Type'                                    # True if the name of the export type should be added to the export directory otherwise False

# user interface - filename options
UI_FILENAME_OPTIONS_GROUP_ID = 'FilenameOptions'                                            # Group id that contains the filename options UI elements
UI_FILENAME_OPTIONS_GROUP_NAME = 'Filename Options'                                         # Name of the group that contains the filename options UI elements

UI_FILENAME_ADD_PROJECT_NAME_NAME = 'Add Project Name'                                      # True if the name of the project should be added to the export name otherwise False
UI_FILENAME_ADD_DESIGN_NAME_NAME = 'Add Design Name'                   	                    # True if the name of the design should be added to the export name otherwise False
UI_FILENAME_REMOVE_VERSION_TAGS_NAME = 'Remove Version Tags'                                # True if version tags should be removed otherwise False
UI_FILENAME_ELEMENT_SEPERATOR_NAME = 'Element Separator'                                    # Character that separates e.g. project name, occurrence name and body name in an export name
UI_FILENAME_ADD_CONFIGURATION_NAME = 'Add Configuration Name'                               # True if the name of the current configuration should be added to the export name otherwise False
UI_FILENAME_REMOVE_VERSION_TAGS_NAME = 'Remove Version Tags'                                # True if version tags should be removed otherwise False
UI_FILENAME_ELEMENT_SEPERATOR_NAME = 'Element Separator'                                    # Character that separates e.g. project name, occurrence name and body name in an export name
UI_FILENAME_ELEMENT_SEPERATOR_VALUES = ['.', '-', '_']                                      # List of valid characters
UI_FILENAME_OCCURRENCE_ID_SEPERATOR_NAME = 'Occurrence ID Separator'                        # Character that separates the occurrence name and the instance id
UI_FILENAME_OCCURRENCE_ID_SEPERATOR_VALUES = ['.', '-', '_']                                # List of valid characters
UI_FILENAME_REPLACE_SPACES_NAME = 'Replace Spaces'                                          # True if spaces should be replaced, otherwise False
UI_FILENAME_REPLACE_SPACES_WITH_NAME = 'Replace Spaces With'                                # Character that replaces spaces in the filename
UI_FILENAME_REPLACE_SPACES_WITH_VALUES = ['.', '-', '_']                                    # List of valid characters
UI_FILENAME_USE_PART_NUMBER_NAME = 'Replace Component Name With Part Number'                # True if the name of the project should be added to the export name otherwise False

# user interface - misc
UI_MISC_TAB_ID = 'Misc'
UI_MISC_TAB_NAME = 'Misc'

# user interface - common
UI_COMMON_GROUP_ID = 'Common'                                                               # Group id that contains common settings
UI_COMMON_GROUP_NAME = 'Common'                                                             # Name of the group that contains common settings

UI_SHOW_SUMMARY_FOR_NAME = 'Show Summary For'                                               # Show export summary for infos, warnings or errors
UI_SHOW_SUMMARY_FOR_VALUES = [UI_SHOW_SUMMARY_FOR_INFO_VALUE, 
                                UI_SHOW_SUMMARY_FOR_WARNING_VALUE,
                                UI_SHOW_SUMMARY_FOR_ERROR_VALUE]                            # Show warnings and errors

UI_AUTOSAVE_PROJECT_CONFIGURATION_NAME = 'Autos Save'                                       # Auto save project configuration
UI_AUTOSAVE_DESCRIPTION_NAME = 'Auto Save Message'                                          # Message for the auto save action
# user interface - version information
UI_VERSION_GROUP_ID = 'VersionInfo'                                                         # Group id that contains version information
UI_VERSION_GROUP_NAME = 'Version Info'                                                      # Name of the group that contains version information

UI_VERSION_CHECK_INTERVAL_NAME = 'Version Check Interval'                                   # Name of the field that contains the check interval
UI_VERSION_DOWNLOAD_URL_ID = 'downloadUrl'                                                  # Id of the field the contains the new version
UI_VERSION_DOWNLOAD_URL_NAME = 'Download URL'                                               # Name of the field that contains the new version

# configuration - common
CONF_DEFAULT_CONFIG_NAME = 'Defaults.json'                                                  # Name of the configuration file that stores the default configuration
CONF_PROJECT_ATTRIBUTE_GROUP = 'ExportIt'                                                   # Name of the attribute group that stores the project specific data
CONF_PROJECT_ATTRIBUTE_KEY = 'projectConfiguration'                                         # Key of the key that contains the project specific configuration (delta to default configuration)
CONF_VERSION_KEY = 'version'                                                                # Key of the element that contains the version of the default configuration
CONF_VERSION_DEFAULT = '1.3.0'                                                              # Default version of the default configuration

# configuration - export options
CONF_EXPORT_OPTIONS_TYPE_KEY = 'exportTypes'                                                # Name of the element that contains the export types
CONF_EXPORT_OPTIONS_TYPE_DEFAULT = [UI_EXPORT_TYPES_STL_VALUE, UI_EXPORT_TYPES_STEP_VALUE,
                                         UI_EXPORT_TYPES_3MF_VALUE]                         # Valid values STEP, STL
CONF_EXPORT_OPTIONS_EXCLUDE_LINKS_KEY = 'excludeExternalLinks'                              # Name of the element that contains the export types
CONF_EXPORT_OPTIONS_EXCLUDE_LINKS_DEFAULT = False                                           # True if external links should be exclude, otherwise False
CONF_EXPORT_OPTIONS_EXCLUDE_COMPONENTS_KEY = 'excludeComponents'                            # List of occurrences that should be excluded
CONF_EXPORT_OPTIONS_EXCLUDE_COMPONENTS_DEFAULT = []                                         # Checkbox type list of occurrences that should be excluded

# configuration - stl options
CONF_STL_STRUCTURE_KEY = 'StlStructure'                                                     # Name of the element that contains the stl structure
CONF_STL_STRUCTURE_DEFAULT = [UI_STRUCTURE_ONE_FILE_VALUE]                                  # Valid values 'One File', 'One File Per Body In Component, 'One File Per Body In Occurrence'
CONF_STL_REFINEMENT_KEY = 'StlRefinement'                                                   # Name of the element that contains the stl refinement
CONF_STL_REFINEMENT_DEFAULT = [UI_STL_REFINEMENT_LOW_VALUE]                                 # Valid values 'Low', 'Medium', 'Hight', 'Ultra'
CONF_STL_SURFACE_DEVIATION_KEY = 'stlSurfaceDeviation'                                      # Name of the element that contains the stl surface deviation for custom settings
CONF_STL_SURFACE_DEVIATION_DEFAULT = 0.00321                                                # Default for the custom surface deviation
CONF_STL_NORMAL_DEVIATION_KEY = 'stlNormalDeviation'                                        # Name of the element that contains the stl normal deviation for custom settings
CONF_STL_NORMAL_DEVIATION_DEFAULT = 10.00                                                   # Default for the custom normal deviation
CONF_STL_MAX_EDGE_LENGTH_KEY = 'stlMaxEdgeLength'                                           # Name of the element that contains the stl max edge length for custom settings
CONF_STL_MAX_EDGE_LENGTH_DEFAULT = 64.0312                                                  # Default for the custom max edge length
CONF_STL_ASPECT_RATIO_KEY = 'stlAspectRatio'                                                # Name of the element that contains the stl aspect ratio for custom settings
CONF_STL_ASPECT_RATIO_DEFAULT = 21.5000                                                     # Default for the custom aspect ratio

# configuration - 3mf options
CONF_3MF_STRUCTURE_KEY = '3mfStructure'                                                     # Name of the element that contains the 3mf structure
CONF_3MF_STRUCTURE_DEFAULT = [UI_STRUCTURE_ONE_FILE_VALUE]                                  # Valid values 'One File', 'One File Per Body In Component, 'One File Per Body In Occurrence'
CONF_3MF_REFINEMENT_KEY = '3mfRefinement'                                                   # Name of the element that contains the 3mf refinement
CONF_3MF_REFINEMENT_DEFAULT = [UI_3MF_REFINEMENT_LOW_VALUE]                                 # Valid values 'Low', 'Medium', 'Hight', 'Ultra'
CONF_3MF_SURFACE_DEVIATION_KEY = '3mfSurfaceDeviation'                                      # Name of the element that contains the 3mf surface deviation for custom settings
CONF_3MF_SURFACE_DEVIATION_DEFAULT = 0.00321                                                # Default for the custom surface deviation
CONF_3MF_NORMAL_DEVIATION_KEY = '3mfNormalDeviation'                                        # Name of the element that contains the 3mf normal deviation for custom settings
CONF_3MF_NORMAL_DEVIATION_DEFAULT = 10.00                                                   # Default for the custom normal deviation
CONF_3MF_MAX_EDGE_LENGTH_KEY = '3mfMaxEdgeLength'                                           # Name of the element that contains the 3mf max edge length for custom settings
CONF_3MF_MAX_EDGE_LENGTH_DEFAULT = 64.0312                                                  # Default for the custom max edge length
CONF_3MF_ASPECT_RATIO_KEY = '3mfAspectRatio'                                                # Name of the element that contains the 3mf aspect ratio for custom settings
CONF_3MF_ASPECT_RATIO_DEFAULT = 21.5000                                                     # Default for the custom aspect ratio

# configuration - step options
CONF_STEP_STRUCTURE_KEY = 'stepStructure'                                                   # Name of the element that contains the step structure
CONF_STEP_STRUCTURE_DEFAULT = [UI_STRUCTURE_ONE_FILE_VALUE]                                 # Valid values 'One File', 'One File Per Component

# configuration - f3d options
CONF_F3D_STRUCTURE_KEY = 'f3dStructure'                                                     # Name of the element that contains the f3d structure
CONF_F3D_STRUCTURE_DEFAULT = [UI_STRUCTURE_ONE_FILE_VALUE]                                  # Valid values 'One File', 'One File Per Component

# configuration - export directory
CONF_EXPORT_DIRECTORY_CONFIGURE_KEY = 'exportDirectoryConfiguration'                        # Key of the element that contains the kind of export directory
CONF_EXPORT_DIRECTORY_CONFIGURE_DEFAULT = UI_EXPORT_DIRECTORY_CONFIGURE_DEFAULT_VALUE       # Default value for the export directory configuration
CONF_EXPORT_DIRECTORY_KEY = 'exportDirectory'                                               # Key of the element that contains the export directory
CONF_EXPORT_DIRECTORY_DEFAULT = ''                                                          # Value that's used to initialize the export directory
CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_KEY = 'addProjectNameToDirectory'                    # True if the name of the project should be added to the export directory otherwise False
CONF_EXPORT_DIRECTORY_ADD_PROJECT_NAME_DEFAULT = False                                      # Valid values for the default: True, False
CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_KEY = 'addDesignNameToDirectory'                      # True if the name of the design should be added to the export directory otherwise False
CONF_EXPORT_DIRECTORY_ADD_DESIGN_NAME_DEFAULT = True                                        # Valid values for the default: True, False
CONF_EXPORT_DIRECTORY_ADD_DENSITY_NAME_KEY = 'addDensityTypeToDirectory'                    # Valid values for the default: True, False
CONF_EXPORT_DIRECTORY_ADD_DENSITY_NAME_DEFAULT = False                                      # True if the name of the density should be added to the export directory otherwise False
CONF_EXPORT_DIRECTORY_ADD_EXPORT_TYPE_KEY = 'addExportTypeToDirectory'                      # True if the name of the export type should be added to the export directory otherwise False
CONF_EXPORT_DIRECTORY_ADD_EXPORT_TYPE_DEFAULT = True                                        # Valid values for the default: True, False

# configuration - filename options
CONF_FILENAME_ADD_PROJECT_NAME_KEY = 'addProjectNameToFilename'                             # True if the name of the project should be added to the export name otherwise False
CONF_FILENAME_ADD_PROJECT_NAME_DEFAULT = False                                              # Valid values for the default: True, False
CONF_FILENAME_ADD_DESIGN_NAME_KEY = 'addDesignNameToFilename'         	                    # True if the name of the design should be added to the export name otherwise False
CONF_FILENAME_ADD_DESIGN_NAME_DEFAULT = True                                                # Valid values for the default: True, False
CONF_FILENAME_REMOVE_VERSION_TAGS_KEY = 'removeVersionTags'                                 # True if version tags should be removed otherwise False
CONF_FILENAME_REMOVE_VERSION_TAGS_DEFAULT = True                                            # Valid values for the default: True, False
CONF_FILENAME_ELEMENT_SEPERATOR_KEY = 'elementSeparator'                                    # Character that separates e.g. project name, occurrence name and body name in an export name
CONF_FILENAME_ELEMENT_SEPERATOR_DEFAULT = '.'                                               # Valid values for the default: '.', '-', '_'
CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_KEY = 'occurrenceIdSeparator'                         # Character that separates the occurrence name and the instance id
CONF_FILENAME_OCCURRENCE_ID_SEPERATOR_DEFAULT = '_'                                         # Valid values for the default: '.', '-', '_'
CONF_FILENAME_REPLACE_SPACES_KEY = 'replaceSpaces'                                          # True if spaces should be replaced, otherwise False
CONF_FILENAME_REPLACE_SPACES_DEFAULT = False                                                # Valid values are True or False
CONF_FILENAME_REPLACE_SPACES_WITH_KEY = 'replaceSpacesWith'                                 # Character that replaces spaces in the filename
CONF_FILENAME_REPLACE_SPACES_WITH_DEFAULT = '-'                                             # Valid values for the default: '.', '-', '_'
CONF_FILENAME_USE_PART_NUMBER_KEY = 'usePartNumber'                                         # Valid values for the default: True, False
CONF_FILENAME_USE_PART_NUMBER_DEFAULT = False                                               # Valid values for the default: True, False

CONF_FILENAME_ADD_CONFIGURATION_NAME_KEY = 'addConfigurationNameToFilename'                 # True if the name of the current configuration should be added to the export name otherwise False
CONF_FILENAME_ADD_CONFIGURATION_NAME_DEFAULT = False                                        # Valid values for the default: True, False

# configuration - common
CONF_SHOW_SUMMARY_FOR_KEY = 'showSummaryFor'                                                # Show export summary for infos, warnings or errors
CONF_SHOW_SUMMARY_FOR_DEFAULT = UI_SHOW_SUMMARY_FOR_WARNING_VALUE                           # Show warnings and errors
CONF_AUTOSAVE_PROJECT_CONFIGURATION_KEY = 'autoSaveProjectConfiguration'                    # Key that contains the auto save project configuration
CONF_AUTOSAVE_PROJECT_CONFIGURATION_DEFAULT = False                                         # True if project configurations should be saved automatically, otherwise False
CONF_AUTOSAVE_DESCRIPTION_KEY = 'autoSaveMessage'                                           # Key that contains the version description
CONF_AUTOSAVE_DESCRIPTION_DEFAULT = 'ExportIt configuration changed'                        # Description for the version 

# configuration - check for updates
CONF_VERSION_CHECK_INTERVAL_IN_DAYS_KEY = 'checkVersionFrequencyInDays'                     # Key that contains the frequency
CONF_VERSION_CHECK_INTERVAL_IN_DAYS_DEFAULT = 1                                             # Default value for the polling interval
CONF_VERSION_CHECK_INTERVAL_IN_DAYS_MIN = 1                                                 # Min value for the polling interval
CONF_VERSION_CHECK_INTERVAL_IN_DAYS_MAX = 30                                                # Max value for the polling interval

# internal structure of export objects
REC_OCCURRENCE_PATH = 'occurrencePath'                                                      # Full path name of the occurrence
REC_BODIES = 'bodies'                                                                       # BREP Body
REC_OCCURRENCE = 'occurrence'                                                               # Occurrence
REC_IS_UNIQUE = 'isUnique'                                                                  # Marker if this record should be used, if all components (not occurrences) should be exported
REC_IS_TOP_LEVEL = 'isTopLevel'                                                             # Marker if this record should be used, if only top level components should be exported
REC_IS_REFERENCED_COMPONENT = 'isReferencedComponent'                                       # True if this occurrence is referencing an external component otherwise false
REC_HAS_MESH_BODIES = 'hasMeshBodies'                                                       # True if the component has mesh bodies, otherwiser False
REC_PART_NUMBER = 'partNumber'                                                              # Part number of the component

# internal structure of summary
SUMMARY_INFOS = 'info'                                                                      # List of info messages
SUMMARY_WARNINGS = 'warnings'                                                               # List of warnings messages
SUMMARY_ERRORS = 'errors'                                                                   # List of error messages

# internal attributes version check
VERSION_LAST_CHECKED_FILENAME = "VersionCheck.json"                                         # Name of the file that contains the date of the last check.
VERSION_API_URL = 'https://api.github.com/repos/WilkoV/Fusion360_ExportIt/releases/latest'  # API ULR to get the latest release information
