import requests
from urllib import request
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import threading
from data_gov import csv_converter
from data_gov import parse_hmisv0
main_url='https://data.gov.in'
catalog_url=main_url+'/catalogs'
directory_save=NONE
'''try:
    catalog_source_code=requests.get(catalog_url)
    catalog_source_text=catalog_source_code.text
    catalog_soup=BeautifulSoup(catalog_source_text)
except Exception:
    messagebox.showinfo(title='Internet Connectivity',message='Please check your internet connectivity, no connection found')
    exit()'''
file_download_count=0
flag_kill=False
resume_value=0
neo4j_username=None
neo4j_password=None

kill_begin_count=0
def display_network_error():
    messagebox.showerror(title='Network Disconnection',message='Network disconnection found, please manually clear previous location and start crawl again.')
def file_gather(hmis_page_url,page_no,head_data_file_temp,task_field,task_tree):
    if not flag_kill:
        another_page_availabale=True
        region_name_list=[]
        #print(hmis_page_url)
        state_name=hmis_page_url.split('indicators-')[1].split('\n')[0]
        state_name=state_name.replace('-','_')
        #print(state_name)
        task_tree.config(state='normal')
        task_tree.delete(1.0,END)
        task_tree.config(state='disabled')
        head_data_file_temp.write("STATE\n")
        head_data_file_temp.write(state_name)
        task_field.config(state='normal')
        task_field.replace(1.0,END,'State is being parsed--'+state_name+'\n')
        task_field.config(state='disabled')
        head_data_file_temp.write('\n')
        head_data_file_temp.write("FILE NAME START HERE")
        head_data_file_temp.write('\n')
        region_count=1.0
        #File retreival=================
        while another_page_availabale and not flag_kill:
            another_page_availabale_flag=False
            try:
                hmis_page_source_code=requests.get(hmis_page_url)
            except Exception:
                display_network_error()
            hmis_page_source_text=hmis_page_source_code.text
            hmis_page_soup=BeautifulSoup(hmis_page_source_text)
            for links in hmis_page_soup.findAll('a',{'class':'ext data-extension csv'}):
                if not flag_kill:
                    print(links)
                    file_download_url=str(links).split('" href="')[1].split('">csv</a>')[0]
                    try:
                        file_download_response=request.urlopen(file_download_url)
                    except Exception:
                        display_network_error()
                    file_download_read=file_download_response.read()
                    file_download=str(file_download_read)
                    file_download_formated=file_download#.split('\\n')
                    global file_download_count

                    region_name=str(links).split('report')[1].split(state_name.replace('_','-'))[0]
                    if(region_name=='-'):
                        region_name+=state_name+'_cumulative_data_'
                    print(region_name)
                    try:
                        if(str(region_name).split('/')[1].split('">csv')[0] =="download"):
                            region_name=region_name.split('-20')[0]+'-'
                    except Exception:
                        task='DO Nothing'
                    region_name=str(region_name).replace('-','_')
                    region_name=region_name[1:-1]

                    print(region_name)
                    if region_name not in region_name_list:
                        file_download_count+=1
                        download_file_name=directory_save+'/file_'+str(file_download_count)+'.csv'
                        file_formation=open(download_file_name,'w')
                        task_field.config(state='normal')
                        task_field.replace(1.0,END,'Region is located for the state--'+state_name+'\n ')
                        task_field.config(state='disabled')
                        head_data_file_temp.write(region_name+'\n')
                        task_tree.config(state='normal')
                        task_tree.insert(region_count,region_name+'\n')
                        task_tree.config(state='disabled')
                        region_count+=1
                        region_name_list+=[region_name]
                        head_data_file_temp.write('file_'+str(file_download_count)+'.csv')
                        head_data_file_temp.write('\n')
                        file_download_soup=BeautifulSoup(file_download_formated)
                        #for lines in file_download_formated:
                         #   file_formation.write(lines+'\n')
                        for links in file_download_soup.findAll('meta',{'http-equiv':"refresh"}):
                            if not flag_kill:
                                #print(lines)
                                actual_file_download_url=str(links).split(';url=')[1].split('" http-equiv')[0]
                                #print(actual_file_download_url)
                                try:
                                    actual_file_download_response=request.urlopen(actual_file_download_url)
                                except Exception:
                                    continue
                                actual_file_download_read=actual_file_download_response.read()
                                actual_file_download=str(actual_file_download_read)
                                actual_file_download_formated=actual_file_download.split('\\n')
                                for lines in actual_file_download_formated:
                                    file_formation.write(lines +'\n')

                        #file_formation.close()
            page_no+=1
            for links in hmis_page_soup.findAll('a',{'title':'Go to page '+str(page_no)}):
                if not flag_kill:
                    ##print("Another page present---"+str(page_no))
                    ##print(links)
                    another_page_availabale_flag=True
                    hmis_page_url='https://data.gov.in'+str(links).split('<a href="')[1].split('" title=')[0].replace('amp;','')+'#web_catalog_tabs_block_10'
                    ##print(hmis_page_url)
            if not another_page_availabale_flag and not flag_kill:
                another_page_availabale=False

        head_data_file_temp.write("FILE NAME END HERE")
        head_data_file_temp.write('\n')



