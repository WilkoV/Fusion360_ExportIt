import adsk.core, adsk.fusion, adsk.cam, traceback

from .BaseLogger import logger

# dict with inputCommands
tabs = {}
groups = {}

def addTab(inputs :adsk.core.CommandInputs, tabId, tabName, isActive):
    # tab group
    tabCmdInput = inputs.addTabCommandInput(tabId, tabName)

    if isActive:
        # activate tab in the UI
        tabCmdInput.activate()

    tabInputs = tabCmdInput.children

    # cache tab inputs
    tabs[tabId] = tabInputs

    logger.debug("tab %s added", tabId)
    logger.debug("isActive %s", isActive)

def addGroupToTab(tabId, groupId, groupName, isExpanded):
    tabInputs = tabs.get(tabId)
    addGroup(tabInputs, groupId, groupName, isExpanded)

def addGroup(inputs :adsk.core.CommandInputs, groupId, groupName, isExpanded):
    # create group
    groupCmdInput = inputs.addGroupCommandInput(groupId, groupName)

    # set groups behavior
    groupCmdInput.isExpanded = isExpanded
    groupCmdInput.isEnabledCheckBoxDisplayed = False
    groupInputs = groupCmdInput.children

    # cache group inputs
    groups[groupId] = groupInputs

    logger.debug("group %s added", groupId)

def addStringInputToGroup(groupId, stingInputId, label, initialValue, isEnabled):
    # get list of UI elements
    groupInputs = groups.get(groupId)

    # add UI element to list
    input = groupInputs.addStringValueInput(stingInputId, label, initialValue)
    input.isEnabled = isEnabled

    logger.debug("StringInput %s added to group %s", stingInputId, groupId)

def addIntergerInputSpinnerToGroup(groupId, integerInputId, label, minimal, maximal, spinStep, initialValue):
    # get list of UI elements
    groupInputs = groups.get(groupId)

    # add UI element to list
    groupInputs.addIntegerSpinnerCommandInput(integerInputId, label, minimal, maximal, spinStep, initialValue)

def addFloatInputSpinnerToGroup(groupId, floatInputId, label, unitType, minimal, maximal, spinStep, initialValue):
    # get list of UI elements
    groupInputs = groups.get(groupId)

    logger.warning("%s %f %f %f %f", floatInputId, minimal, maximal, spinStep, initialValue)
    # add UI element to list
    groupInputs.addFloatSpinnerCommandInput(floatInputId, label, unitType, minimal, maximal, spinStep, initialValue)

def addBoolInputToGroup(groupId, boolInputId, label, initialValue):
    # get list of UI elements
    groupInputs = groups.get(groupId)

    # add UI element to list
    groupInputs.addBoolValueInput(boolInputId, label, True, '', initialValue)

    logger.debug("StringInput %s added to group %s", boolInputId, groupId)

def addTextListDropDown(groupId, dropDownId, label, itemNames :list, selectedItemName):
    # get list of UI elements
    groupInputs = groups.get(groupId)

    # add UI element to list
    dropDownInput = groupInputs.addDropDownCommandInput(dropDownId, label, adsk.core.DropDownStyles.TextListDropDownStyle)
    dropDownItems = dropDownInput.listItems

    # check if drop down list has a selected entry
    isItemSelected = False

    # create drop down items
    for itemName in itemNames:
        dropDownItems.add(itemName, False)

    # select item
    selectDropDownItemByName(groupInputs, dropDownId, selectedItemName)

    logger.debug("TextListDropDown %s added to group %s", dropDownId, groupId)

def selectDropDownItemByName(inputs :adsk.core.CommandInputs, dropDownId, selectedItemName):
    # iterate over items in the drop down list
    for listItem in inputs.itemById(dropDownId).listItems:
        if listItem.name == selectedItemName:
            # match found
            logger.debug('%s -> %s is selected', dropDownId, listItem.name)

            # activate item
            listItem.isSelected = True

            # this list can only handle one active element, stop prossing
            return True

    # No match found
    logger.warning('No item selected for drop down list %s', dropDownId)

    return False

def getSelectedDropDownItem(inputs :adsk.core.CommandInputs, dropDownId):
    # get list of drop down entries
    listItems = inputs.itemById(dropDownId).listItems
    itemName = None

    # search the selected item
    for item in listItems:
        # check each entry if it's selected or not.
        if item.isSelected:
            itemName = item.name

            logger.debug('%s -> %s is selected', dropDownId, itemName)

            # Only one element can be selected so stop searching and return the result
            return itemName

    # no entry selected
    logger.debug("drop down %s has no selected elements", dropDownId)

    return itemName

def addCheckBoxDropDown(groupId, dropDownId, label, itemNames :list, selectedItemNames :list):
    # get list of UI elements
    groupInputs = groups.get(groupId)

    # create drop down element
    dropDownInput = groupInputs.addDropDownCommandInput(dropDownId, label, adsk.core.DropDownStyles.CheckBoxDropDownStyle)

    # create list elements
    dropDownItems = dropDownInput.listItems

    logger.debug("%s", itemNames)
    logger.debug("%s", selectedItemNames)

    # process each item in the items list
    for itemName in itemNames:
        dropDownItems.add(itemName, False)

    selectDropDownItemByNames(groupInputs, dropDownId, selectedItemNames, False)

def selectDropDownItemByNames(inputs :adsk.core.CommandInputs, dropDownId, selectedItemNames:list, clearOldSelection):
    itemSelected = False

    # iterate over items in the drop down list
    for listItem in inputs.itemById(dropDownId).listItems:
        if listItem.name in selectedItemNames:
            # match found
            logger.debug('%s -> %s is selected', dropDownId, listItem.name)

            # select item
            listItem.isSelected = True
            itemSelected = True

        elif clearOldSelection:
            listItem.isSelected = False

    if not itemSelected:
        logger.warning('No item selected for drop down list %s', dropDownId)

    return itemSelected

def getSelectedDropDownItems(inputs :adsk.core.CommandInputs, dropDownId):
    # get list of items
    listItems = inputs.itemById(dropDownId).listItems

    # get all selected items
    selectedItems = []
    for item in listItems:
        if item.isSelected:
            # copy selected item into result list
            itemName = item.name
            selectedItems.append(itemName)

            logger.debug('%s -> %s is selected', dropDownId, itemName)

    if len(selectedItems) == 0:
        logger.debug("drop down %s has no selected elements", dropDownId)

    # return result list
    return selectedItems

def addSelectionCommandToInputs(groupId, selectionId, label, selectionFilters :list):
    # get list of UI elements
    groupInputs = groups.get(groupId)

    # add command to list of inputs
    selectionCommand = groupInputs.addSelectionInput(selectionId, label, '')

    # set limit to limitless
    selectionCommand.setSelectionLimits(0)

    # add list of selection filters
    for selectionFilter in selectionFilters:
        selectionCommand.addSelectionFilter(selectionFilter)

def hideUiElement(inputs :adsk.core.CommandInputs, elementId):
    element = inputs.itemById(elementId)
    element.isVisible = False

def showUiElement(inputs :adsk.core.CommandInputs, elementId):
    element = inputs.itemById(elementId)
    element.isVisible = True

def setUiValue(inputs :adsk.core.CommandInputs, elementId, value):
    element = inputs.itemById(elementId)
    element.value = value