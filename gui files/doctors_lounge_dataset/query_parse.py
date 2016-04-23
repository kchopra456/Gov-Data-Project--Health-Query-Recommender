from py2neo import Node,Relationship,Graph,authenticate
import threading
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from time import sleep
neo4j_username=None
neo4j_password=None
try:
    authenticate("localhost:7474",neo4j_username,neo4j_password)
except Exception:
    none=None
graph=Graph()
#graph.cypher.execute('MATCH n optional match(n)-[r]->(),(p)-[r1]-(n) DELETE n,r,p,r1;')
delimiters=[',',';','?','/','-','_','+','=','(',')','|','\\','{','}','[',']',':','!','@','#','$','%','^','&','*','~','`','\"'
            ,', ','; ','? ','/ ','- ','_ ','+ ','= ', '( ',') ','| ','\\ ','{ ','} ','[ ','] ',': ','! ','@ ','# ','$ ','% ','^ ','& ','* ','~ ','` ','\" ']
directory_path='C:/Gov Data Project/gui files/doctors_lounge_dataset'
line_count=0

def get_progress_len():
    try:
        query_data_read=open(directory_path+'/query_file.txt','r')
    except Exception:
        messagebox.showerror(title='Medical Dataset Fault',message='No file having query database was found, the file must be named "query_file.txt"')
        return 0
    query_data_len=0
    query_read='a'
    while(query_read!=''):
        query_read=query_data_read.readline().strip()
        if(query_read!=''):
            query_data_len+=1
    query_data_read.close()
    print(query_data_len)
    return query_data_len


