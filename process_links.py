import os
import csv
import time

clinks = []
channel_list = "channels.csv"
with open(channel_list, 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    total_entries = 0
    for row in csv_reader:
        total_entries +=1
        if ( len(row) > 0 ):
            # print(row[0])
            link_parts = row[0].split('/')
            if ( len(link_parts) >= 4 and link_parts[2]=="www.youtube.com" ) :
                # print(row[0], end="")
                # print(" Valid Youtube link")
                checks = link_parts[3].split("?")
                if checks[0]=="user" or checks[0]=="channel" :
                    print("Its a Youtube channel")
                    if len(link_parts) < 5:
                        print("Not complete link")
                    elif len(link_parts) == 5:
                        ylink = str(row[0])+'/videos'
                        clinks.append(ylink)
                        # command = "python3 crawl_link.py "+ylink
                        # os.system(command)
                    elif len(link_parts) > 5 :
                        ylink = str(row[0])
                        clinks.append(ylink)
                        # command = "python3 crawl_link.py "+ylink
                        # os.system(command)
                    # time.sleep(1)


                elif checks[0] == 'watch':
                    print("Its a youtube video link")
                else :
                    print("This is something else")
            else :
                print(row[0], end=" ")
                print(str(total_entries)+"Invalid Youtube lInk")
        print(" ")
    print('Processed All Entries. '+ str(total_entries))

with open('all_links_gen', mode='w') as mycsv:
    csv_writer = csv.writer(mycsv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for i in range(len(clinks)):
        csv_writer.writerow([clinks[i]])
# print(len(clinks))
# link = "https://www.youtube.com/user/shahrzadraqs/videos"
# parts = link.split('/')
# print(parts)
# print( parts[3].split("?"))

# for i in range(1):
#     link = "https://www.youtube.com/channel/UC3vpdI7klzLSLNgqZEESZ4g/videos"
#     command = "python3 crawl_link.py "+link
#     os.system(command)
#     print("/////////All Links Done////////////")
#     time.sleep(1)
