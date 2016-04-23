from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from py2neo import *
#import guitry1

neo4j_user_name='neo4j'
neo4j_password='neo4j'
try:
    authenticate("localhost:7474",neo4j_user_name,neo4j_password)
except Exception:
    none=None
global graph
graph=Graph()

class gui:
    def __init__(self,rootwindow):

        #from main############
        self.status_text_count=1.0
        self.state_list=[]
        #state_name=graph.find("State")
        state_match_list=graph.cypher.execute('MATCH(s:State) RETURN s ORDER BY s.state_name')
        #print(state_match_list)
        for state_name in state_match_list:
            self.state_list+=[str(state_name).split('state_name:"')[1].split('"}')[0]]

        self.state_region_dic={}
        for state_name in self.state_list:
            region_list=[]
            region_match_list=graph.cypher.execute('MATCH(s:State{state_name:"'+str(state_name)+'"}) OPTIONAL MATCH(s)-[:CONTAIN]->(r:Region) RETURN r ORDER BY r.name')
            for region_name in region_match_list:
                #print(str(region_name).split('region_name:"')[1].split('"}')[0])
                region_list+=[str(region_name).split('region_name:"')[1].split('"}')[0]]
            self.state_region_dic.update({state_name:region_list})
        #frame_head=ttk.Frame(rootwindow)
        frame_body=ttk.Frame(rootwindow,width=770,height=260)
        self.frame_display=ttk.Frame(rootwindow,height=100,width=770)
        #frame_head.pack(padx=10,pady=10)
        frame_body.place(x=0,y=0)
        self.frame_display.place(x=20,y=260)
        #main_logo=PhotoImage(file='C:/Python Tutorials/pyhton work/data_gov.GIF')
       # label_main_logo=ttk.Label(frame_head)
        #label_main_logo.pack(side=LEFT,anchor='w')
        #label_main_logo.config(image=main_logo.subsample(10,10))
        style=ttk.Style()
        #rootwindow.configure(background='#3b5b6d')
        style.configure('TFrame',)
        style.configure('TLabel',)



        ####






        style.configure('TLabel',font=('Aerial',10))
        if(len(self.state_list)==0):
            self.state_list+=["No data regarding states in the current database"]
        #self.label1=ttk.Label(frame_head,text="HMIS Data Collection",font=("Aerial",18,'bold'))
        #self.label1.pack(side=LEFT)



        ###########TREEVIEW OF THE CURRENT PROCESS STATUS###########

        self.current_selected_status=StringVar()
        self.status_check=ttk.Checkbutton(frame_body,command=self.status_display,text='Click here to hide Details',variable=self.current_selected_status)
        self.status_check.place(x=30,y=230)
        self.current_selected_status.set(1)
        self.status_text=Text(self.frame_display,width=100,height=9,font=('Aerial',10))
        self.status_text.config(state='disabled')
        self.status_text.grid(row=0,column=1,ipadx=3,ipady=3,)
        self.status_text.forget()
        #self.current_selected_status.set('0')
        self.status_scroll=ttk.Scrollbar(self.frame_display,orient=VERTICAL,command=self.status_text.yview)
        self.status_scroll.grid(row=0,column=2,sticky='ns')
        self.status_text.config(yscrollcommand=self.status_scroll.set)
        self.status_scroll.forget()
        self.frame_display.forget()
        ################################################################



        ###########DROPDOWN FOR THE STATE SELECTION PROCESS###########
        label_state=ttk.Label(frame_body,text="State:")
        label_state.place(x=30,y=0)
        self.current_selected_state=StringVar()
        self.state_region_dic.update({'Choose State':"Choose a State first!"})
        #print(self.state_region_dic)
        self.state_list=['Select State'] + self.state_list
        self.state_list_use=[]
        for state in self.state_list:
            state_temp=str.upper(state[0:1])
            flag_under=False
            for char_state in state[1:]:
                if char_state=='_':
                    flag_under=True
                elif flag_under==True:
                    state_temp+=str.upper(char_state)
                    flag_under=False
                else:
                    state_temp+=char_state
            self.state_list_use+=[state_temp]
        print(self.state_list_use)
        self.state_dropdown=ttk.Combobox(frame_body,value=self.state_list,textvariable=self.current_selected_state,width=35)
        self.state_dropdown.place(x=30,y=20)
        self.state_dropdown.set("Select State")
        self.state_dropdown.bind("<Button-1>",self.state_display)
        self.current_state_check=IntVar()
        self.state_check=ttk.Checkbutton(frame_body,text='Done',variable=self.current_state_check,command=self.state_display_check)
        self.state_check.place(x=240,y=45)
        ###############################################################

        
        ###########DROPDOWN FOR THE REGION SELECTION PROCESS###########
        label_region=ttk.Label(frame_body,text="Region:")
        label_region.place(x=30,y=60)
        self.current_selected_region=StringVar()
        self.region_dropdown=ttk.Combobox(frame_body,textvariable=self.current_selected_region,width=35)
        self.region_dropdown.place(x=30,y=80)
        self.region_dropdown.state(['disabled'])
        self.region_dropdown.set("Select Region")
        self.region_dropdown.bind("<Button-1>",self.region_display)
        self.current_region_check=IntVar()
        self.region_check=ttk.Checkbutton(frame_body,text='Done',variable=self.current_region_check,command=self.region_display_check)
        self.region_check.place(x=240,y=105)
        self.region_check.state(['disabled'])
        ################################################################

        
        ###########DROPDOWN FOR THE INDICATOR SELECTION PROCESS###########
        label_indicator=ttk.Label(frame_body,text="Indicator:")
        label_indicator.place(x=300,y=0)
        self.current_selected_indicator=StringVar()
        self.indicator_dropdown=ttk.Combobox(frame_body,textvariable=self.current_selected_indicator,width=70)
        self.indicator_dropdown.place(x=300,y=20)
        self.indicator_dropdown.state(['disabled'])
        self.indicator_dropdown.set("Select Indicator")
        self.indicator_list=[]
        indicator_data=graph.cypher.execute('MATCH(i:Indicator) RETURN i ORDER BY i.name')
        #print(indicator_data)
        for indicator_name in indicator_data:
            #print(indicator_name)
            self.indicator_list+=[str(indicator_name).split(',name:"')[1].split('"')[0]]
        self.indicator_list=["Select Indicator"]+self.indicator_list
        #print(self.indicator_list)
        self.indicator_dropdown.config(value=self.indicator_list)
        self.indicator_dropdown.bind("<Button-1>",self.indicator_display)
        self.current_indicator_check=IntVar()
        self.indicator_check=ttk.Checkbutton(frame_body,text='Done',variable=self.current_indicator_check,command=self.indicator_display_check)
        self.indicator_check.place(x=680,y=45)
        self.indicator_check.state(['disabled'])
        ################################################################


        ###########DROPDOWN FOR THE PARAMETER SELECTION PROCESS###########
        label_parameter=ttk.Label(frame_body,text="Parameter:")
        label_parameter.place(x=300,y=60)
        self.current_selected_parameter=StringVar()
        self.parameter_dropdown=ttk.Combobox(frame_body,textvariable=self.current_selected_parameter,width=70)
        self.parameter_dropdown.place(x=300,y=80)
        self.parameter_dropdown.state(['disabled'])
        self.parameter_dropdown.set("Select Parameter")
        self.parameter_dict={}
        parameter_data=graph.cypher.execute('MATCH(p:Parameter) RETURN p ORDER BY p.name')
        self.status_text.config(state='normal')
        self.status_text.insert(str(self.status_text_count),'****************NEO4J RETURN FOR THE  MATCH OF PARAMETER QUERY**********\n')
        self.status_text.config(state='disabled')
        self.status_text_count+=1
        #print(parameter_data)
        for parameter_name in parameter_data:
            print(parameter_name)
            self.status_text.config(state='normal')
            self.status_text.insert(str(self.status_text_count),'('+str(parameter_name).split('(')[1].split(')')[0]+')'+'\n')
            self.status_text.config(state='disabled')
            self.status_text_count+=1
            self.parameter_name=str(parameter_name).split(',name:"')[1].split('"')[0]
            parameter_sr_NO=str(parameter_name).split('sr_NO:"')[1].split('.')[0]
            update_list=[]
            try:
                #print(self.parameter_dict[self.parameter_sr_NO])
                update_list=self.parameter_dict[parameter_sr_NO]
            except Exception:
                update_list=[]
            if(len(update_list)!=0):
                #print(update_list)
                if self.parameter_name not in update_list:
                   update_list+=[self.parameter_name]
            else:
                update_list=[self.parameter_name]
            self.parameter_dict.update({parameter_sr_NO:update_list})
        self.status_text.config(state='normal')
        self.status_text.insert(str(self.status_text_count),'(*************************END OF NEO4J QUERY RETRIEVAL**************************\n\n')
        self.status_text.config(state='disabled')
        self.status_text_count+=2
        #self.parameter_dict.update{"Select Parameter":self.parameter_list
        #print(self.parameter_dict)
        self.parameter_dropdown.bind("<Button-1>",self.parameter_display)
        self.current_parameter_check=IntVar()
        self.parameter_check=ttk.Checkbutton(frame_body,text='Done',variable=self.current_parameter_check,command=self.parameter_display_check)
        self.parameter_check.place(x=680,y=105)
        self.parameter_check.state(['disabled'])
        ################################################################

        ###########DROPDOWN FOR THE RELATIONSHIP SELECTION PROCESS###########
        label_relationship=ttk.Label(frame_body,text="Relationship:")
        label_relationship.place(x=30,y=120)
        self.current_selected_relationship=StringVar()
        self.relationship_dropdown=ttk.Combobox(frame_body,textvariable=self.current_selected_relationship,width=35)
        self.relationship_dropdown.place(x=30,y=140)
        self.relationship_dropdown.state(['disabled'])
        self.relationship_dropdown.set("Select relationship")
        self.relationship_list=[]
        self.relationship_dropdown.bind("<Button-1>",self.property_hide)
        self.current_relationship_check=IntVar()
        self.relationship_check=ttk.Checkbutton(frame_body,text='Done',variable=self.current_relationship_check,command=self.property_display)
        self.relationship_check.place(x=240,y=165)
        self.relationship_check.state(['disabled'])
        ################################################################



        ###########DROPDOWN FOR THE PARAMETER TYPE SELECTION PROCESS###########
        label_parameter_type=ttk.Label(frame_body,text="Parameter Type:")
        label_parameter_type.place(x=300,y=120)
        self.current_selected_parameter_type=StringVar()
        self.parameter_type_dropdown=ttk.Combobox(frame_body,textvariable=self.current_selected_parameter_type,width=35)
        self.parameter_type_dropdown.place(x=300,y=140)
        self.parameter_type_dropdown.state(['disabled'])
        self.parameter_type_dropdown.set("Select Type")
        self.parameter_type_list=[]
        self.parameter_type_dropdown.bind("<Button-1>",self.property_hide)
        self.current_parameter_type_check=IntVar()
        self.parameter_type_check=ttk.Checkbutton(frame_body,text='Done',variable=self.current_parameter_type_check,command=self.property_display)
        self.parameter_type_check.place(x=680,y=165)
        self.parameter_type_check.state(['disabled'])
        ################################################################


        ###########DROPDOWN FOR THE PROPERTY SELECTION PROCESS###########
        label_property=ttk.Label(frame_body,text="Property:")
        label_property.place(x=30,y=180)
        self.current_selected_property=StringVar()
        self.property_dropdown=ttk.Combobox(frame_body,textvariable=self.current_selected_property,width=40)
        self.property_dropdown.place(x=30,y=200)
        self.property_dropdown.state(['disabled'])
        self.property_dropdown.set("Select Property")
        self.property_list=[]
        self.property_dropdown.bind("<Button-1>",self.button_activate)
        ################################################################

        #########SUBMIT BUTTON#################
        self.submit_button=ttk.Button(frame_body,text='SUBMIT',command=self.value_display)
        self.submit_button.place(x=340,y=200)
        self.submit_button.state(['disabled'])
        ##########################################

        ###########PROPERTY RETRIEVAL TEXTBOX##########
        self.property_value=Text(frame_body)
        self.property_value.insert(1.0,'Property Value')
        self.property_value.config(state='disabled')
        self.property_value.config(height=1,width=15)
        self.property_value.place(x=530,y=200)
        self.property_list=[]
        ################################################################
        self.state_display('<1>')





            #self.indicator_display('<Button-1>')

    '''def relationship_display_check(self):
        task=None
    def parameter_type_display_check(self):
        task =None'''

    def status_display(self):
        if self.current_selected_status.get()=='0':
            #self.status_text.forget()
            self.status_check.config(text='Click here to see Details')
            self.frame_display.place_forget()
        else:
            self.status_check.config(text='Click here to hide Details')
            self.frame_display.place(x=20,y=260)
            self.status_text.grid(row=0,column=0,ipadx=3,ipady=3)
            self.status_text.config(yscrollcommand=self.status_scroll.set)


    def button_activate(self,event):
        if(self.property_dropdown.instate(['!disabled'])):
            #if(self.current_selected_property.get()!='Select Property'):
                self.submit_button.state(['!disabled'])
                if self.property_value.get(1.0,END)!='Property Value\n':
                    self.property_value.config(state='normal')
                    self.property_value.delete(1.0,END)
                    self.property_value.config(state='disabled')
                #self.value_display()
           # else:
            #    self.submit_button.state(['disabled'])
            #    self.value_display()
        else:
            self.submit_button.state(['disabled'])
            self.property_value.config(state='normal')
            self.property_value.replace(1.0,END,'Property Value')
            self.property_value.config(state='disabled')
            #self.value_display()


    def value_display(self):
        #self.property_value.replace('1.0','end','')
        key_value=self.current_selected_property.get()
        if self.current_selected_property.get() not in self.property_list:
            self.property_value.replace('1.0','end','')
            self.property_value.insert(1.0,'Property Value')
            self.property_value.config(state='disabled')
            self.display_info()

        else:
            print(self.property_dict[key_value])
            self.property_value.config(state='normal')
            self.property_value.replace('1.0','end',self.property_dict[key_value])
            self.property_value.config(state='disabled')
            

    def property_hide(self,event):
        if self.current_selected_parameter_type.get() not in self.parameter_type_list:
            self.current_parameter_type_check.set(0)
        if self.current_selected_relationship.get() not in self.relationship_list:
            self.current_relationship_check.set(0)
        self.property_display()
    def property_display(self):
        #if self.relationship_dropdown.instate(['!disabled']) and self.parameter_type_dropdown.instate(['!disabled']):
        if self.current_parameter_type_check.get()==1 and self.current_relationship_check.get()==1:
            if self.current_selected_relationship.get()=="Select Relationship"  or self.current_selected_parameter_type.get()=="Select Type":
                self.property_dropdown.state(['disabled'])
                self.property_dropdown.set("Select Property")
                self.property_list=[]
                self.display_info()
                if self.current_selected_parameter_type.get() not in self.parameter_type_list:
                    self.current_parameter_type_check.set(0)
                if self.current_selected_relationship.get() not in self.relationship_list:
                    self.current_relationship_check.set(0)
                #self.button_activate('<1>')
            else:
                if self.current_selected_relationship.get() not in self.relationship_list or self.current_selected_parameter_type.get() not in self.parameter_type_list:
                    self.display_info()
                    self.property_dropdown.state(['disabled'])
                    self.property_dropdown.set("Select Property")
                    self.display_info()
                    if self.current_selected_parameter_type.get() not in self.parameter_type_list:
                        self.current_parameter_type_check.set(0)
                    if self.current_selected_relationship.get() not in self.relationship_list:
                        self.current_relationship_check.set(0)
                    #self.button_activate('<1>')
                else:
                    self.property_list=[]
                    self.property_dropdown.set("Select Property")
                    property_data=graph.cypher.execute('MATCH(i:Indicator{name:"'+self.current_selected_indicator.get()+'"})-[r:'+self.current_selected_relationship.get()+'{region_name:"'+self.current_selected_region.get()+'",state_name:"'+self.current_selected_state.get()+'"}]->(p:Parameter{name:"'+self.current_selected_parameter.get()+'",parameter_type:"'+self.current_selected_parameter_type.get()+'"}) RETURN r')
                    print('MATCH(i:Indicator{name:"'+self.current_selected_indicator.get()+'"})-[r:'+self.current_selected_relationship.get()+'{region_name:"'+self.current_selected_region.get()+'",state_name:"'+self.current_selected_state.get()+'"}]->(p:Parameter{name:"'+self.current_selected_parameter.get()+'",parameter_type:"'+self.current_selected_parameter_type.get()+'"}) RETURN r')
                    print(property_data)
                    self.property_dict={}
                    property_data=str(property_data).split(self.current_selected_relationship.get()+' {')[1].split("}]")[0]
                    property_data_list=property_data.split(',')
                    print(len(property_data_list))
                    #print(property_data)
                    for property_data_element in property_data_list:
                        property_element=property_data_element.split(":")
                        property_key=property_element[0]
                        #print(property_data)

                        if(property_key=='region_name') or(property_key=='state_name'):
                            #property_data=None
                            continue
                        self.property_list+=[property_key]
                        print(property_key)
                        print(property_data_element)
                        property_value=property_data_element.split('"')[1].split('"')[0].replace("\\"+"r"+"\\"+"n",'')
                        self.property_dict.update({property_key:property_value})
                        print(property_value)
                    print(len(self.property_dict))
                    self.property_dropdown.config(value=self.property_list)
                    self.property_dropdown.state(['!disabled'])
                    #self.button_activate('<1>')
        else:
            self.property_dropdown.state(['disabled'])
            self.property_dropdown.set("Select Property")
            self.button_activate('<1>')


    def parameter_display_check(self):
        if self.current_parameter_check.get()==1:
            if self.current_selected_parameter.get() not in self.parameter_list:
                self.current_parameter_check.set(0)
                self.relationship_dropdown.state(['disabled'])
                self.parameter_type_dropdown.state(['disabled'])
                #self.parameter_display_check()
                self.relationship_check.state(['disabled'])
                self.parameter_type_check.state(['disabled'])
                self.relationship_check.state(['disabled'])
                self.parameter_type_check.state(['disabled'])
                self.relationship_list=[]
                self.parameter_type_list=[]
                #self.property_display('<Button-1>')
                self.display_info()
            else:
                    self.relationship_list=[]
                    self.parameter_type_list=[]
                    self.relationship_dropdown.set('Select Relationship')
                    self.parameter_type_dropdown.set('Select Type')
                    relationship_data=graph.cypher.execute('MATCH(i:Indicator{name:"'+self.current_selected_indicator.get()+'"}),(p:Parameter{name:"'+self.current_selected_parameter.get()+'"}) WITH i,p MATCH(i)-[r{region_name:"'+self.current_selected_region.get()+'",state_name:"'+self.current_selected_state.get()+'"}]->(p) RETURN TYPE(r) ORDER BY TYPE(r)' )
                    type_data=graph.cypher.execute('MATCH(p:Parameter{name:"'+self.current_selected_parameter.get()+'"})  RETURN p.parameter_type ORDER BY p.parameter_type' )
                    #type_data=graph.cypher.execute('MATCH(i:Indicator{name:"'+self.current_selected_indicator.get()+'"}),(p:Parameter{name:"'+self.current_selected_parameter.get()+'"}) WITH i,p MATCH(i)-[r{region_name:"'+self.current_selected_region.get()+'",state_name:"'+self.current_selected_state.get()+'"}]->(p) RETURN r' )
                    print(type_data)
                    self.status_text.config(state='normal')
                    self.status_text.insert(str(self.status_text_count),'****************FOLLOWING IS THE NEO4J RETURN QUERY FOR PARAMETER TYPE************ \n')
                    self.status_text.config(state='disabled')
                    self.status_text_count+=1
                    self.status_text.config(state='normal')
                    self.status_text.insert(str(self.status_text_count),str(type_data)+'\n')
                    self.status_text.config(state='disabled')
                    self.status_text_count+=1
                    #print('MATCH(i:Indicator{name:"'+self.current_selected_indicator.get()+'"}),(p:Parameter{name:"'+self.current_selected_parameter.get()+'"}) WITH i,p MATCH(i)-[r{region_name:"'+self.current_selected_region.get()+'",state_name:"'+self.current_selected_state.get()+'"}]->(p) RETURN TYPE(r)' )
                    print(relationship_data)
                    self.status_text.config(state='normal')
                    self.status_text.insert(str(self.status_text_count),'****************FOLLOWING IS THE NEO4J RETURN QUERY FOR RELATIONSHIP LIST************\n')
                    self.status_text.config(state='disabled')
                    self.status_text_count+=1
                    self.status_text.config(state='normal')
                    self.status_text.insert(str(self.status_text_count),str(relationship_data)+'\n')
                    self.status_text.config(state='disabled')
                    self.status_text_count+=1
                    for relationship in relationship_data:
                        relationship_text=str(relationship).split('-\n')[1].split('\n')[0].strip()
                        if relationship_text not in self.relationship_list:
                            self.relationship_list+=[relationship_text]
                    self.relationship_dropdown.config(value=self.relationship_list)
                    self.relationship_dropdown.state(['!disabled'])
                    self.relationship_check.state(['!disabled'])
                    for type in type_data:
                        type_text=str(type).split('-\n')[1].split('\n')[0].strip()
                        if type_text not in self.parameter_type_list:
                            self.parameter_type_list+=[type_text]
                    self.parameter_type_dropdown.config(value=self.parameter_type_list)
                    self.parameter_type_dropdown.state(['!disabled'])
                    self.parameter_type_check.state(['!disabled'])
                    #self.property_display('<Button-1>')

        else:
            self.current_parameter_type_check.set(0)
            self.current_parameter_check.set(0)
            self.parameter_type_dropdown.set("Select Type")
            self.relationship_dropdown.set('Select Relationship')
            self.parameter_type_dropdown.state(['disabled'])
            self.relationship_dropdown.state(['disabled'])
            self.current_parameter_type_check.set(0)
            self.relationship_check.state(['disabled'])
            self.current_relationship_check.set(0)
            self.parameter_type_check.state(['disabled'])
            #self.parameter_display_check()
            #self.parameter_check.state(['disabled'])

    def parameter_display(self,evet):
        #if(self.parameter_dropdown.instate(['!disabled'])):
           if(self.current_selected_parameter.get()=="Select Parameter"):
                self.status_text.config(state='normal')
                self.status_text.insert(str(self.status_text_count),'*****************SEARCHING THE DATABASE FOR THE PARAMETER LIST*********************\n')
                self.status_text.config(state='disabled')
                self.status_text_count+=1.0
                self.status_text.config(state='normal')
                self.status_text.insert(str(self.status_text_count),'*****************FOLLOWING IS THE LIST OF PARAMETERS CURRENTLY IN DATABASE*************\n')
                self.status_text.config(state='disabled')
                self.status_text_count+=1.0
                self.parameter_list=self.parameter_dict[str(self.current_selected_indicator.get()).split('M')[1].split(' [')[0]]
                for parameter in self.parameter_list:
                    #print('DATA CHECK')
                    self.status_text.config(state='normal')
                    self.status_text.insert(str(self.status_text_count),parameter+'\n')
                    self.status_text.config(state='disabled')
                    self.status_text_count+=1.0
                self.status_text.config(state='normal')
                self.status_text.insert(str(self.status_text_count),'*****************PARAMETER LIST ENDS HERE*************\n\n')
                self.status_text.config(state='disabled')
                self.status_text_count+=2.0
           else:
                self.current_parameter_check.set(0)
                self.parameter_display_check()
           '''else:
                if self.current_selected_parameter.get() not in self.parameter_dict[str(self.current_selected_indicator.get()).split('M')[1].split(' [')[0]]:
                    self.relationship_dropdown.state(['disabled'])
                    self.relationship_dropdown.set("Select Relationship")
                    self.parameter_type_dropdown.state(['disabled'])
                    self.parameter_type_dropdown.set("Select Relationship")
                    self.property_display('<Button-1>')
                    self.display_info()'''


    def indicator_display_check(self):
        if self.current_indicator_check.get()==1:
            if self.current_selected_indicator.get() not in self.indicator_list or self.current_selected_indicator.get()=='Select Indicator':
                self.current_indicator_check.set(0)
                self.parameter_dropdown.state(['disabled'])
                self.parameter_display_check()
                self.parameter_check.state(['disabled'])
                self.display_info()
            else:
                self.parameter_dropdown.state(['!disabled'])
                self.parameter_check.state((['!disabled']))
                #self.parameter_dropdown.set("Select Parameter")
                parameter_sr_NO=str(self.current_selected_indicator.get()).split('M')[1].split(' [')[0]
                self.parameter_dropdown.config(value=self.parameter_dict[parameter_sr_NO])
                self.parameter_dropdown.state(['!disabled'])
                self.parameter_display('<Button-1>')

        else:
            self.current_parameter_check.set(0)
            self.parameter_dropdown.set("Select Parameter")
            self.parameter_dropdown.state(['disabled'])
            self.parameter_display_check()
            self.parameter_check.state(['disabled'])

    def indicator_display(self,event):
        #if(self.indicator_dropdown.instate(['!disabled'])):
            if(self.current_selected_indicator.get()=="Select Indicator"):
                self.status_text.config(state='normal')
                self.status_text.insert(str(self.status_text_count),'*****************SEARCHING THE DATABASE FOR INDICATOR LIST*********************\n')
                self.status_text.config(state='disabled')
                self.status_text_count+=1.0
                self.status_text.config(state='normal')
                self.status_text.insert(str(self.status_text_count),'*****************FOLLOWING IS THE LIST OF INDICATORS CURRENTLY IN DATABASE*************\n')
                self.status_text.config(state='disabled')
                self.status_text_count+=1.0
                for indicator in self.indicator_list:
                    #print('DATA CHECK')
                    self.status_text.config(state='normal')
                    self.status_text.insert(str(self.status_text_count),indicator+'\n')
                    self.status_text.config(state='disabled')
                    self.status_text_count+=1.0
                self.status_text.config(state='normal')
                self.status_text.insert(str(self.status_text_count),'*****************INDICATOR LIST ENDS HERE*************\n\n')
                self.status_text.config(state='disabled')
                self.status_text_count+=2.0
            else:
                self.current_indicator_check.set(0)
                self.indicator_display_check()

                '''if self.current_selected_indicator.get() not in self.indicator_list:
                    self.parameter_dropdown.state(['disabled'])
                    self.parameter_dropdown.set("Select Parameter")
                    self.parameter_display('<Button-1>')'''
    def region_display_check(self):
        if self.current_region_check.get()==1:
            if self.current_selected_region.get() not in self.region_list:
                self.current_region_check.set(0)
                self.indicator_dropdown.state(['disabled'])
                self.indicator_display_check()
                self.indicator_check.state(['disabled'])
                self.display_info()
            else:
                self.indicator_dropdown.state(['!disabled'])
                self.indicator_check.state((['!disabled']))
                self.indicator_display('<Button-1>')
        else:
            self.current_indicator_check.set(0)
            self.indicator_dropdown.set("Select Indicator")
            self.indicator_dropdown.state(['disabled'])
            self.indicator_display_check()
            self.indicator_check.state(['disabled'])

    def region_display(self,event):
        #print(self.current_selected_state.get())
        #if(self.region_dropdown.instate(['!disabled'])):
            state_check=self.current_selected_state.get()
            '''if state_check not in self.state_list:
                self.region_dropdown.set("Select Region")
                self.region_dropdown.state(['disabled'])
                self.region_check.state(['disabled'])
                self.current_state_check.set(0)
                self.display_info()'''
            #else:
             #   self.region_dropdown.config(value=self.state_region_dic[self.current_selected_state.get()])
            if(self.current_selected_region.get()=="Select Region"):
                self.status_text.config(state='normal')
                self.status_text.insert(str(self.status_text_count),'*****************SEARCHING THE DATABASE FOR REGION LISTINGS*********************\n')
                self.status_text.config(state='disabled')
                self.status_text_count+=1.0
                self.status_text.config(state='normal')
                self.status_text.insert(str(self.status_text_count),'*****************FOLLOWING IS THE LIST OF REGIONS CURRENTLY IN DATABASE*************\n')
                self.status_text.config(state='disabled')
                self.status_text_count+=1.0
                self.region_list=self.state_region_dic[state_check]
                for region in self.region_list:
                    self.status_text.config(state='normal')
                    self.status_text.insert(str(self.status_text_count),region+'\n')
                    self.status_text.config(state='disabled')
                    self.status_text_count+=1.0
                    self.status_text.config(state='normal')
                self.status_text.insert(str(self.status_text_count),'*****************REGION LIST ENDS HERE*************\n\n')
                self.status_text.config(state='disabled')
                self.status_text_count+=2.0
                self.region_dropdown.config(value=self.region_list)
            if self.current_region_check.get()==1:
                self.current_region_check.set(0)
                self.region_display_check()
                
                '''else:
                    if self.current_selected_region.get() not in self.region_list:
                        self.indicator_dropdown.set("Select Indicator")
                        self.indicator_dropdown.state(['disabled'])
                        self.indicator_display('<Button-1>')
                    else:
                        self.indicator_dropdown.set("Select Indicator")
                        self.indicator_dropdown.state(['!disabled'])
                        self.indicator_display('<Button-1>')
        else:
            self.indicator_dropdown.state(['disabled'])
            self.indicator_dropdown.set("Select Indicator")
            self.indicator_display('<Button-1>')'''

    def state_display_check(self):
        if self.current_state_check.get()==1:
            if(self.current_selected_state.get() not in self.state_list) or self.current_selected_state.get()=='Select State':
                self.region_dropdown.state(['disabled'])
                self.region_dropdown.set("Select Region")
                self.region_display_check()
                self.region_check.state(['disabled'])
                self.current_state_check.set(0)
                self.display_info()
            else:
                self.region_dropdown.set("Select Region")
                self.region_dropdown.state(['!disabled'])
                self.region_check.state(['!disabled'])
                self.region_display('<Button-1>')
        else:
            self.current_region_check.set(0)
            self.region_dropdown.set("Select Region")
            self.region_dropdown.state(['disabled'])
            self.region_display_check()
            self.region_check.state(['disabled'])



    def state_display(self,event):
        if(self.current_selected_state.get()=="Select State"):
            #self.region_dropdown.state(['disabled'])
            #self.region_dropdown.set("Select Region")
            self.status_text.config(state='normal')
            self.status_text.insert(str(self.status_text_count),'*****************SEARCHING THE DATABASE FOR THE STATE LISTINGS*********************\n')
            self.status_text.config(state='disabled')
            self.status_text_count+=1.0
            self.status_text.config(state='normal')
            self.status_text.insert(str(self.status_text_count),'*****************FOLLOWING IS THE LIST OF STATES CURRENTLY IN DATABASE*************\n')
            self.status_text.config(state='disabled')
            self.status_text_count+=1.0
            for state in self.state_list:
                #print('DATA CHECK')
                self.status_text.config(state='normal')
                self.status_text.insert(str(self.status_text_count),state+'\n')
                self.status_text.config(state='disabled')
                self.status_text_count+=1.0
            self.status_text.config(state='normal')
            self.status_text.insert(str(self.status_text_count),'*****************STATE LIST ENDS HERE*************\n\n')
            self.status_text.config(state='disabled')
            self.status_text_count+=2.0
            #self.region_display('<Button-1>')
        if self.current_state_check.get()==1:
            self.current_state_check.set(0)
            self.state_display_check()


    def display_info(self):
        messagebox.showinfo(title='Incorrect Input',message='The choice entered doesn\'t seem to exits int the database')