class hmis_data_crawler(threading.Thread):
    def __init__(self,progress,task_field,task_tree,crawl_button,kill_button):
        threading.Thread.__init__(self)
        self.task_field=task_field
        self.task_tree=task_tree
        self.progress=progress
        self.crawl_button=crawl_button
        self.kill_button=kill_button
        print('thread')
    def run(self):
        self.progress.start()
        global resume_value
        self.task_field.config(state='normal')
        self.task_field.replace(1.0,END,'Establishing connection with the server...')
        self.task_field.config(state='disabled')
        try:
            resume_file=open(directory_save+'/resume_info','r')
            resume_value=getint(resume_file.readline().strip())
            file_download_count=getint(resume_file.readline().strip())
            resume_file.close()

        except Exception:
            task=None
        hmis_url_list=['https://data.gov.in/catalogs/group_name/health-management-information-system-27343?query=&sort_by=created&sort_order=DESC&items_per_page=5&page=0','https://data.gov.in/catalogs/group_name/health-management-information-system-27343?query=&sort_by=created&sort_order=DESC&items_per_page=5&page=1',
                       'https://data.gov.in/catalogs/group_name/health-management-information-system-27343?query=&sort_by=created&sort_order=DESC&items_per_page=5&page=2','https://data.gov.in/catalogs/group_name/health-management-information-system-27343?query=&sort_by=created&sort_order=DESC&items_per_page=5&page=3',
                       'https://data.gov.in/catalogs/group_name/health-management-information-system-27343?query=&sort_by=created&sort_order=DESC&items_per_page=5&page=4','https://data.gov.in/catalogs/group_name/health-management-information-system-27343?query=&sort_by=created&sort_order=DESC&items_per_page=5&page=5',
                       'https://data.gov.in/catalogs/group_name/health-management-information-system-27343?query=&sort_by=created&sort_order=DESC&items_per_page=5&page=6']


        if resume_value>0:
            #print('here')
            #resume_choice=messagebox.askyesno(title='Resume Crawler',message='Some files from the previous download may be available, if you have not manually deleted the directory; we can resume from the previous progress!')
            #if resume_choice:
            self.task_field.config(state='normal')
            self.task_field.replace(1.0,END,'Resume location found...')
            self.task_field.config(state='disabled')
            print(hmis_url_list[resume_value:])
            hmis_url_list=hmis_url_list[resume_value:]
        for url in hmis_url_list:
                head_data_file_temp=open(directory_save+'/head_data_file_temp.txt','w')
                global  flag_kill
                if not flag_kill:
                    #print('working')
                    hmis_url=url
                    #for links in catalog_soup.findAll('a'):
                        #if links.string=='Health Management Information System':
                         #   hmis_url=str(links)
                        #print(links)
                    hmis_source_code=None
                    try:

                        hmis_source_code=requests.get(url)

                        #print(hmis_source_code)
                    except Exception:
                        display_network_error()
                    hmis_source_text=hmis_source_code.text
                    #print('here')
                    #print(hmis_source_text)
                    hmis_soup=BeautifulSoup(hmis_source_text)
                    list_go=[]
                    for links in hmis_soup.findAll('div'):
                        if not flag_kill:
                            #print(links)

                            for go in links.findAll('span',{'class':"field-content ogpl-capitalize"}):
                                if go in list_go:
                                    continue
                                else:
                                    list_go+=[go]
                                    print(list_go)
                                    print(go)
                                    #print(str(links).split('<a href="/catalog/')[1].split("-indicators")[0])
                                    if(str(links).split('<a href="/catalog/')[1].split("-indicators")[0]=='hmis-district-level-item-wise-and-month-wise-comparison-various'):
                                        file_url='https://data.gov.in'+str(go).split('<a href="')[1].split('">')[0]
                                        #print(file_url)
                                        file_gather(file_url,1,head_data_file_temp,self.task_field,self.task_tree)
                head_data_file_temp.close()
                head_data_file_temp=open(directory_save+'/head_data_file_temp.txt','r')
                if not flag_kill:
                    resume_value+=1
                    resume_file_save=open(directory_save+'/resume_info','w')
                    resume_file_save.write(str(resume_value)+'\n')
                    resume_file_save.write(str(file_download_count))
                    resume_file_save.close()
                    print (resume_value)
                    head_data_file=open(directory_save+'/Head_data_file.txt','a')
                    self.task_field.config(state='normal')
                    self.task_field.replace(1.0,END,'Saving the current crawl status...')
                    self.task_field.config(state='disabled')
                    text=head_data_file_temp.readline().strip()
                    while text!='':
                        head_data_file.write(text)
                        head_data_file.write('\n')
                        text=head_data_file_temp.readline().strip()
                    global file_download_count
                    global kill_begin_count
                    kill_begin_count=file_download_count
                    #link_title=links.title
                    #print(links)
        self.progress.stop()
        if not flag_kill:
            self.task_field.config(state='normal')
            self.task_field.replace(1.0,END,'Update successfull, wait for file conversion!')
            self.task_field.config(state='disabled')
            csv_converter.directory_path=directory_save
            csv_converter.file_download_count=file_download_count
            csv_converter.main(self.task_field,self.task_tree,self.progress)
            parse_hmisv0.repositroy_url=directory_save
            parse_hmisv0.file_download_count=file_download_count
            parse_hmisv0.main(self.task_field,self.task_tree,self.progress)
            self.task_tree.config(state='normal')
            self.task_field.config(state='normal')
            self.task_field.replace(1.0,END,'Package has completed updating database!')
            self.task_tree.replace(1.0,END,'All the steps for updating have reported success status, package should work perfectly with the updated database!')
            self.task_tree.config(state='disabled')
            self.task_field.config(state='disabled')
            self.crawl_button.state(['!disabled'])
            self.kill_button.state(['disabled'])
