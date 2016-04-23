#from py2neo import Node,Graph,Relationship,authenticate
import requests
from bs4 import BeautifulSoup
#graph=Graph()
#authenticate("localhost:7474","neo4j","ultimate")
#data_file=open("data_file.txt",'r')
from tkinter import NONE
from tkinter import ttk
directory_path=None
signal=True
status_text=None
done_button=NONE
progress_bar=NONE
crawl_complete_flag=False
def strcmp(str1,str2):
    if(str1==str2):
        return True
    else:
        return False
def make_graph(data_file):
    label=data_file.readline()
    label=label.strip()
    temp=''
    last_Main_Head=''
    last_Main_Head_Ref=''
    while (label!= temp):
        if signal:
            if (strcmp(label,"MAIN HEAD")):
                print(label)
                query_file.write(label+'\n')
                label=data_file.readline()
                label=label.strip()
                print(label)
                status_text.set('beginning depth in search for-'+label)
                query_file.write(label+'\n')
                last_Main_Head=label
                label_url=data_file.readline().strip()
                print(label_url.replace('&amp','&'))
                query_file.write(label_url.replace('&amp','&')+'\n')
               # last_Main_Head_Ref=Node("Main_Head",name=label,url=label_url)
                #graph.create(last_Main_Head_Ref)
                temp=label
                #del_file.write(label)
                label=data_file.readline()
                label=label.strip()
            else:
                if(not strcmp(label,last_Main_Head)) and signal:
                    #print(label)
                    #label=data_file.readline()
                    print("SUB HEAD")
                    query_file.write('SUB HEAD\n')
                    print(label)
                    status_text.set('parsing for queries-'+label)
                    query_file.write(label+'\n')
                    print(label_url.replace('&amp','&'))
                    query_file.write(label_url.replace('&amp','&')+'\n')
                    label_url=data_file.readline().strip()
                    print(label_url.replace('&amp','&'))
                    #Sub_Head_Ref=Node("Sub_Head",name=label,url=Sub_Head_url)
                    #graph.create_unique(Relationship(last_Main_Head_Ref,'PARENT_TO',Sub_Head_Ref))
                    try:
                        get_query(label_url,1)
                    except Exception:
                        print('All data has been read!')
                        print('Even maybe your data connection was interrupted, check the file to make sure.')
                        status_text.set('Crawler was signaled for completion, make sure your connection was not broken.')
                        done_button.state(['!disabled'])
                        global progress_bar
                        progress_bar.stop()
                        global crawl_complete_flag
                        crawl_complete_flag=True
                        #exit(0)
                    temp=label
                    label=data_file.readline()
                    label=label.strip()
                    #del_file.write(str(label))
        else:return

def get_query(url,page_check):
    source_code=requests.get(url)
    source_text=source_code.text
    source_soup=BeautifulSoup(source_text)
    print(url)
    for links in source_soup.findAll('a',{'class':'topictitle'}):
        if signal:
            query_file.write(links.string+'\n')
            print(links.string)
            query_file.write('http://www.doctorslounge.com/forums'+str(links).split('href=".')[1].split(';sid=')[0].replace('&amp','&').replace(';','')+'\n')
            print('http://www.doctorslounge.com/forums'+str(links).split('href=".')[1].split(';sid=')[0].replace('&amp','&').replace(';',''))
            #query_ref=Node("Query",name=links.string)
            #query_url='http://www.doctorslounge.com/forums'+str(links).split('<a href=".')[1].split('amp;')[0]+str(links).split('<a href="./viewtopic.php?f=98&amp;')[1].split('" class="topictitle"')[0]
            #print(query_url)
            #----------------------------------------------------------
            #for gender in source_soup.findAll('dd',{'class':"profile-custom-field profile-sex"}):
             #   print(gender.string)
            #-----------------------------------------------------------
        else:return
    for topic_count in source_soup.findAll('a',{"role":["button","separator"]}):
        #print(topic_count)
        #print(topic_count.string)

        if signal:
            if strcmp(topic_count.string,'Next') or topic_count.string is None:
                #DO Nothin now
                nothing=0
            else:
                if int(topic_count.string)>= page_check+1 or strcmp(topic_count.string,'...'):
                    page_url='http://www.doctorslounge.com/forums'+str(topic_count).split('<a href=".')[1].split('amp;')[0]+('start=')+str(page_check*100)
                    page_check+=1
                    #print(page_url)

                    get_query_page(page_url)
            #topic_count_final=int(topic_count.string.split('"pagination">')[1].split(' topics<ul>')[0])
            #print(topic_count_final)
        else:return
def get_query_page(url):
    source_code=requests.get(url)
    source_text=source_code.text
    source_soup=BeautifulSoup(source_text)
    for links in source_soup.findAll('a',{'class':'topictitle'}):
        if signal:
            query_file.write(links.string+'\n')
            print(links.string)
            query_file.write('http://www.doctorslounge.com/forums'+str(links).split('href=".')[1].split(';sid=')[0].replace('&amp','&').replace(';','')+'\n')
            print('http://www.doctorslounge.com/forums'+str(links).split('href=".')[1].split(';sid=')[0].replace('&amp','&').replace(';',''))

            #query_file.write(links.string)
            #query_file.write('\n')
            #query_url='http://www.doctorslounge.com/forums'+str(links).split('<a href=".')[1].split('amp;')[0]+str(links).split('<a href="./viewtopic.php?f=98&amp;')[1].split('"')[0]
            #print(query_url)
        else:return
def main(text_status,done_reference,progress_status):
    global status_text
    status_text=text_status
    global done_button
    done_button=done_reference
    global query_file
    query_file=open(directory_path.replace('\\','/')+"/query_file.txt",'w')
    global progress_bar
    progress_bar=progress_status
    global data_file
    data_file=open(directory_path.replace('\\','/')+"/data_file.txt",'r')
    make_graph(data_file)
#main()
if __name__=='__main__':main()