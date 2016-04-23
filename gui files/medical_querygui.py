from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import webbrowser
from doctors_lounge_dataset import data_collection
from doctors_lounge_dataset import crawl_topics
from doctors_lounge_dataset import query_parse
import threading
from py2neo import Graph,authenticate
neo4j_username=None
neo4j_password=None
try:
    authenticate("localhost:7474",neo4j_username,neo4j_password)
except Exception:
    none=None
graph=Graph()

delimiters=[',',';','?','/','-','_','+','=','(',')','|','\\','{','}','[',']',':','!','@','#','$','%','^','&','*','~','`','\"'
            ,', ','; ','? ','/ ','- ','_ ','+ ','= ', '( ',') ','| ','\\ ','{ ','} ','[ ','] ',': ','! ','@ ','# ','$ ','% ','^ ','& ','* ','~ ','` ','\" '
            ' ,',' ;',' ?',' /',' -',' _',' +',' =',' (',' )',' |',' \\',' {',' }' ,' [',' ]',' :',' !',' @',' #',' $',' %',' ^',' &',' *',' ~',' `' ,' \"']

flag_kill_recommender=FALSE
user_query=None
recommend_query_text=NONE
keyword_dict={}
query_count=NONE


class recomender_thread(threading.Thread):
    def __int__(self):
        threading.Thread.__init__(self)


    def run(self):
        global user_query
        global recommend_query_text
        self.user_query=user_query
        self.recommend_query_text=recommend_query_text
        query_line=1.0
        if(len(self.user_query)!=0) and flag_kill_recommender==FALSE:
            key_list=self.user_query.split(" ")
            print(key_list)
            if len(key_list)==1 and flag_kill_recommender==FALSE:
                query_search=graph.cypher.execute('MATCH(w:Word)WHERE w.name=~"(?i)'+key_list[0]+'" WITH w.query_index as query_index UNWIND(query_index) as index  MATCH(q:Query_Topic{query_index:index}) RETURN q.query LIMIT 30')
                print(query_search)
                self.recommend_query_text.config(state='normal')
                self.recommend_query_text.delete(1.0,END)
                self.recommend_query_text.config(state='disabled')
                for query in query_search:
                    print(str(query).split('query')[1].replace('-','').strip())
                    self.recommend_query_text.config(state='normal')
                    self.recommend_query_text.insert(query_line,'@'+str(query).split('query')[1].replace('-','').strip()+'\n')
                    self.recommend_query_text.config(state='disabled')
                    query_count.set(getint(query_line))
                    query_line+=1
            else:
                self.recommend_query_text.config(state='normal')
                self.recommend_query_text.replace(1.0,END,'Searching...')
                self.recommend_query_text.config(state='disabled')
                query_index=[]
                extra_space_count=0
                for keyword in key_list:
                    print(len(keyword))
                    if(len(keyword)==0) and flag_kill_recommender==FALSE:
                        extra_space_count+=1
                        continue
                    temp_index_list=[]
                    try:
                        temp_index_list+=keyword_dict[keyword]
                    except Exception:
                        #print(str(graph.cypher.execute('MATCH (w:Word{name:"'+keyword+'"}) RETURN w.query_index')).split('[')[1].split(']')[0])
                        temp_index_str=str(graph.cypher.execute('MATCH (w:Word) WHERE w.name=~"(?i)'+keyword+'" RETURN w.query_index')).split('[')[1].split(']')[0].split(',')
                        for index in temp_index_str:
                            if int(index.strip()) not in temp_index_list and flag_kill_recommender==FALSE:
                                temp_index_list+=[int(index.strip())]
                        keyword_dict.update({keyword:temp_index_list})
                    print(temp_index_list)
                    print(len(temp_index_list))
                    if len(temp_index_list)!=0:
                        query_index+=[temp_index_list]
                print(query_index)
                dump_index=[]
                union_index=[]
                count_index=0
                for index_list in query_index:
                    dump_index+=index_list
                    for index in index_list:
                        count_index=0
                        for index_dump in dump_index:
                            if index == index_dump and flag_kill_recommender==FALSE:
                                    count_index+=1
                        #print(count_index)
                        if count_index!=len(key_list)-extra_space_count and flag_kill_recommender==FALSE:
                            union_index+=[index]
                print(dump_index)
                print(len(dump_index))
                print(union_index)
                print(len(union_index))
                intersection_index=dump_index
                for index in union_index:
                    intersection_index.remove(index)
                print(intersection_index)
                if len(intersection_index)==0:
                    intersection_index=union_index[0:60]

                if flag_kill_recommender==FALSE:

                        print(intersection_index)
                        query_found=graph.cypher.execute('WITH '+str(intersection_index)+' as root UNWIND(root) as index MATCH(w:Word)WHERE index in w.query_index WITH COLLECT(w.name) as word_list,index  UNWIND(word_list) as word MATCH(w1:Word{name:word})-[rl:NEXT]->(w2:Word) where index in w2.query_index with collect(rl.count) as _count_list,index with reduce(done=0, x in _count_list|done+x) as _count,index MATCH(q:Query_Topic{query_index:index}) return q.query,_count ORDER BY q.query_rank DESC,_count LIMIT 30')
                        print('WITH  range('+str(index)+','+str(index)+') as root UNWIND(root) as index MATCH(w:Word)WHERE index in w.query_index WITH COLLECT(w.name) as word_list,index  UNWIND(word_list) as word MATCH(w1:Word{name:word})-[rl:NEXT]->(w2:Word) where index in w2.query_index with collect(rl.count) as _count_list,index with reduce(done=0, x in _count_list|done+x) as _count,index MATCH(q:Query_Topic{query_index:index}) return q.query,_count ORDER BY q.query_rank,_count DESC LIMIT 30')
                        self.recommend_query_text.config(state='normal')
                        self.recommend_query_text.delete(1.0,END)
                        self.recommend_query_text.config(state='disabled')
                        for query in query_found:
                            print(str(query).split('query')[1].replace('-','').strip())
                            self.recommend_query_text.config(state='normal')
                            self.recommend_query_text.insert(query_line,'@'+str(query).split('query')[1].replace('-','').strip()+'\n')
                            self.recommend_query_text.config(state='disabled')
                            query_count.set(getint(query_line))
                            query_line+=1
                            print(query_count.get())


