This folder Contains following folders :
  1. Audios - This is a temporary folder to save audio files
  2. Videos - This is a temporary folder to download Videos
  3. Logs - This folder contains 4 logs per day
  4. Video_Links - This folder contains Video links of youtube channels
  5. Crawler-Input - This folder contains csv files containing youtube channel's videos url

How to Crawl :
  1. run "python3 crawler.py <index1> <csv file>"
      <index1> = index of the channel in csv file from where it will start crawling
      <csv file> = csv file in Crawler-Input folder which contains links to youtube channels
  2. run "python3 crawl_link_Vdisplay.py <youtube channel url>"
      <youtube channel url> = url of youtube channel videos

Files :
  1. Requirements.txt - all dependencies and modules list
  2. process_links.py - processes urls in csv file and extracts vaild urls

run "gcloud auth login" - login with google account which has permission granted for google cloud bucket