#hmis_data_crawler(catalog_soup)
#################################################DIRECTORY LOCATION#####################################
def get_directory_path(destination_entry,crawl_button):
    directory_path=filedialog.askdirectory()
    global directory_save
    directory_save=directory_path
    print(directory_save)
    destination_entry.state(['!disabled'])
    destination_entry.delete(0,END)
    destination_entry.insert(0,directory_path)
    destination_entry.state(['disabled'])
    if len(destination_entry.get())>0:
        crawl_button.state(['!disabled'])


##################################################################################3


#####################################################
def main(rootwindow):
    print('here')
    #rootwindow=Tk();
    #rootwindow.geometry('770x420')
    #rootwindow.resizable(FALSE,FALSE)
    parse_hmisv0.neo4j_username=neo4j_username
    parse_hmisv0.neo4j_password=neo4j_password
###############################RIGHT FRAME WIDGETS#########################################
    right_frame=ttk.Frame(rootwindow,height=420,width=350)
    task_field=Text(right_frame,height=1,width=49,font=('Aerial',10))
    task_tree=Text(right_frame,height=26,width=47,wrap='word',font=('Aerial',10))
    task_tree_scroll=ttk.Scrollbar(right_frame,orient=VERTICAL,command=task_tree.yview)
    task_tree.config(yscrollcommand=task_tree_scroll.set)
    task_field.grid(row=0,column=0,columnspan=2,rowspan=1,sticky='w')
    task_tree.grid(row=2,column=0,sticky='w')
    task_tree_scroll.grid(row=2,column=1,sticky='ns')
    right_frame.place(x=420,y=0)
    for widget in right_frame.grid_slaves():
        if widget.winfo_class()!='TScrollbar':
            widget.config(state='disabled')
        else:
            widget.state(['!disabled'])
####################################################################