def main():
    try:
        authenticate("localhost:7474","neo4j","ultimate")
    except Exception:
        none=None
    global graph
    graph=Graph()
    global state_list
    state_list=[]
    #state_name=graph.find("State")
    state_match_list=graph.cypher.execute('MATCH(s:State) RETURN s ORDER BY s.state_name')
    #print(state_match_list)
    for state_name in state_match_list:
        state_list+=[str(state_name).split('state_name:"')[1].split('"}')[0]]
    #print(state_list)
    global state_region_dic
    state_region_dic={}
    for state_name in state_list:
        region_list=[]
        region_match_list=graph.cypher.execute('MATCH(s:State{state_name:"'+str(state_name)+'"}) OPTIONAL MATCH(s)-[:CONTAIN]->(r:Region) RETURN r ORDER BY r.name')
        for region_name in region_match_list:
            #print(str(region_name).split('region_name:"')[1].split('"}')[0])
            region_list+=[str(region_name).split('region_name:"')[1].split('"}')[0]]
        state_region_dic.update({state_name:region_list})
    #print(state_region_dic)

    rootwindow=Tk()
    rootwindow.geometry('770x420+50+50')
    rootwindow.resizable(False,False)
    rootwindow.title('HMIS DATABASE')
    global frame_head
    global frame_body
    global frame_display
    frame_head=ttk.Frame(rootwindow)
    frame_body=ttk.Frame(rootwindow)
    frame_display=ttk.Frame(rootwindow)
    frame_head.pack(padx=10,pady=10)
    frame_body.pack()
    frame_display.pack()
    #main_logo=PhotoImage(file='C:/Python Tutorials/pyhton work/data_gov.GIF')
    #label_main_logo=ttk.Label(frame_head)
    #label_main_logo.pack(side=LEFT,anchor='nw')
    #label_main_logo.config(image=main_logo)
    global style
    style=ttk.Style()
    #rootwindow.configure(background='#3b5b6d')
    #style.configure('TFrame',background='#3b5b6d')
    #style.configure('TLabel',background='#3b5b6d')
    #state_list=[]
    gui(rootwindow)
    rootwindow.mainloop()
#main()
if __name__=="__main__":main()