class query_recommender:
    def __init__(self,root_window,rootwindow):
        self.rootwindow=rootwindow
        self.window=root_window
        self.main_tab=ttk.Notebook(root_window,height=420,width=770)
        self.main_tab.place(x=0,y=0)
        print(self.main_tab.winfo_class())
        self.search_frame=ttk.Frame(self.main_tab,height=400,width=770)
        self.create_frame=ttk.Frame(self.main_tab,height=400,width=770)
        self.main_tab.add(self.search_frame,text='Medical Query Database')
        self.main_tab.add(self.create_frame,text='Create Live Query Database')

        ###############FORUM SERACH FROM THE DATASET###############
        self.forum_list=['Select Forum']
        forums=graph.cypher.execute('MATCH(f:Forum) RETURN f.forum_name ORDER BY f.forum_name')
        for forum in forums:
            print(str(forum).split('forum_name')[1].replace('-','').strip())
            self.forum_list+=[str(forum).split('forum_name')[1].replace('-','').strip()]
        ###########################################################

        ###############DEFAULT HEAD TOPIC SELECTION###############
        self.head_list=['Select Head-Topic']
        head_topics=graph.cypher.execute('MATCH(h:Head_Topic) RETURN h.topic ORDER BY h.topic')
        for topic in head_topics:
            print(str(topic).split('topic')[1].replace('-','').strip())
            self.head_list+=[str(topic).split('topic')[1].replace('-','').strip()]
        ###########################################################

        ###############DEFAULT SUB TOPIC SELECTION###############
        self.sub_list=['Select Sub-Topic']
        sub_topics=graph.cypher.execute('MATCH(s:Sub_Topic) RETURN s.topic ORDER BY s.topic')
        for topic in sub_topics:
            print(str(topic).split('topic')[1].replace('-','').strip())
            self.sub_list+=[str(topic).split('topic')[1].replace('-','').strip()]
        ###########################################################

        ##########################MEDICAL QUERY DARABASE_TAB####################
        style=ttk.Style()
        style.configure('status.TFrame',bg='blue')
        self.search_display_frame=ttk.Frame(self.search_frame,height=390,width=770)
        self.search_status_frame=ttk.Frame(self.search_frame,height=170,width=770,style='status.TFrame')
        self.query_text=Text(self.search_display_frame,width=50,height=4,wrap='word',font=('Aerial',10))
        recommend_query_scroll_frame=Frame(self.search_display_frame,height=80,width=70)
        query_url_scroll_frame=Frame(self.search_display_frame,height=80,width=70)
        self.recommend_query_text=Text(recommend_query_scroll_frame,width=50,height=4,wrap='word',font=('Aerial',10))
        #self.query_url_text=Text(query_url_scroll_frame,width=50,height=4,wrap='word',font=('Aerial',10))
        self.current_selected_query_use=IntVar()
        self.current_selected_url_get=IntVar()
        self.query_use=ttk.Checkbutton(self.search_display_frame,text='Use Query?',variable=self.current_selected_query_use,command=self.recommend_query)
        self.url_get=ttk.Checkbutton(self.search_display_frame,text='Get URL',variable=self.current_selected_url_get,command=self.retrieve_url)
        self.search_submit=ttk.Button(self.search_display_frame,text='Submit',command=self.submit_selection)
        self.query_status_text=Text(self.search_status_frame,width=104,height=12,wrap='word',font=('Aerial',10))
        self.current_selected_forum=StringVar()
        self.current_selected_head=StringVar()
        self.current_selected_sub=StringVar()

        self.forum_dropdown=ttk.Combobox(self.search_display_frame,width=25,value=self.forum_list,textvariable=self.current_selected_forum,postcommand=self.forum_change)
        self.main_head_dropdown=ttk.Combobox(self.search_display_frame,width=25,value=self.head_list,textvariable=self.current_selected_head,postcommand=self.head_change)
        self.sub_head_dropdown=ttk.Combobox(self.search_display_frame,width=25,value=self.sub_list,textvariable=self.current_selected_sub,postcommand=self.sub_change)
        self.select_forum=IntVar()
        self.select_head=IntVar()
        self.select_sub=IntVar()
        self.forum_check=ttk.Checkbutton(self.search_display_frame,text='Done',variable=self.select_forum,command=self.forum_display)
        self.head_check=ttk.Checkbutton(self.search_display_frame,text='Done',variable=self.select_head,command=self.head_display)
        self.sub_check=ttk.Checkbutton(self.search_display_frame,text='Done',variable=self.select_sub,command=self.sub_display)
        self.forum_dropdown.set('Select Forum')
        self.main_head_dropdown.set('Select Head-Topic')
        self.sub_head_dropdown.set('Select Sub-Topic')
        self.current_selected_query_status=IntVar()
        self.current_selected_query_status.set(1)
        self.query_status=ttk.Checkbutton(self.search_display_frame,text='Check Here To See Details',variable=self.current_selected_query_status,command=self.status_display)
        self.recommend_query_scroll=ttk.Scrollbar(recommend_query_scroll_frame,orient=VERTICAL,command=self.recommend_query_text.yview)
        #self.query_url_scroll=ttk.Scrollbar(query_url_scroll_frame,orient=VERTICAL,command=self.query_url_text.yview)
        self.status_scroll=ttk.Scrollbar(self.search_status_frame,orient=VERTICAL,command=self.query_status_text.yview)
        self.recommend_query_text.config(yscrollcommand=self.recommend_query_scroll.set)
        #self.query_url_text.config(yscrollcommand=self.query_url_scroll.set)
        self.query_status_text.config(yscrollcommand=self.status_scroll.set,cursor='hand2')
        self.query_status_text.bind('<1>',lambda e:self.find_query('<1>',self.query_status_text))
        self.query_text.insert(1.0,str.lower('*******ENTER YOUR QUERY HERE*******\nTRY NOT TO USE ANY KIND OF SPECIAL SYMBOLS \nAFTER EACH KEYWORD ENTER A SPACE ONLY THEN THE KEYWORD WILL BE ACCEPTED FOR RECOMMENDATION SEARCH'))
        self.query_text.config(state='disabled')
        self.recommend_query_text.insert(1.0,str.lower('*** RECOMMENDED QUERIES WILL BE HERE****\n IF YOU HAVE A QUERY PASTE HERE THEN CHECK "GET URL" AND URL WILL BE RETRIEVED FROM THE DATASET- DO NOT MODIFY THIS FIELD'))
        self.recommend_query_text.config(state='disabled')
        self.recommend_query_text.bind('<Triple-1>',self.recommend_url)
        self.recommend_dispaly_flag=FALSE
        clear_warning=Label(query_url_scroll_frame,bg='white',text='We allow you to modify current database, to clear your ranking cache and\nalso clear databsae completely! Use Carefully!')
        self.cache_value=IntVar()
        self.cache_button=ttk.Button(query_url_scroll_frame,text='Clear query cache',command=self.clear_cache)
        self.delete_button=ttk.Button(query_url_scroll_frame,text='Delete Database',command=self.clear_database)
        ###################################

        self.search_display_frame.place(x=0,y=0)
        self.search_status_frame.place(x=10,y=190)
        recommend_query_scroll_frame.place(x=10,y=100)
        query_url_scroll_frame.place(x=390,y=100)
        clear_warning.grid(row=0,column=0,columnspan=2)
        self.cache_button.grid(row=1,column=0,pady=10)
        self.delete_button.grid(row=1,column=1,pady=10)
        self.query_text.place(x=10,y=5)
        self.query_use.place(x=290,y=75)
        #self.url_get.place(x=290,y=170)
        #self.query_url_text.insert(1.0,str.lower('ONLY ONE URL WILL BE DISPLAYED HERE- THE QUERY ON THE TOP OF THE LIST IN RECOMMEND SEARCH- PASTE A QUERY TO GET ITS URL'))
        #self.query_url_text.config(state='disabled')
        self.url_get.state(['disabled'])
        self.forum_dropdown.place(x=390,y=5)
        self.main_head_dropdown.place(x=580,y=5)
        self.sub_head_dropdown.place(x=390,y=50)
        self.forum_check.place(x=530,y=27)
        self.head_check.place(x=710,y=27)
        self.sub_check.place(x=530,y=75)
        self.search_submit.place(x=620,y=50)
        self.recommend_query_text.grid(row=0,column=0)
        self.recommend_query_scroll.grid(row=0,column=1,sticky='ns')
        #self.query_url_text.grid(row=0,column=0)
        #self.query_url_scroll.grid(row=0,column=1,sticky='ns')
        self.query_status.place(x=10,y=170)
        self.query_status_text.grid(row=0,column=1,rowspan=2,pady=10)
        self.status_scroll.grid(row=0,column=2,rowspan=2,pady=10,sticky='ns')

        ######################################################

        ############## CREATE QUERY DATASET##########################
        crawler_frame=ttk.Frame(self.create_frame,height=390,width=385)
        creator_frame=ttk.Frame(self.create_frame,height=390,width=385)
        crawler_frame.place(x=0,y=0)
        creator_frame.place(x=385,y=0)
        ######################CRAWLER FRAME WIDGETS##############
        top_label=Label(crawler_frame,relief=RAISED,bg='white',font=('Aerial',10),text='The following crawler will help you to collect Live medical queries.\nNote that this is only for Educational Purposes.',justify=LEFT)
        instruction_label=Label(crawler_frame,justify=LEFT,text='Please read the following carefully.Only after agreeing to the \nterms below you can access live update.')
        instruction_frame=ttk.Frame(crawler_frame,height=210,width=300)
        instruction_text=Text(instruction_frame,height=13,width=40 ,wrap='word')
        instruction_text.insert(1.0,'Notice\nThe below package contains the access to crawl forum, Doctor\'s Lounge. It is a online medical query forum.\n\n'
                                                                        'With the use of this package you will be able to access all the medical queries ever discussed on the forum, remotely on your desktop.'
                                                                        'The use of such dataset for commercial purposes is strictly discouraged.\n\n'
                                                                        'We are providing this package only in use for Educational Purposes. To study these medical queries for Medical Data Analysis or other\n'
                                                                        'Academic activities.\n\n'
                                                                        'Following are a few steps, first you must adhere to before crawling through the forum\n\n'
                                                                        '@Make sure that you select a new directory, to store the updated Query DataSet.\n\n'
                                                                        '@If the directory provided by us is selected it may corrupt the current DataSet and the whole package may not work correctly\n\n'
                                                                        '@If somehow the DataSet gets corrupted please copy the backup provided by us in the backup directory to "doctors_lounge_dataset" directory and then create a new Dataset\n\n'
                                                                        '@Make sure your system has connection to the internet and has no SSL bound, else this may not work properly\n\n')
        instruction_text.config(state='disabled')
        instruction_text_scroll=ttk.Scrollbar(instruction_frame,orient=VERTICAL,command=instruction_text.yview)
        instruction_text.config(yscrollcommand=instruction_text_scroll.set)
        self.current_selected_agreement=StringVar()
        self.current_selected_agreement.set('disagree')
        self.agree_button=ttk.Radiobutton(crawler_frame,text='I agree to the terms',variable=self.current_selected_agreement,value='agree',command=self.activate_crawl)
        self.disagree_button=ttk.Radiobutton(crawler_frame,text='I do not agree to the terms',variable=self.current_selected_agreement,value='disagree',command=self.activate_crawl)
        self.directory_entry=ttk.Entry(crawler_frame,width=22)
        self.directory_button=ttk.Button(crawler_frame,text='GO',width=4,command=self.get_directory_path)
        self.crawl_button=ttk.Button(crawler_frame,text='Crawl!',command=self.crawl_web)

        top_label.place(x=0,y=0)
        instruction_label.place(x=40,y=40)
        instruction_frame.place(x=40,y=70)
        instruction_text.grid(row=0,column=0)
        instruction_text_scroll.grid(row=0,column=1,sticky='ns')
        self.agree_button.place(x=30,y=300)
        self.disagree_button.place(x=30,y=330)
        self.directory_entry.place(x=200,y=300)
        self.directory_button.place(x=340,y=300)
        self.crawl_button.place(x=260,y=340)
        self.directory_entry.state(['disabled'])
        self.directory_button.state(['disabled'])
        self.crawl_button.state(['disabled'])
        self.directory_path=''