class data_parser(threading.Thread):
    def __init__(self,progress,top_root,root,rootwindow):
        threading.Thread.__init__(self)
        print('node')
        self.rootwindow=rootwindow
        self.main_root=root
        self.top_root=top_root
        self.done_button=ttk.Button(top_root,text='Complete!',command=self.done_display)
        self.done_button.grid(row=1,column=1,pady=30)
        self.done_button.state(['disabled'])
        close_button=ttk.Button(top_root,text='Cancel',command=self.close_display)
        close_button.grid(row=1,column=2,pady=30)
        self.progress_count=progress
        self.status_text=StringVar()
        self.status_text.set('beginning query file parser')
        status_label=Label(top_root,textvariable=self.status_text)
        status_label.grid(row=2,column=0,columnspan=3,sticky='sw')

    def run(self):
        global line_count
        self.signal=True
        corrupt_flag=False
        query_data=open(directory_path+'/query_file.txt','r')
        doctors_lounge_node=Node('Forum',forum_name='Doctor\'s Lounge',forum_url='http://www.doctorslounge.com/forums/index.php?sid=fb515ecf7faaccd8b2fdc41367a32b14')
        query=query_data.readline().strip()
        line_count+=1
        #progress_count.set(getdouble(line_count))
        query_number=1
        len_done=get_progress_len()
        while query!='' and self.signal==True:
            if(query=='MAIN HEAD'):
                head_topic=query_data.readline().strip()
                line_count+=1
                self.status_text.set('parsing queries for head topic- '+head_topic+'...')
                #progress_count.set(getdouble(line_count))
                head_topic_url=query_data.readline().strip()
                line_count+=1
               # progress_count.set(getdouble(line_count))
                head_topic_node=Node('Head_Topic',topic=head_topic,head_topic_url=head_topic_url)
                graph.create(head_topic_node)
                graph.create(Relationship(doctors_lounge_node,'BOARD_INDEX',head_topic_node))
                query=query_data.readline().strip()
                if(query=='SUB HEAD'):
                    while((query!='MAIN HEAD') and (query!='')) and self.signal==True:
                        sub_topic=query_data.readline().strip()
                        line_count+=1
                        print(sub_topic)
                        print(line_count)
                        self.progress_count.set(getdouble(line_count))
                        self.status_text.set('parsing sub topic for '+head_topic+'-'+sub_topic+'...')
                        #progress_count.set(getdouble(line_count))
                        if(sub_topic==''):
                            query=''
                            print('here')
                            #self.status_text.set('DATABASE creation complete!')
                            #messagebox.showinfo(title='Database COmpletion',message='Database has been created, please restart the package for the changes to take effect.')
                            continue
                        sub_topic_url=query_data.readline().strip()
                        line_count+=1
                        print(line_count)
                       # progress_count.set(getdouble(line_count))
                        if(sub_topic_url==''):
                            print('DATABASE seems to be corrupted. Collect new dataset!')
                            corrupt_flag=True
                            #self.status_text.set('DATABASE seems to be corrupted. Collect new dataset!')
                            #self.top_root.state('withdrawn')
                            #self.main_root.state('normal')
                            #messagebox.showinfo(title='Corrupt Dataset',message='Databset is corrupted, collect new dataset; cancel the current progress.')
                            query=''
                            continue
                        sub_topic_node=Node('Sub_Topic',topic=sub_topic,sub_topic_url=sub_topic_url)
                        graph.create(sub_topic_node)
                        graph.create(Relationship(head_topic_node,'TOPIC_INDEX',sub_topic_node))
                        query=query_data.readline().strip()
                        line_count+=1
                        #progress_count.set(getdouble(line_count))
                        while((query!='SUB HEAD') and (query!='MAIN HEAD')) and (query!='') and self.signal==True:
                            query_topic=query
                            query_end=None
                            if(query!=''):
                                for symbol in delimiters:
                                    query=query.replace(symbol,' ').replace('  ',' ').strip()
                                #print(query)
                                text=[query.split(' ')]
                                #print(text)
                                word_text=[]
                                for words in text:
                                    #print(str.lower(str(words)))
                                    #print(words)
                                    #previous_refernce=None
                                    previous_word=''
                                    words[-1]=words[-1].replace('.','')
                                    for word in words:
                                        word=str.lower(str(word))
                                        #print(word)
                                        graph.cypher.execute('MERGE(w:Word{name:"'+word+'"}) ON CREATE SET w.query_index=['+str(query_number)+'] ON MATCH SET w.query_index=w.query_index+['+str(query_number)+']')
                                        if(word==str.lower(str(words[0]))):
                                            query_begin=graph.find_one('Word','name',word)
                                            #print(query_begin)
                                            graph.create(Relationship(sub_topic_node,'QUERY_INDEX',query_begin))
                                        if(previous_word!=''):
                                            #new_refernce=graph.find_one('Word','name',word)
                                            graph.cypher.execute('MATCH(w1:Word{name:"'+previous_word+'"}),(w2:Word{name:"'+word+'"}) WHERE w1<>w2'
                                                                    ' WITH w1,w2 MERGE(w1)-[r:NEXT]->(w2) ON MATCH SET r.count=r.count+1 ON CREATE SET r.count=0')
                                        previous_word=word
                                        query_end=graph.find_one('Word','name',word)
                            #print(query_topic)
                            query_topic_url=query_data.readline().strip()
                            line_count+=1
                           # progress_count.set(getdouble(line_count))
                            if(query_topic_url==''):
                                print('DATABASE seems to be corrupted. Collect new dataset!')
                                corrupt_flag=True
                                #self.status_text.set('DATABASE seems to be corrupted. Collect new dataset!')
                                #self.top_root.state('withdrawn')
                                #elf.main_root.state('normal')
                                #messagebox.showinfo(title='Corrupt Dataset',message='Databset is corrupted, collect new dataset; cancel the current progress.')
                                query=''
                                continue
                            query_topic_node=Node('Query_Topic',query=query_topic,query_url=query_topic_url,head_topic=head_topic,sub_topic=sub_topic,forum_name='Doctor\'s Lounge',query_index=query_number,query_rank=0)
                            graph.create((query_topic_node))
                            graph.create(Relationship(query_end,'QUERY_INDEX',query_topic_node))
                            query_number+=1
                            query=query_data.readline().strip()
                            line_count+=1
                            self.progress_count.set(getdouble(line_count))
                            print(line_count)
                            #print(self.progress_count.get())
                           # progress.
        if line_count>=len_done and not corrupt_flag:
                print('Thread complete')
                self.done_button.state(['!disabled'])
                line_count=0
        else:
                print('Thread Stopped')
                self.status_text.set('DATABASE seems to be corrupted. Collect new dataset!')
                #self.top_root.state('withdrawn')
                #self.main_root.state('normal')
                #messagebox.showinfo(title='Corrupt Dataset',message='Databset is corrupted, collect new dataset; cancel the current progress.')
                line_count=0
                #exit()
    def done_display(self):
        print('done')
        self.top_root.state('withdrawn')
        self.rootwindow.state('normal')
        messagebox.showinfo(title='Database Completion',message='Database has been created, please restart the package for the changes to take effect.')


    def close_display(self):
        print('close')
        print(self)
        choice=messagebox.askokcancel(title='Grpah Formation Interrupt',message='This will interrupt the graph formation, may corrupt the dataset! Press "OK" to interrupt.')
        print(choice)
        if choice:
            self.signal=False
            self.top_root.state('withdrawn')
            self.rootwindow.state('normal')
            messagebox.showinfo(title='Corrupt Database',message='You just interrupted the Dataset creation. We recomend not to use this dataset, this package may not work properly.')
def main(root,rootwindow):
        global line_count
        progress_len=get_progress_len()
        if progress_len==0:
            rootwindow.state('normal')
            return
        #global parse_backgroung
        top_root=Toplevel(root)
        top_root.geometry('+400+400')
        top_root.overrideredirect(True)
        top_root.title('Medical Query Dataset')
        progress_count=DoubleVar()

        create_progress1=ttk.Progressbar(top_root,length=370,orient=HORIZONTAL,mode='determinate',maximum=getdouble(progress_len),variable=progress_count)
        create_progress1.grid(row=0,column=0,padx=5,pady=5,columnspan=4)
        parse_background=data_parser(progress_count,top_root,root,rootwindow)
        parse_background.start()
        rootwindow.state('withdrawn')

print(directory_path+'hi')
#data_parser()
#main()
print(directory_path+'hi')
#go()
if '__init'=='__main__':main()