###############################LEFT FRAME WIDGETS#########################################
    left_frame=ttk.Frame(rootwindow,width=420,height=420)
    top_label=Label(left_frame,relief=RAISED,bg='white',font=('Aerial',10),justify=LEFT,text='The crawler package for data.gov, will allow you to update the\t\t\t\ngovernment database in our package to the most recent statistics.')
    notice_frame=ttk.Frame(left_frame,height=240,width=310,)
    notice_text=Text(notice_frame,height=15,width=38,wrap='word')
    notice_text.insert(1.0,'Notice\nThe package here allows you to make a live update from data.gov.in, the statewise catalogues of the HMIS data.\n\n'
                           'The package below is in beta phase, so the success rate of the package varies, depending on your internet connection, update of information on the goverment catalogue server.\n\n'
                           'The package crawls goverment catalogues and fetch HMIS data files group them according to states, have a backup storage of the crawled files in a txt file, saving the downloaded csv file in the same directory.\n\n'
                           'There is an additional feature to the package; the catalogue dataset is too big, so we made this package to store the previous data download status and files too.\n\n'
                           'We keep track of the crawler, if your connection fails, just kill the current crawl and then restart it,  the crawler shall resume from the most recent status save, if no corruption of the package has occured.\n\n'
                           '')
    notice_scroll=ttk.Scrollbar(notice_frame,orient=VERTICAL,command=notice_text.yview)
    notice_text.config(yscrollcommand=notice_scroll.set)
    current_agreement=StringVar()
    current_agreement.set('disagree')
    progress=ttk.Progressbar(left_frame,length=240,mode='indeterminate',orient=HORIZONTAL)
    #crawler_thread=hmis_data_crawler(progress,task_field,task_tree)
    crawl_button=ttk.Button(left_frame,text='Crawl!')
    kill_button=ttk.Button(left_frame,text='Kill!')
    crawl_button.config(command=lambda :begin_crawl(crawl_button,kill_button,progress,task_field,task_tree))
    kill_button.config(command=lambda:stop_crawl(progress,crawl_button,kill_button,task_tree,task_field))
    kill_button.state(['disabled'])
    destination_location=ttk.Entry(left_frame,width=22)
    destination_location.state(['disabled'])
    directory_button=ttk.Button(left_frame,text='GO',width=4,command=lambda :get_directory_path(destination_location,crawl_button))
    directory_button.state(['disabled'])
    agree_button=ttk.Radiobutton(left_frame,text='I agree to the the terms',variable=current_agreement,value='agree',command= lambda:activate_crawl(crawl_button,current_agreement,directory_button,destination_location))
    disagree_button=ttk.Radiobutton(left_frame,text='I do not agree to the the terms',variable=current_agreement,value='disagree',command=lambda:activate_crawl(crawl_button,current_agreement,directory_button,destination_location))

    kill_button.place(x=320,y=340)
    crawl_button.state(['disabled'])
    left_frame.place(x=0,y=0)
    top_label.place(x=0,y=0)
    notice_frame.place(x=60,y=60)
    notice_text.grid(row=0,column=0)
    notice_scroll.grid(row=0,column=1,sticky='ns')
    agree_button.place(x=30,y=310)
    disagree_button.place(x=30,y=340)
    crawl_button.place(x=230,y=340)
    progress.place(x=90,y=380)
    destination_location.place(x=230,y=310)
    directory_button.place(x=370,y=310)
    #rootwindow.mainloop()
########################################################################################



def activate_crawl(crawl_button,current_agreement,diretory_button,directory_path):
    if current_agreement.get()=='agree':
        #crawl_button.state(['!disabled'])
        diretory_button.state(['!disabled'])
        directory_path.state(['!disabled'])
        directory_path.delete(0,END)
        directory_path.state(['disabled'])
    else:
        crawl_button.state(['disabled'])
        diretory_button.state(['disabled'])

def begin_crawl(crawl_button,kill_button,progress,task_field,task_tree):
    global flag_kill
    flag_kill=FALSE
    parse_hmisv0.kill_flag=False
    crawl_button.state(['disabled'])
    crawler_thread=hmis_data_crawler(progress,task_field,task_tree,crawl_button,kill_button)
    crawler_thread.start()
    print('crawl begin')
    kill_button.state(['!disabled'])

def stop_crawl(progress,crawl_button,kill_button,task_tree,task_field):
    #crawler_thread._stop()
    crawl_button.state(['!disabled'])
    kill_button.state(['disabled'])
    progress.stop()
    global file_download_count
    global kill_begin_count
    file_download_count=kill_begin_count
    global flag_kill
    flag_kill=TRUE
    parse_hmisv0.kill_flag=True
    task_tree.config(state='normal')
    task_field.config(state='normal')
    task_tree.replace(1.0,END,'Interruption detected!')
    task_field.replace(1.0,END,'If crawling was interrupted please begin again.')
    task_tree.config(state='disabled')
    task_field.config(state='disabled')
    messagebox.showinfo(title='Crawler Interrupt', message='You interrupted the crawler, please manually empty the folder before crawling; or choose an EMPTY LOCATION.\n'
                                                           'To resume from the last save point choose the same location(Do not alter the directory manually).')


if __name__=='__main__':main()