from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import sys
import download_video
from os import path
driver = webdriver.Firefox()

channel_link = sys.argv[1]

# driver.get("https://www.youtube.com/user/GameofThrones/videos")
driver.get(channel_link)
# channel_name = str(driver.find_elements_by_tag_name('title'))
channel_name = str(driver.title)
print("Channel Name = " +channel_name)

SCROLL_PAUSE_TIME = 0.3
# Get scroll height
js = "return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"

js2 = "window.scrollTo(0, Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight ) );"

last_height = driver.execute_script(js)
# print("last height = "+ str(last_height))

def checkspin():
    try :
        spinners = driver.find_elements_by_tag_name('paper-spinner')
    except StaleElementReferenceException:
        print("Error in finding elements")
    if ( len(spinners) > 0 ):
        try:
            # spinId = str(spinners[0].get_attribute('id'))
            # spinClass = str(spinners[0].get_attribute('class'))
            spinHidden = str(spinners[0].get_attribute('aria-hidden'))
        except:
            print("Error in finding the aria-hidden")
            spinHidden='Active'
            driver.refresh()
            time.sleep(2)
        # spinActive = spinners[0].get_attribute('active')
        if ( spinHidden == 'true' ):
            spin = "Hidden"
        else :
            spin = "Active"
    else :
        spin = "No Spinner Tag Present"
    return spin

while True:
    spinner = str(checkspin()).strip()
    if spinner == 'Hidden':
        # print("Scrolling Down")
        driver.execute_script(js2)
        time.sleep(SCROLL_PAUSE_TIME)
    # elif spinner == 'Active' :
        # print("Loading Content")
    elif spinner == 'No Spinner Tag Present' :
        print("No more videos")
        break
    newh = driver.execute_script(js)
    print ("New Height is = "+ str(newh))

time.sleep(1)
# assert "GameofThrones" in driver.title
# print(driver)
print("Page loaded")
elems = driver.find_elements_by_class_name("style-scope ytd-grid-video-renderer")
csvfile = "Video_Links/"+channel_name+".csv"

with open(csvfile, mode='w') as mycsv:
    csv_writer = csv.writer(mycsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Hello = "Hello There"
    # Name = "Ranjan"
    # csv_writer.writerow([Hello, Name])
    # csv_writer.writerow([Hello, Name])
    for i in range(len(elems)):
        try:
            links = elems[i].find_elements_by_tag_name('a')
            vlink = links[0].get_attribute('href')
            title = links[1].get_attribute('title')
            a = elems[i].find_element_by_id('metadata-line')
            b = a.find_elements_by_tag_name('span')
            views = b[0].get_attribute('innerHTML')
            vtime = b[1].get_attribute('innerHTML')
            localtime = time.asctime( time.localtime(time.time()) )
            csv_writer.writerow([channel_name, title, views, vtime, vlink, localtime ])
            download_video.download_video(vlink,channel_name)
        except:
            csv_writer.writerow([channel_name,"Could Not be Downloaded please try again" ])
            with open('download_error.csv', mode='a') as errorcsv:
                error_writer = csv.writer(errorcsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                localtime = time.asctime( time.localtime(time.time()) )
                error_writer.writerow([channel_name,"Could Not be Downloaded please try again", localtime ])
            print("Could Not be Downloaded please try again")
            break

print ("Total Links Found = "+ str(len(elems))+" at "+channel_name+" .CSV FILE CREATED")

time.sleep(1)
# print(len(vlinks))
driver.close()