##############################################################################################################

    ###########################MEDICAL DATABASE CREATE WIDGETS#############################################
        top_label_create=Label(creator_frame,relief=RAISED,bg='white',font=('Aerial',10),text='The following package will aid you to create neo4j graph dataset.\nPlease read the prerequites below to continue.',justify=LEFT)
        instruction_label_create=Label(creator_frame,justify=LEFT,text='Following are listed the prerequisites.\nFollow the instructions or you may corrupt dataset')
        instruction_frame_create=ttk.Frame(creator_frame,height=210,width=300)
        instruction_text_create=Text(instruction_frame_create,height=13,width=40 ,wrap='word')
        instruction_text_create.insert(1.0,'Notice\nThe below package will allow tou to create a graphene database of the query dataset.\n\n'
                                                                        'If you have made a live update using our Query Crawler package just check use the same path as crawler and crate the database. This package will take care from their'
                                                                        'This package parses through the query file generated by the crawler package, and design a database that has efficient storage capability and a specific format.\n\n'
                                                                        'If you want to use yout own dataset, please look into the query_file in our package directory study the format and alter your file accordingly.\n\n'
                                                                        'Failure to alter the file in given format will alter the format of database and database corrupton may crash this whole package.\n\n'
                                                                        'On any instance this package stops working, use a neo4j empty database, then you can use the crawler package and parser to create a correct formatted database.\n\n'
                                                                        'Following are a few steps, first you must adhere to before creating a new database\n\n'
                                                                        '@Make sure that neo4j client is active with a new database storage directory, use of our directory will corrupt the current dataset and package may not work efficiently in the future\n\n'
                                                                        '@If somehow the DataSet gets corrupted please copy the backup provided by us in the backup directory to "doctors_lounge_dataset" directory and then create a new Dataset\n\n'
                                                                        '@Make sure your system has running neo4j client, and you have entered correct authentication details.\n\n')
        instruction_text_create.config(state='disabled')
        instruction_text_create_scroll=ttk.Scrollbar(instruction_frame_create,orient=VERTICAL,command=instruction_text_create.yview)
        instruction_text_create.config(yscrollcommand=instruction_text_create_scroll.set)
        self.prerequisites_status=IntVar()
        self.prerequisites_check=ttk.Checkbutton(creator_frame,text='Prerequisites completed',variable=self.prerequisites_status,command=self.activate_create)
        self.use_crawler_path_status=IntVar()
        self.use_crawler_path=ttk.Checkbutton(creator_frame,text='I want to use same path as Crawler',variable=self.use_crawler_path_status,command=self.get_crawler_path)
        self.directory_entry_create=ttk.Entry(creator_frame,width=22)
        self.directory_button_create=ttk.Button(creator_frame,text='GO',width=4,command=self.get_directory_path_create)
        self.create_button=ttk.Button(creator_frame,text='Create!',command=self.create_dataset)
       # print(query_parse.query_data_len)
        self.create_progress=ttk.Progressbar(creator_frame,length=370,orient=HORIZONTAL,mode='indeterminate')
        top_label_create.place(x=0,y=0)
        instruction_label_create.place(x=40,y=40)
        instruction_frame_create.place(x=40,y=70)
        instruction_text_create.grid(row=0,column=0)
        instruction_text_create_scroll.grid(row=0,column=1,sticky='ns')

        self.prerequisites_check.place(x=50,y=280)
        self.use_crawler_path.place(x=50,y=310)
        self.directory_entry_create.place(x=50,y=340)
        self.directory_button_create.place(x=210,y=340)
        self.create_button.place(x=290,y=340)
       # self.create_progress.place(x=10,y=360)


        self.use_crawler_path.state(['disabled'])
        self.directory_entry_create.state(['disabled'])
        self.directory_button_create.state(['disabled'])
        self.create_button.state(['disabled'])
        self.directory_path_create=''

        ########################LABEL FOR RECOMMENDWINDOW DECLARATION######
        recommend_query_count=StringVar()
        global query_count
        query_count=recommend_query_count
        query_count.set('0')





