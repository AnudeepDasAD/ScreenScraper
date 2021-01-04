from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import argparse
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import requests
from sentAnalysis import Analyze

def argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--searchItem', dest='searchItem', help='Enter search item')
    parser.add_argument('-c', '--useChannel', dest = 'useChannel', help='Enter "true" if searching for channel, otherwise "false"', action = 'store_true')
    return parser.parse_args()

#No longer being used
def navigateToVideos():
    #Go to the videos tab
    videos = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse[2]/div[3]/ytd-c4-tabbed-header-renderer/app-header-layout/div/app-header/div[2]/app-toolbar/div/div/paper-tabs/div/div/paper-tab[2]')
    videos.click()

def launchChannelSearch():
    channelXpath = '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-channel-renderer'
    actualChannel = driver.find_elements_by_xpath(channelXpath)
    if len(actualChannel) > 0:
        channelXpath +='/div/div[1]/a'
        #Clicking on the channel
        driver.find_element_by_xpath(channelXpath).click()
        time.sleep(2)
        #navigateToVideos()
    else:
        print('Could not find channel. Please enter a channel name or ensure you are using YouTube API level 3')

def getItems(numItems, xpath):
    listItems = driver.find_elements_by_xpath(xpath)
    listItems = listItems[:numItems]
    print(listItems)
    return listItems

#No longer being used
def infinityScroll():
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
    time.sleep(2)
    html.send_keys(Keys.HOME)
    #html.send_keys(Keys.DOWN)
    

def aggregateVideos(xpath, numItemsWanted):
    #gets a list of videos
    listVideos = getItems(numItemsWanted,xpath)
    for video in listVideos:
        video.click()
        time.sleep(2)
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #infinityScroll()
        #Gets a comment container and puts it in the list
        #commentElements = getItems(3, specificCommentXpath)
        print(driver.current_url)
        urls.append(driver.current_url)
        driver.execute_script('window.history.go(-1);')
        #parse the url
        time.sleep(2)

def expandPage(numScrolls):
    moreButton = driver.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-shelf-renderer/div[1]/div[2]/ytd-vertical-list-renderer/div[2]/yt-formatted-string')
    i = 1
    while len(moreButton) > 0 and i <= numScrolls:
        infinityScroll()
        moreButton = driver.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-shelf-renderer/div[1]/div[2]/ytd-vertical-list-renderer/div[2]/yt-formatted-string')
        i += 1

#set up
arguments = argument_parser()
#To get rid of some messages
chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument(r"user-data-directory=C:\Users\Anude\AppData\Local\Google\Chrome\User myChrome")

# r = binary raw switch
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# driver = webdriver.Chrome(executable_path=r'C:\Screen Scraper\chromedriver', options=chrome_options)
driver.get("https://www.youtube.com")

youTubeSearchBar = driver.find_element_by_name("search_query")
youTubeSearchButton = driver.find_element_by_id("search-icon-legacy")
youTubeSearchBar.send_keys(str(arguments.searchItem))
# youTubeSearchBar.send_keys('critical role')
youTubeSearchButton.click()
time.sleep(2)

urls = []

'''
if str(arguments.useChannel).lower() == 'true':
    launchChannelSearch()
    time.sleep(3)
    videoXpathAtChannelHome = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[1]/div[3]/ytd-shelf-renderer/div[1]/div[2]/yt-horizontal-list-renderer/div[2]/div/ytd-grid-video-renderer'
    videoXpathVideoTab = '/html/body/ytd-app/div/ytd-page-manager/ytd-browse[2]/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-grid-renderer/div[1]/ytd-grid-video-renderer'

    aggregateVideos(videoXpathAtChannelHome, 3)
    '''
#else:
    #Launching general video search
videoXpathSearchPage = '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-shelf-renderer[1]/div[1]/div[2]/ytd-vertical-list-renderer/div[1]/ytd-video-renderer'
time.sleep(2)
aggregateVideos(videoXpathSearchPage, 3)
time.sleep(2)

#aggregateVideos gets all of the video urls
videoIds = []
#Taking just the video id of the urls
apiKey = 'AIzaSyBwFlugiEhtnseyVC23eD-O91hNFL22X6E'
for url in urls:
    videoIds.append(url[32:])

#create the request urls to get the comments from the videos
req = []
for id in videoIds:
    req.append('https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&key='+apiKey+'&videoId='+id+'&maxResults=100')


#Perform the requests- get the comments into a list
def performRequest(req):
    comments = []
    for r in req:
        send = requests.get(url=r)
        res = send.json()
        for comment in res['items']:
            comments.append(comment['snippet']['topLevelComment']['snippet']['textOriginal'])
    return comments

#gets the comments, they are all put inside a list
comments = performRequest(req)
print(len(comments))

all_analyses_tblob = []
all_analyses_vader = []
for comment in comments:
    analysisTblob, analysisVader = Analyze(comment)
    all_analyses_tblob.append(analysisTblob)
    all_analyses_vader.append(analysisVader)

avgAnalysisTblob = sum(all_analyses_tblob)/len(all_analyses_tblob)
avgAnalysisVader = sum(all_analyses_vader)/len(all_analyses_vader)

print(f'Average analysis of Tblob: {avgAnalysisTblob}')
print(f'Average analysis of Vader: {avgAnalysisVader}')
driver.quit()
