import os
import urllib, urllib.request, json, datetime

from .BaseLogger import logger
from .ConfigurationHelper import getConfiguration
from .Statics import *
from commands import __version__ as addinVersion

githubRemoteVersion = ""                  # remote version id
githubTitle = ""                          # title of the version
githubDescription = ""                    # description of the version
githubDownloadUrl = ""                    # download URL for the new version

def getGithubReleaseInformation():
    global githubRemoteVersion
    global githubTitle
    global githubDescription
    global githubDownloadUrl

    return addinVersion, githubRemoteVersion, githubTitle, githubDescription, githubDownloadUrl

def jsonDateConverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

def writeToVersionCheckFile(lastCheck, lastCheckedFilename):
    with open(lastCheckedFilename, 'w') as jsonOutFile:
        json.dump(lastCheck, jsonOutFile, default = jsonDateConverter, indent=4)
        jsonOutFile.flush()
        jsonOutFile.close()

    logger.debug("last check file created / updated")

def lastUpdate():
    # initialize data
    lastCheck = {}
    currentDate = datetime.datetime.now()
    lastCheckDate = datetime.datetime.now()
    checkForUpdates = False

    # render path and filename
    lastCheckedFilename = os.path.dirname(os.path.abspath(__file__))
    lastCheckedFilename = os.path.join(lastCheckedFilename, 'config')
    lastCheckedFilename = os.path.join(lastCheckedFilename, VERSION_LAST_CHECKED_FILENAME)

    try:
        if not os.path.exists(lastCheckedFilename):
            lastCheck['date'] = currentDate
            writeToVersionCheckFile(lastCheck, lastCheckedFilename)

        else:
            with open(lastCheckedFilename) as jsonInFile:
                lastCheck = json.load(jsonInFile)

            logger.debug("last check file loaded")
            lastCheckDate = datetime.datetime.strptime(lastCheck.get('date'), '%Y-%m-%d %H:%M:%S.%f')

        delta = currentDate - lastCheckDate
        logger.debug("Last check was executed %s days ago.", delta.days)

        if delta.days >= getConfiguration(CONF_VERSION_CHECK_INTERVAL_IN_DAYS_KEY):
            logger.debug("New version check is overdue")

            checkForUpdates = True
            lastCheck['date'] = currentDate
            writeToVersionCheckFile(lastCheck, lastCheckedFilename)

    except:
        logger.error(traceback.format_exc())

    return checkForUpdates

def checkForUpdates():
    global githubRemoteVersion
    global githubTitle
    global githubDescription
    global githubDownloadUrl

    # check if check for update is needed
    if not lastUpdate():
        return False

    # check if the url is reachable
    try:
        # create request
        logger.debug("preparing request for %s", VERSION_API_URL)
        request = urllib.request.Request(VERSION_API_URL)

        # get response1
        logger.debug("executing request")
        response = urllib.request.urlopen(request)

        # read response
        logger.debug("reading response")
        rawData = response.read()
        encoding = response.info().get_content_charset('utf8')

        # pars json string
        logger.debug("parsing response")
        data = json.loads(rawData.decode(encoding))

        # extract relevant data
        githubRemoteVersion = data.get('tag_name')
        githubTitle = data.get('name')
        githubDescription = data.get('body')
        githubDownloadUrl = data.get('html_url')

        logger.debug('add-in version: %s', addinVersion)
        logger.debug('githubRemoteVersion: %s', githubRemoteVersion)
        logger.debug('githubTitle: %s', githubTitle)
        logger.debug('githubDescription: %s', githubDescription)
        logger.debug('githubDownloadUrl: %s', githubDownloadUrl)

        # compare local and remote versions
        if githubRemoteVersion and addinVersion == githubRemoteVersion:
            # no new version found
            logger.info('Add-in is up to date.')

            return False

        else:
            # new version found
            logger.info('Add-in version %s can be downloaded from %s', githubRemoteVersion, githubDownloadUrl)

            return True

    except urllib.error.HTTPError as error:
        logger.error('The server couldn\'t fulfill the request.{}'.format(error))

    except urllib.error.URLError as error:
        logger.error('Fail to reach a server.{}'.format(e.reason))

    except:
        logger.error(traceback.format_exc())

    return False

def showReleaseNotes(isCheckOverdue, ao):
    if isCheckOverdue:
        # inform user about new message
        addinVersion, githubRemoteVersion, githubTitle, githubDescription, githubDownloadUrl = getGithubReleaseInformation()
        ao.ui.messageBox("New version found:\n\nCurrent Version: " + addinVersion + "\n\nNew Version: " + githubRemoteVersion + " - " + githubTitle + "\n\n" + githubDescription)