##############DATABASE MANIPULATION####################
    def clear_cache(self):
        proceed_choice=messagebox.askyesno(title='Cache Clearance',message='Do you want to clear your previous query_use ranking selection?')
        if proceed_choice:
            graph.cypher.execute('MATCH(q:Query_Topic) SET q.query_rank=0')
            self.query_status_text.config(state='normal')
            self.query_status_text.replace(1.0,END,'Clearing cached preferences,may take some time; sit back have coffee!')
            self.query_status_text.config(state='disabled')
    def clear_database(self):
        proceed_choice=messagebox.askyesno(title='Database Clearance',message='Do you want to clear your database, all query data will be removed?')
        if proceed_choice:
            self.query_status_text.config(state='normal')
            self.query_status_text.insert(1.0,END,'Cleaning database,may take some time; sit back have coffee!')
            self.query_status_text.config(state='disabled')
            graph.cypher.execute('MATCH(n) OPTIONAL MATCH(n)-[r]-() DELETE n,r')
###################################################################
    def recommend_url(self,event):
        if self.current_selected_query_use.get()==1 and len(self.recommend_query_text.get(1.0,END))>1:
            if self.recommend_dispaly_flag==FALSE:
                self.recommend_window=Toplevel(self.window)
                #recommend_window.transient()
                #self.window.state('withdrawn')
                self.recommend_window.overrideredirect(TRUE)
                self.recommend_window.title('Recommended Queries')
                self.recommend_window.resizable(FALSE,FALSE)
                self.recommend_query_count=ttk.Label(self.recommend_window,textvariable=query_count)
                self.recommend_query_window_text=Text(self.recommend_window,font=('Aerial',10),height=30,width=100,wrap='word',cursor='hand2')
                scroll_recommend_window_text=ttk.Scrollbar(self.recommend_window,orient=VERTICAL,command=self.recommend_query_window_text.yview)
                self.recommend_query_window_text.config(yscrollcommand=scroll_recommend_window_text.set)
                self.recommend_query_window_text.grid(row=0,column=0,columnspan=2)
                scroll_recommend_window_text.grid(row=0,column=2,sticky='ns')
                self.recommend_query_window_text.insert(1.0,str.lower(self.recommend_query_text.get(1.0,END)))
                self.recommend_query_window_text.config(state='disabled')
                self.close_recommend_text=ttk.Button(self.recommend_window,text='Close',command=self.return_query_window)
                self.close_recommend_text.grid(row=1,column=0,pady=5,padx=5,sticky='e')
                self.refresh_recommend_text=ttk.Button(self.recommend_window,text='Refresh',command=self.refresh_recommender_window)
                self.refresh_recommend_text.grid(row=1,column=1,pady=5,padx=5,sticky='w')
                self.recommend_query_count.grid(row=1,column=1,pady=5,padx=5,sticky='e')
                self.recommend_dispaly_flag=TRUE
           # self.recommend_query_window_text.c

            self.recommend_query_window_text.bind('<1>',lambda e:self.find_query('<1>',self.recommend_query_window_text))

    def find_query(self,event,text_widget):
        try:
            text_widget.tag_remove('selection','selection.first','selection.last')
        except Exception:
            task=None
        #self.recommend_query_window_text.config(state='normal')

        text_widget.tag_add('selection','current linestart','current lineend')
        text_widget.tag_configure('selection',background='yellow')
        #print(self.recommend_query_window_text.mark_names())
        #self.recommend_query_window_text.insert('insert','hey')
        #print(self.recommend_query_window_text.get('current linestart','current lineend'))
