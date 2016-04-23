from tkinter import *
from tkinter  import ttk
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import Image
import webbrowser
from py2neo import authenticate,Graph
import godgui
import medical_querygui
import medical_querygui
from data_gov import gov_crawlerv1
class base_window:
    def __init__(self,rootwindow):
        self.rootwindow=rootwindow
        self.side_frame_label_list=[]
        self.style=ttk.Style()
        #style.configure('TFrame',anchor='w')
        self.style.configure('TLabel',font=('Aerial',12),anchor='sw')
        self.style.configure('auth.TLabel',font=('Aerial',12),anchor='sw')
        #style.configure()
        self.style.configure('main_theme.TFrame')
        self.style.configure('side_theme.TFrame',background='#78ff78')
        self.style.configure('side_theme.TLabel',font=('Aerial',12),anchor='center',padding=15,background='#78ff78')
        self.style.configure('version_label.TLabel',activebackground='red')
        graph_logo=PhotoImage(file="C:/Gov Data Project/gui files/graphlogo2.gif")
        data_gov_logo=PhotoImage(file='C:/Gov Data Project/gui files/data_gov.gif')
        about=PhotoImage(file='C:/Gov Data Project/gui files/about.gif')
        about_label=ttk.Label(rootwindow,cursor='hand2')
        about_label.about=about
        about_label.config(image=about_label.about)
        about_label.place(x=900,y=0)
        about_label.bind('<1>',self.about_display)

        self.top_side_label=Label(rootwindow,width=190,height=120,anchor='center',background='#54cc54')
        self.side_frame=ttk.Frame(rootwindow,relief=SUNKEN,width=190,height=420,style='side_theme.TFrame')
        self.main_frame=ttk.Frame(rootwindow,width=770,height=420,style='main_theme.TFrame')
        self.top_side_label.graph_logo=graph_logo
        self.top_side_label.config(image=self.top_side_label.graph_logo)
        self.top_label_main_frame=Label(rootwindow,relief=RAISED,width=770,height=80,anchor='e',pady=30,background='#78ff78')
        self.top_label_main_frame.data_gov_logo=data_gov_logo
        self.top_label_main_frame.config(image=self.top_label_main_frame.data_gov_logo)
        #self.side_frame.pack(side=LEFT,fill=Y,expand=True,anchor='w')
        #self.side_frame.grid()
        #self.side_frame.grid_propagate(0)
        self.side_frame.place(x=0,y=120)
        self.top_side_label.place(x=0,y=0)
        self.main_frame.place(x=190,y=120)
        self.top_label_main_frame.place(x=190,y=40)
        #self.main_frame.pack(side=LEFT,fill=BOTH,expand=True)
        #self.main_frame.grid()

        #self.main_label0=ttk.Label(self.main_frame,image=graph_logo,background='Blue')
        #self.main_label0.grid(row=0,column=0,columnspan=10,rowspan=3)
        #side_label0.pack(fill=X)
        self.side_label1=ttk.Label(self.side_frame,text='Neo4j Authentication',width=21,relief=SUNKEN,style='side_theme.TLabel')
        #self.side_label1.configure(image=neo4j_logo)s
        self.side_label2=ttk.Label(self.side_frame,text='Search Dataset',width=21,style='side_theme.TLabel')
        self.side_label3=ttk.Label(self.side_frame,text='Query Locator',width=21,style='side_theme.TLabel')
        self.side_label4=ttk.Label(self.side_frame,text='Create New Dataset',width=21,style='side_theme.TLabel')
        self.side_label_version=ttk.Label(self.side_frame,text='1.2.01',cursor='pirate')

        #self.side_label1.pack(fill=X,ipadx=10,ipady=10)
        self.side_label1.place(x=0,y=0)
        self.side_label1.use=0
        #self.side_label2.pack(fill=X,ipadx=10,ipady=10)
        self.side_label2.place(x=0,y=51)
        self.side_label2.use=0
        #self.side_label3.pack(fill=X,ipadx=10,ipady=10)
        self.side_label3.place(x=0,y=103)
        self.side_label3.use=0
        self.side_label4.place(x=0,y=155)
        self.side_label4.use=0
        self.side_label_version.place(x=50,y=400)
        self.side_frame_label_list+=[self.side_label1]
        self.side_frame_label_list+=[self.side_label2]
        self.side_frame_label_list+=[self.side_label3]
        self.side_frame_label_list+=[self.side_label4]
        self.side_label1.bind('<Enter>',lambda e:self.call_motion('<Enter>',self.side_label1))
        self.side_label1.bind('<Leave>',lambda e:self.call_select('<Leave>',self.side_label1))
        self.side_label2.bind('<Enter>',lambda e:self.call_motion('<Enter>',self.side_label2))
        self.side_label2.bind('<Leave>',lambda e:self.call_select('<Leave>',self.side_label2))
        self.side_label3.bind('<Enter>',lambda e:self.call_motion('<Enter>',self.side_label3))
        self.side_label3.bind('<Leave>',lambda e:self.call_select('<Leave>',self.side_label3))
        self.side_label4.bind('<Enter>',lambda e:self.call_motion('<Enter>',self.side_label4))
        self.side_label4.bind('<Leave>',lambda e:self.call_select('<Leave>',self.side_label4))
        self.side_label1.bind('<1>',lambda e:self.label_click('<1>',self.side_label1))
        self.side_label2.bind('<1>',lambda e:self.label_click('<1>',self.side_label2))
        self.side_label3.bind('<1>',lambda e:self.label_click('<1>',self.side_label3))
        self.side_label4.bind('<1>',lambda e:self.label_click('<1>',self.side_label4))

        self.top_side_label.bind('<Triple-Button-1>',lambda e:self.color_choose('<Triple-Button-1>',self.top_side_label))
        self.top_label_main_frame.bind('<Triple-Button-1>',lambda e:self.color_choose('<Triple-Button-1>',self.top_label_main_frame))
        self.side_frame.bind('<Triple-Button-1>',lambda e:self.color_choose('<Triple-Button-1>',self.side_frame))
        self.neo4j_authentication_flag=False
        self.temp_username=None
        self.temp_password=None
    ##############INITITAL MAIN WINDOW############
        self.neo4j_window('<1>')

    def neo4j_window(self,event):
        global rootwindow
        ###################NEO4J AUTHENTICATION COLLECTION#######################
        label_user_name=ttk.Label(self.main_frame,text='UserName:',width=10,style='auth.TLabel')
        label_password=ttk.Label(self.main_frame,text='Password:',width=10,style='auth.TLabel')
        self.neo4j_user_name_input=StringVar()
        self.neo4j_password_input=StringVar()
        self.entry_user_name=ttk.Entry(self.main_frame,textvariable=self.neo4j_user_name_input,width=25)
        self.entry_password=ttk.Entry(self.main_frame,textvariable=self.neo4j_password_input,show='*',width=25)
        #label_user_name.grid(row=3, column=1,padx=5,pady=5)
        label_user_name.place(x=180,y=120)
        self.entry_user_name.place(x=180,y=150)
        #label_user_name.place(x=400,y=240)
        label_password.place(x=380,y=120)
        self.entry_password.place(x=380,y=150)
        #self.entry_password.place(x=600,y=240)
        button_neo4j_submit=ttk.Button(self.main_frame,text='Submit',command=self.neo4j_authentication)
        button_neo4j_submit.place(x=260,y=230)
        button_neo4j_clear=ttk.Button(self.main_frame,text='Clear',command=self.clear_neo_details)
        button_neo4j_clear.place(x=380,y=230)
        Label(self.main_frame,font=('Aerial',8),bg='white',relief=RAISED,text='This package needs neo4j client actively running in the background for most of the time, and failure of the client can make the package unresponsive.\t\t\n'
                                                            'Please enter the authentication detials for the neo4j server below, only then you\'ll be allowed access to other packages! (Have neo4j configured to port 7474)').place(x=0,y=0)

        if self.neo4j_authentication_flag:
            self.entry_user_name.insert(0,self.temp_username)
            self.entry_password.insert(0,self.temp_password)
    ##############################################################################

    def about_display(self,event):
        about_window=Toplevel(self.rootwindow,height=300,width=250)
        about_window.title('About')
        about_window.resizable(FALSE,FALSE)
        neo4j_logo=PhotoImage(file='C:/Gov Data Project/gui files/neo4j-log2015.gif')
        neo4j_about_label=ttk.Label(about_window,cursor='hand2')
        neo4j_about_label.image_neo=neo4j_logo
        neo4j_about_label.config(image=neo4j_about_label.image_neo)
        neo4j_about_label.place(x=5,y=80)
        neo4j_about_label.bind('<1>',self.neodocs)
        python_logo=PhotoImage(file='C:/Gov Data Project/gui files/python-logo.gif').subsample(2,2)
        python_about_label=ttk.Label(about_window,cursor='hand2')
        python_about_label.image_python=python_logo
        python_about_label.config(image=python_about_label.image_python)
        python_about_label.place(x=70,y=180)
        python_about_label.bind('<1>',self.pythondocs)
        tkinter_logo=PhotoImage(file='C:/Gov Data Project/gui files/tkinter-logo.gif').subsample(2,2)
        tkinter_about_label=ttk.Label(about_window,cursor='hand2')
        tkinter_about_label.image_tkinter=tkinter_logo
        tkinter_about_label.config(image=tkinter_about_label.image_tkinter)
        tkinter_about_label.place(x=50,y=5)
        tkinter_about_label.bind('<1>',self.tkdocs)





    def tkdocs(self,event):
        webbrowser.open_new_tab('http://www.tkdocs.com/')

    def neodocs(self,event):
        webbrowser.open_new_tab('http://neo4j.com/')

    def pythondocs(self,event):
        webbrowser.open_new_tab('https://docs.python.org/3.3/')
    def call_motion(self,event,label):
        print(event)
        label.config(relief=SUNKEN)
    def call_select(self,event,label):
        print(event)
        if label.use!=1:
            label.config(relief=FLAT)

    def label_click(self,event,label):
        if self.neo4j_authentication_flag:
            try:
                    graph=Graph()
                    authenticate('localhost:7474',self.neo4j_user_name_input.get(),self.neo4j_password_input.get())
                    graph.cypher.execute('MATCH n RETURN n LIMIT 1;')
            except Exception:
                    messagebox.showerror(title='Neo4j Authentication',message='Disconnection with client found, login again.')
                    self.neo4j_authentication_flag=False
                    self.neo4j_window('<1>')

        label.config(relief=SUNKEN)
        for side_label in self.side_frame_label_list:
            if(side_label!=label):
                side_label.config(relief=FLAT)
        if(label.use==0):
            self.main_frame.config(padding='0i')
            label.use=1
            self.main_frame.forget
            for widget in self.main_frame.pack_slaves():
                    print(widget.winfo_class())
                    if widget.winfo_class()=='TNotebook':
                        widget.hide(0)
                        widget.hide(0)
                    else:
                        widget.forget()
            for widget in self.main_frame.grid_slaves():
                    print(widget.winfo_class())
                    if widget.winfo_class()=='TNotebook':
                        widget.grid_hide(0)
                        widget.grid_hide(1)
                    else:
                        widget.grid_forget()
            for widget in self.main_frame.place_slaves():
                    print(widget.winfo_class())
                    if widget.winfo_class()=='TNotebook':
                        widget.forget(0)
                        widget.forget(0)
                    else:
                        widget.place_forget()
            self.main_frame.place_forget()
            self.main_frame=ttk.Frame(rootwindow,width=770,height=420,style='main_theme.TFrame')
            self.main_frame.place(x=190,y=120)
            if(label==self.side_label1):
                self.neo4j_window('<1>')
            elif(label==self.side_label2):
                if(label==self.side_label2) and self.neo4j_authentication_flag:
                    neo4j_up=messagebox.askokcancel(title='Neo4j database',message='Please make sure that neo4j client is running with correct database. Else package may not work properly.')
                    if neo4j_up:
                        #self.main_frame.config(padding='0.15i')
                        #messagebox.showinfo(title='Warning',message='In the abscence of neo4j client, package may stop responding! Wait for package to read database!')
                        godgui.gui(self.main_frame)
                    else:
                        self.neo4j_window('<1>')
                        self.label_click('<1>',self.side_label1)
                else:
                    messagebox.showinfo(title='Neo4j Authentication',message='You\'ll first have to fill in authentication details!')
                    self.neo4j_window('<1>')
                    self.label_click('<1>',self.side_label1)
            elif(label==self.side_label3):
                if(label==self.side_label3) and self.neo4j_authentication_flag:
                    neo4j_up=messagebox.askokcancel(title='Neo4j database',message='Please make sure that neo4j client is running with correct database. Else package may not work properly.')
                    if neo4j_up:
                        #messagebox.showinfo(title='Warning',message='In the abscence of neo4j client, package may stop responding!')
                        global rootwindow
                        medical_querygui.query_recommender(self.main_frame,rootwindow)
                    else:
                        self.neo4j_window('<1>')
                        self.label_click('<1>',self.side_label1)
                else:
                    messagebox.showinfo(title='Neo4j Authentication',message='You\'ll first have to fill in authentication details!')
                    self.neo4j_window('<1>')
                    self.label_click('<1>',self.side_label1)
            elif(label==self.side_label4):
                if(label==self.side_label4) and self.neo4j_authentication_flag:
                    gov_crawlerv1.main(self.main_frame)
                else:
                    messagebox.showinfo(title='Neo4j Authentication',message='You\'ll first have to fill in authentication details!')
                    self.neo4j_window('<1>')
                    self.label_click('<1>',self.side_label1)
            for side_label in self.side_frame_label_list:
                if(side_label!=label):
                    side_label.use=0

    def clear_neo_details(self):
        self.entry_user_name.delete(0,END)
        self.entry_password.delete(0,END)
        self.neo4j_authentication_flag=False
    def neo4j_authentication(self):
        if(self.neo4j_user_name_input.get()=='')or(self.neo4j_password_input.get()==''):
            if(self.neo4j_password_input.get()==''):
                messagebox.showerror(title='Neo4j Authentication',message='Password field can not be left blank!')
            else:
                if self.neo4j_user_name_input.get()=='':
                    messagebox.showerror(title='Neo4j Authentication',message='UserName field can not be left blank!')
        else:
            try:
                graph=Graph()
                authenticate('localhost:7474',self.neo4j_user_name_input.get(),self.neo4j_password_input.get())
                graph.cypher.execute('MATCH n RETURN n LIMIT 1;')
                godgui.neo4j_user_name=self.neo4j_user_name_input.get()
                godgui.neo4j_password=self.neo4j_password_input.get()
                medical_querygui.neo4j_username=self.neo4j_user_name_input.get()
                medical_querygui.neo4j_password=self.neo4j_password_input.get()
                gov_crawlerv1.neo4j_username=self.neo4j_user_name_input.get()
                gov_crawlerv1.neo4j_password=self.neo4j_password_input.get()
                print(self.neo4j_user_name_input.get())
                print(self.neo4j_password_input.get())
                self.temp_username=self.neo4j_user_name_input.get()
                self.temp_password=self.neo4j_password_input.get()
                self.neo4j_authentication_flag=True
                messagebox.showinfo(title='Neo4j Authentication',message='Client authentication complete!')
            except Exception:
                messagebox.showerror(title='Neo4j Authentication',message='Authentication with the Neo4j client failed, verify that client is running.\n'
                                                                          'Make sure your details are correct.')
                self.neo4j_authentication_flag=False
            godgui.neo4j_user_name=self.neo4j_user_name_input.get()
            godgui.neo4j_password=self.neo4j_password_input.get()
            medical_querygui.neo4j_username=self.neo4j_user_name_input.get()
            medical_querygui.neo4j_password=self.neo4j_password_input.get()
            gov_crawlerv1.neo4j_username=self.neo4j_user_name_input.get()
            gov_crawlerv1.neo4j_password=self.neo4j_password_input.get()
            print(self.neo4j_user_name_input.get())
            print(self.neo4j_password_input.get())

    def color_choose(self,event,widget):
        color=colorchooser.askcolor()
        print(color)
        print(widget.winfo_class())
        print(self.top_side_label.winfo_name())
        if color[1]!=None:
            if widget.winfo_class()=='TFrame':
                self.style.configure('side_theme.TFrame',background=color[1])
                self.style.configure('side_theme.TLabel',background=color[1])
            if widget.winfo_class()=='Label':
                #if widget.winfo_name()==self.top_side_label.winfo_name():
                    widget.config(background=color[1])
                    print('yes')


def main():
    global rootwindow
    rootwindow=Tk()
    rootwindow.title('Query Package')
    #rootwindow.configure(background='white')
    rootwindow.geometry('960x545')
    rootwindow.resizable('False','False')
    base_window(rootwindow)
    rootwindow.mainloop()

if __name__=='__main__':main()
