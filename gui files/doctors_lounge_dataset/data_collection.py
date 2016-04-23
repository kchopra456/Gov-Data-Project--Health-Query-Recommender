import requests
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import threading
from doctors_lounge_dataset import crawl_topics

BeautifulSoup('html', "html.parser")

directory_path='C:/Gov Data Project/gui files/doctors_lounge_dataset'
progress=NONE
top_root=NONE
root=NONE
text_status=NONE
signal=True

crawl_flag=False
signal_complete=False
done_reference=NONE
def strcmp(str1,str2):
    if(str1==str2):
        return False
    else:
        return True
class index_data(threading.Thread):
    def __index__(self):
        threading.Thread.__init__(self)
    def run(self):
        global progress
        global root
        global top_root
        self.progress=progress
        self.root=root
        self.top_root=top_root
        self.progress.start()
        self.main_root=root
        self.top_root=top_root

        self.progress=progress
        index_heads_begin=index_heads()
        index_heads_begin.start()
        #self.progress.stop()


class index_heads(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global url
        global signal
        source_code=requests.get(url)
        text_source=source_code.text
        soup_obj=BeautifulSoup(text_source)
        #print(soup_obj)
        print('link formed')
        text_status.set('link formation complete, beginning Main Topics parsing...')

        for links in soup_obj.findAll('dt'):
                if signal:
                    #dt_soup=BeautifulSoup(links.text)
                    #print(links)
                    for head_topics in links.findAll('div',{"class":"list-inner"}):
                        #print(head_topics)
                        if head_topics.string is not None and signal:
                            #print("MAIN HEAD")
                            #print(head_topics.string)
                            data_file.write('MAIN HEAD\n')
                            data_file.write(str(head_topics.string))
                            text_status.set('Head topic query url retrieval-'+head_topics.string)
                            head_topics_url='http://www.doctorslounge.com/forums'+str(head_topics.findNext('a')).split('<a href=".')[1].split('">')[0]
                            data_file.write('\n')
                            data_file.write(head_topics_url)
                            data_file.write('\n')
                        for main_heads in links.findAll('a',{'class':'forumtitle'}):
                            if signal:
                                #print(main_heads.string)
                                data_file.write(str(main_heads.string))
                                data_file.write('\n')
                                text_status.set('Sub topic query url retrieval-'+main_heads.string)
                                #print(main_heads)
                                sub_heads_url='http://www.doctorslounge.com/forums'+str(main_heads).split('<a class="forumtitle" href=".')[1].split('">')[0]
                                data_file.write(sub_heads_url)
                                data_file.write('\n')
                    #print()
        #return
        #exit(1)
        if signal:
            #progress.stop()
            print('here')
            global crawl_flag
            crawl_flag=True
            crawl_topics.crawl_complete_flag=False
            crawl_topics.main(text_status,done_reference,progress)
            exit(1)
            #if crawl_topics.signal:
            #messagebox.askokcancel(parent=top_root,title='Proceed to crawl',message='The package has made connection with the server, do you want to proceed to crawl?')
            '''if (proceed)==True:
                crawl_topics.main()
            else:
                global progress
                progress.stop()
            '''

url='http://www.doctorslounge.com/forums/index.php'

def done_display():
        print('done')
        top_root.state('withdrawn')
        root.state('normal')
        global signal_complete
        signal_complete=True


def close_display():
    global signal_complete
    global crawl_flag
    if not signal_complete:

            print('close')
            choice=messagebox.askokcancel(title='Crawler Interrupt',message='This will disconnect current query retrieval, query database will may not be complete! .')
            print(choice)
            if choice:
                global signal
                signal=False
               # global crawl_flag
                if crawl_flag:
                    crawl_topics.signal=False
                top_root.state('withdrawn')
                root.state('normal')
                if not crawl_topics.crawl_complete_flag:
                    messagebox.showinfo(title='Corrupt Database',message='You just interrupted the Dataset creation. We recomend not to use this dataset, this package may not work properly.')
                #crawl_topics.signal=True
                crawl_flag=True
                #signal=True
    else:
        top_root.state('withdrawn')
        root.state('normal')
        messagebox.showinfo(title='Crawling Complete!',message='Crawling is complete, now you may use this dataset to create a new database!')
        signal_complete=False
def main(root_window,rootwindow):
    global data_file
    data_file=open(directory_path+"/data_file.txt",'w')
    print(directory_path)
    top_root_window=Toplevel(root_window)
    top_root_window.geometry('+400+400')
    top_root_window.resizable(False,False)
    top_root_window.overrideredirect(True)
    top_root_window.title('Medical Query Dataset')
    progressbar=ttk.Progressbar(top_root_window,length=370,orient=HORIZONTAL,mode='indeterminate')
    progressbar.grid(row=0,column=0,padx=5,pady=5,columnspan=4)
    rootwindow.state('withdrawn')
    global progress
    progress=progressbar
    global top_root
    top_root=top_root_window
    global root
    root=rootwindow
    done_button=ttk.Button(top_root,text='Complete!',command=done_display)
    done_button.grid(row=1,column=1,pady=30)
    done_button.state(['disabled'])
    global done_reference
    done_reference=done_button
    close_button=ttk.Button(top_root,text='Cancel',command=close_display)
    close_button.grid(row=1,column=2,pady=30)
    status_text=StringVar()
    status_text.set('requesting a connection with server...')
    status_label=Label(top_root_window,textvariable=status_text,wraplength=320)
    status_label.grid(row=2,column=0,columnspan=3,sticky='sw')
    begin_indexing=index_data()
    global text_status
    text_status=status_text
    begin_indexing.start()
if __name__ == '__main__':main()