##########################RETRIEVE URL AND OPEN IN BROWSER#################################
        query_to_get=text_widget.get('current linestart','current lineend')
        query_to_get=query_to_get.replace('@','').strip()
        print(query_to_get)
        url=graph.cypher.execute('MATCH (q:Query_Topic) WHERE TOLOWER(q.query)="'+str.lower(query_to_get)+'" SET q.query_rank=q.query_rank+1 RETURN q.query_url')
        print('MATCH (q:Query_Topic) WHERE TOLOWER(q.query)="'+str.lower(query_to_get)+'" SET q.query_rank=q.query_rank+1 RETURN q.query_url')
        print(str(url).split('query_url')[1].replace('-','').strip())
        if len(str(url).split('query_url')[1].replace('-','').strip())==1:
                self.no_url_message()

        for link in url:
            print(str(link).split('query_url')[1].replace('-','').strip())

            #self.query_url_text.insert(1.0,str(link).split('query_url')[1].replace('-','').strip())
            webbrowser.open_new_tab( str(link).split('query_url')[1].replace('-','').strip()+ 'doc/')
###########################################################################################


    def return_query_window(self):
        self.recommend_window.state('withdrawn')
        #self.window.state('normal')
        #self.window.deiconify()
        self.recommend_dispaly_flag=FALSE

    def refresh_recommender_window(self):
        self.recommend_query_window_text.config(state='normal')
        self.recommend_query_window_text.replace(1.0,END,str.lower(self.recommend_query_text.get(1.0,END)))
        self.recommend_query_window_text.config(state='disabled')
#########

###############################SEARCH TAB CALLBACK FUNCTIONS####################################
    ###########################SUBMIT BUTTON SELECTION#################
    def submit_selection(self):

        line_count=1.0
        #self.query_status_text.delete(1.0,'end')
        #self.recommend_query_text.config(state='normal')
        #self.recommend_query_text.delete(1.0,'end')
        #self.recommend_query_text.config(state='disabled')
        cypher_search_query='MATCH(q:Query_Topic'
        if(self.current_selected_query_use.get()==0):
            if self.select_forum.get()==1:
                forum_name=self.current_selected_forum.get()
                cypher_search_query+='{forum_name:"'+forum_name+'"'
            if self.select_head.get()==1:
                head_topic=self.current_selected_head.get()
                if(self.select_forum.get()==1):
                    cypher_search_query+=',head_topic:"'+head_topic+'"'
                else:
                    cypher_search_query+='{head_topic:"'+head_topic+'"'
            if self.select_sub.get()==1:
                sub_topic=self.current_selected_sub.get()
                if(self.select_forum.get()==1) or (self.select_head.get()==1):
                    cypher_search_query+=',sub_topic:"'+sub_topic+'"'
                else:
                    cypher_search_query+='{sub_topic:"'+sub_topic+'"'
            if(self.select_forum.get()==1)or (self.select_head.get()==1) or self.select_sub.get()==1:
                cypher_search_query+='}) RETURN q ORDER BY q.query_rank DESC'
            else:
                cypher_search_query+=') RETURN q ORDER BY q.query_rank DESC'
                return
            query_list=graph.cypher.execute(cypher_search_query)
            print("*******************THE LIST OF QUERIES******************************")
            self.query_status_text.config(state='normal')
            self.query_status_text.insert(line_count,"*******************THE LIST OF QUERIES******************************\n")
            line_count+=1
            for query in query_list:
                print(query)
                print(str(query).split('query:"')[1].split('"')[0])
                self.query_status_text.insert(line_count,str(query).split('query:"')[1].split('",query_index')[0]+'\n')
                line_count+=1
            self.query_status_text.config(state='disabled')
    ######################################################################################


    ##########################RECOMMEND QUERY###############################
    def recommend_query(self):
        if self.current_selected_query_use.get()==1:
            ###################DISABLING OPTIONAL SEARCH##############
            self.current_selected_forum.set('Select Forum')
            self.current_selected_head.set('Select Head-Topic')
            self.current_selected_sub.set('Select Sub-Topic')
            self.forum_dropdown.state(['disabled'])
            self.main_head_dropdown.state(['disabled'])
            self.sub_head_dropdown.state(['disabled'])
            self.forum_check.state(['disabled'])
            self.head_check.state(['disabled'])
            self.sub_check.state(['disabled'])
            self.search_submit.state(['disabled'])
            #########################################################

            #################ENABLE QUERY SEARCH####################
            self.query_text.config(state='normal')
            self.recommend_query_text.config(state='normal')
            self.url_get.state(['!disabled'])
            self.query_text.delete(1.0,END)
            self.recommend_query_text.delete(1.0,END)
            self.recommend_query_text.config(state='disabled')

            ######################################################
            self.query_text.bind('<space>',self.query_recommend_search)
        else:
            self.query_text.unbind('<space>')
            ###################ENABLE OPTIONAL SEARCH##############
            self.forum_dropdown.state(['!disabled'])
            self.main_head_dropdown.state(['!disabled'])
            self.sub_head_dropdown.state(['!disabled'])
            self.forum_check.state(['!disabled'])
            self.head_check.state(['!disabled'])
            self.sub_check.state(['!disabled'])
            self.search_submit.state(['!disabled'])

            ########################################################

            #################DISABLING QUERY SEARCH####################
            self.query_text.delete(1.0,END)
            self.recommend_query_text.config(state='normal')
            self.recommend_query_text.delete(1.0,END)
            #self.query_url_text.delete(1.0,END)
            self.query_text.insert(1.0,str.lower('*******ENTER YOUR QUERY HERE*******\nTRY NOT TO USE ANY KIND OF SPECIAL SYMBOLS \nAFTER EACH KEYWORD ENTER A SPACE ONLY THEN THE KEYWORD WILL BE ACCEPTED FOR RECOMMENDATION SEARCH'))
            self.recommend_query_text.insert(1.0,str.lower('*** RECOMMENDED QUERIES WILL BE HERE****\n IF YOU HAVE A QUERY PASTE HERE THEN CHECK "GET URL" AND URL WILL BE RETRIEVED FROM THE DATASET- DO NOT MODIFY THIS FIELD'))
            #self.query_url_text.insert(1.0,str.lower('ONLY ONE URL WILL BE DISPLAYED HERE- THE QUERY ON THE TOP OF THE LIST IN RECOMMEND SEARCH- PASTE A QUERY TO GET ITS URL'))

            self.query_text.config(state='disabled')
            self.recommend_query_text.config(state='disabled')
           # self.query_url_text.config(state='disabled')
            self.current_selected_url_get.set(0)
            self.url_get.state(['disabled'])
            ######################################################
    ########################################################################






    #################QUERY RECOMMEND SEARCH####################################
    def query_recommend_search(self,event):
        self.recommend_query_text.config(state='normal')
        self.recommend_query_text.replace(1.0,END,'Searching...')
        self.recommend_query_text.config(state='disabled')
        global flag_kill_recommender
        flag_kill_recommender=TRUE
        user_query=self.query_text.get(1.0,END).strip()
        for symbol in delimiters:
            user_query=user_query.replace(symbol,'').strip()
        print(user_query)
        print(len(user_query))
        global user_query
        user_query=user_query
        global recommend_query_text
        recommend_query_text=self.recommend_query_text
        #recommend_query_text=self.recommend_query_text
        get_recommendation=recomender_thread()
        flag_kill_recommender=FALSE
        get_recommendation.start()

    ######################################################################################



    def retrieve_url(self):
        if self.current_selected_url_get.get()==1:
            #self.query_url_text.config(state='normal')
            #self.query_url_text.delete(1.0,'end')
            query_to_get=self.recommend_query_text.get(1.0,'1.end')
            print(query_to_get)
            query_to_get=query_to_get.replace('@','').strip()
            url=graph.cypher.execute('MATCH (q:Query_Topic{query:"'+query_to_get+'"})  RETURN q.query_url')
            print(url)
            print(str(url).split('query_url')[1].replace('-','').strip())
            if len(str(url).split('query_url')[1].replace('-','').strip())==1:
                    self.no_url_message()

            for link in url:
                print(str(link).split('query_url')[1].replace('-','').strip())

                #self.query_url_text.insert(1.0,str(link).split('query_url')[1].replace('-','').strip())
                webbrowser.open_new_tab( str(link).split('query_url')[1].replace('-','').strip()+ 'doc/')
        #else:
            #self.query_url_text.delete(1.0,END)
            #self.query_url_text.insert(1.0,'ONLY ONE URL WILL BE DISPLAYED HERE- THE QUERY ON THE TOP OF THE LIST IN RECOMMEND SEARCH- PASTE A QUERY TO GET ITS URL')
            #self.query_url_text.config(state='disabled')


    def no_url_message(self):

        messagebox.showerror(title='URL SEARCH FAILED',message='The query was not found in the dataset: Please do not modify the query!')
        self.current_selected_url_get.set(0)

    #################FORUM DISPLAY##################

    def forum_change(self):
        self.select_forum.set(0)
        self.select_head.set(0)
        self.select_sub.set(0)
        self.main_head_dropdown.config(value=self.head_list)
        self.sub_head_dropdown.config(value=self.sub_list)
        self.main_head_dropdown.set('Select Head-Topic')
        self.sub_head_dropdown.set('Select Sub-Topic')

    def forum_display(self):
        if self.select_forum.get()==1:
            if self.current_selected_forum.get()!='Select Forum':
                forum_name=self.current_selected_forum.get()
                if forum_name in self.forum_list:

                    ###############UPDATE HEAD TOPIC SELECTION###############
                    new_head_list=['Select Head-Topic']
                    head_topics=graph.cypher.execute('MATCH(f:Forum{forum_name:"'+forum_name+'"}) OPTIONAL MATCH(f)-->(h:Head_Topic) RETURN h.topic ORDER BY h.topic')
                    #print(head_topics)
                    for topic in head_topics:
                        print(str(topic).split('topic')[1].replace('-','').strip())
                        new_head_list+=[str(topic).split('topic')[1].replace('-','').strip()]
                    self.main_head_dropdown.config(value=new_head_list)
                    ###########################################################
                else:
                    self.message_info_display()
                    self.forum_dropdown.set('Select Forum')
            else:
                self.message_info_display()
                self.select_forum.set(0)
        else:
            self.main_head_dropdown.config(value=self.head_list)
            self.forum_dropdown.set('Select Forum')
    ###########################################################

    #####################HEAD-TOPIC DISPLAY####################

    def head_change(self):
        self.select_head.set(0)
        self.select_sub.set(0)
        self.sub_head_dropdown.config(value=self.sub_list)
        self.sub_head_dropdown.set('Select Sub-Topic')
    def head_display(self):
        if self.select_head.get()==1:
            if self.current_selected_head.get()!='Select Head-Topic':
                head_topic=self.current_selected_head.get()
                if head_topic in self.head_list:
                    ###############UPDATE SUB TOPIC SELECTION###############
                    new_sub_list=['Select Sub-Topic']
                    sub_topics=graph.cypher.execute('MATCH(h:Head_Topic{topic:"'+head_topic+'"}) OPTIONAL MATCH(h)-->(s:Sub_Topic) RETURN s.topic ORDER BY s.topic')
                    #print(sub_topics)
                    for topic in sub_topics:
                        print(str(topic).split('topic')[1].replace('-','').strip())
                        new_sub_list+=[str(topic).split('topic')[1].replace('-','').strip()]
                    self.sub_head_dropdown.config(value=new_sub_list)
                    ###########################################################
                else:
                    self.message_info_display()
                    self.main_head_dropdown.set('Select Head-Topic')
            else:
                self.message_info_display()
                self.select_head.set(0)
        else:
            self.sub_head_dropdown.config(value=self.sub_list)
            self.main_head_dropdown.set('Select Head-Topic')
    ##########################################################

    #################SUB-TOPIC DISPLAY############
    def sub_change(self):
        self.select_sub.set(0)
    def sub_display(self):
        if self.select_sub.get()==1:
            if self.current_selected_sub.get()!='Select Sub-Topic':
                sub_topic=self.current_selected_sub.get()
                if sub_topic not in self.sub_list:
                    self.message_info_display()
                    self.sub_head_dropdown.set('Select Sub-Topic')
            else:
                self.message_info_display()
                self.select_sub.set(0)
        else:
            self.sub_head_dropdown.set('Select Sub-Topic')
    ###############################################

    ###########################STATUS TEXT DISPLAY###################
    def status_display(self):
        if self.current_selected_query_status.get()==0:
            for widget in self.search_status_frame.grid_slaves():
                widget.grid_forget()
        else:
            self.search_status_frame.place(x=10,y=190)
            self.query_status_text.grid(row=0,column=1,rowspan=2,pady=10)
            self.status_scroll.grid(row=0,column=2,rowspan=2,pady=10,sticky='ns')

    def message_info_display(self):
        messagebox.showinfo(title='Invalid Selection',message='The selection of the option doesn\'t seem to exist in the database!')
####################################################################################################

################################CREATE DATASET CALL BACK FUNCTIONS######################################
    def activate_crawl(self):
        self.prerequisites_status.set(0)
        self.activate_create()
        if self.current_selected_agreement.get()=='agree':
            #self.directory_entry.state(['!disabled'])
            self.directory_button.state(['!disabled'])
            #self.crawl_button.state(['!disabled'])
        else:
            self.directory_entry.state(['!disabled'])
            self.directory_entry.delete(0,END)
            self.directory_entry.state(['disabled'])
            self.directory_button.state(['disabled'])
            self.crawl_button.state(['disabled'])
    def get_directory_path(self):
        self.directory_path=filedialog.askdirectory()
        print(self.directory_path)
        if len(self.directory_path)!=0:
            self.directory_entry.state(['!disabled'])
            self.directory_entry.delete(0,END)
            self.directory_entry.insert(0,self.directory_path)
            self.directory_entry.state(['disabled'])
            self.crawl_button.state(['!disabled'])

    def crawl_web(self):

        data_collection.directory_path=self.directory_path.replace('\\','/')
        crawl_topics.directory_path=self.directory_path.replace('\\','/')
        data_collection.signal=True
        crawl_topics.signal=True
        data_collection.main(self.window,self.rootwindow)
        #crawl_topics.main(self.window)


    def activate_create(self):
        if self.prerequisites_status.get()==1:
            self.directory_button_create.state(['!disabled'])

            if len(self.directory_entry.get())!=0:
                self.use_crawler_path.state(['!disabled'])
            else:
                self.use_crawler_path.state(['disabled'])


        else:
            self.directory_entry_create.state(['!disabled'])
            self.directory_entry_create.delete(0,END)
            self.directory_entry_create.state(['disabled'])
            self.directory_button_create.state(['disabled'])
            self.create_button.state(['disabled'])
            self.use_crawler_path.state(['disabled'])
            self.use_crawler_path_status.set(0)

    def get_crawler_path(self):
        if self.use_crawler_path_status.get()==1:
            self.directory_path_create=self.directory_path
            self.directory_button_create.state(['disabled'])
            self.directory_entry_create.state(['!disabled'])
            self.directory_entry_create.delete(0,END)
            self.directory_entry_create.insert(0,self.directory_path_create)
            self.directory_entry_create.state(['disabled'])
            self.create_button.state(['!disabled'])
            query_parse.directory_path=self.directory_path_create
            #self.create_progress.config(maximum=query_parse.get_progress_len())
        else:
            self.directory_path_create=''
            self.directory_button_create.state(['!disabled'])
            self.create_button.state(['disabled'])
    def get_directory_path_create(self):
        self.directory_path_create=filedialog.askdirectory()
        print(self.directory_path_create)
        #if len(self.directory_entry_create.get())!=0:
        self.directory_entry_create.state(['!disabled'])
        self.directory_entry_create.delete(0,END)
        self.directory_entry_create.insert(0,self.directory_path_create)
        self.directory_entry_create.state(['disabled'])
        self.create_button.state(['!disabled'])
        query_parse.directory_path=self.directory_path_create
        #self.create_progress.config(maximum=query_parse.get_progress_len())

    def create_dataset(self):
        query_parse.directory_path=self.directory_path_create
        print(query_parse.directory_path)
        self.create_button.state(['disabled'])
        #go=query_parse.main(self.window)
        query_parse.neo4j_username=neo4j_username
        query_parse.neo4j_password=neo4j_password
        qp=query_parse.main(self.window,self.rootwindow)
        #sleep(2)
        #print(gp)
       #while gp.is_alive:
            #print('yes')
         #   task=None
        #print('done')
        '''########################
        root_progress=Tk()
        line_count=0
        #global progress_count
        progress_count=DoubleVar()
        #create_progress=ttk.Progressbar(root,length=370,orient=HORIZONTAL,mode='determinate',maximum=getdouble(get_progress_len()),variable=progress_count)
        #create_progress.pack()
        #button=ttk.Button(root,text='Click me')
        #button.pack()
        create_progress=query_parse.progress(root,progress_count,line_count)
        #create_progress.start()
        #create_progress.start()
        #sleep(2)
        len_done=query_parse.get_progress_len()
        create_background=query_parse.data_parser(progress_count,line_count,len_done,create_progress)
        create_background.start()
        print(create_background.is_alive())
        while create_background.is_alive():
            print('in thread')
        #############'''
        #self.window.iconify()
        self.create_button.state(['!disabled'])
def main():
    global root
    root=Tk()
    root.geometry('770x420')
    root.resizable(FALSE,FALSE)
    query_recommender(root)
    root.mainloop()

if __name__=='__main__':main()

