__author__ = 'Isha Sethi'
from py2neo import Node,Relationship,Graph,authenticate
from tkinter import END
from tkinter import IntVar
#from file:///C:/Python Tutorials/pyhton work/gov_data import parameter_dict.py
graph=Graph()
neo4j_username=None
neo4j_password=None
try:
    authenticate("localhost:7474",neo4j_username,neo4j_password)
except Exception:
    none=None
file_download_count=0
repositroy_url=None
file_exit_flag=True
count=0
kill_flag=False
#country=Node("Country",country_name="India",label_name="Country")
#graph.create(country)
################################################################################################
def data_parser(region,region_file_name,state,state_name,progress_count):
    file_data=open(repositroy_url+'/'+region_file_name+'.txt','r')
    data_text=file_data.readline()
    #hmis_node=Node("Region",region_name=region,label_name='Region')
    #graph.create(hmis_node)
    graph.cypher.execute('MERGE(r:Region{region_name:"'+region+'",label_name:"Region"})')
    hmis_node=graph.find_one("Region","region_name",region)
    graph.create(Relationship(state,"CONTAIN",hmis_node))
    #===================================
    parameter_dict={'1.1':'Number Under ANC','1.1.1':'Within First Trimester','1.2':'Number Under JSY','1.3':'Number With 3 ANC Check-ups','1.4.1':'Number Given TT1','1.4.2':'Number Given TT2','1.5':'Number Given 100 IFA Tablets','1.6.1':'Number Case Of Hypertension(BP>140/90)','1.6.2':'Number Case Of Eclampsia','1.7.1':'Number Case Of Anaemia(HB<11)','1.7.2':'Number Case Of Severe Anaemia(HB<11)','1.8':'Number Test Case SC Level','2.1.1.a':'Number Conducted At Home and Attended By Trained SBA','2.1.1.b':'Number Conducted At Home and Attended By NON-Trained SBA','2.1.1.c':'Number Conducted At Home and Attended By an SBA','2.1.2':'Number Of Visited Newborns Within 24 Hours','2.1.3':'Number Of Mother Paid JSY Incentive','2.2':'Number Of Deliveries At Public Institutions','2.2.1':'Number Discharged Under 48 Hours','2.2.2.a':'Number Of Mother Paid JSY Incentive','2.2.2.b':'Number Of ASHAs Paid JSY Incentive','2.2.2.c':'Number Of Cases JSY Incentive Paid TO ANMs AWWs','2.3':'Number Of Deliveries at Private institution','2.3.1.a':'Number Of Mother Paid JSY Incentive','2.3.1.b':'Number Of ASHAs Paid JSY Incentive','2.3.1.c':'Number Of Cases JSY Incentive Paid TO ANMs AWWs','3.1.1':'Number Of Caesarean','3.1.2':'Number Of Caesarean','3.1.3':'Number Of Caesarean','3.1.4':'Number Of Caesarean','3.1.5':'Total Number Of Caesarean','3.2':'Number Of Caesarean','4.1.1.a':'Number Of Male Live','4.1.1.b':'Number Of Female Live','4.1.1.c':'Total Number Of Births Live','4.1.2':'Number Of Still','4.1.3':'Number Of Abortions','4.2.1':'Number Of Newborn Weighed','4.2.2':'Number Of Newborn Weighed<2.5kg','4.3':'Number Of Newborn BreastFed<1 Hour','5.1.1':'Number Of Cases With Obstetric Complications at PHCs','5.1.2':'Number Of Cases With Obstetric Complications at CHCs','5.1.3':'Number Of Cases With Obstetric Complications at SDHs','5.1.4':'Number Of Cases With Obstetric Complications at State Owned Institutions','5.1.5':'TotalNumber Of Cases With Obstetric Complications','5.2':'Number Of Cases With Obstetric Complications at Private Institutes','5.3.1':'Number Of Complicated Pregnancies With Antibiotics','5.3.2':'Number Of Complicated Pregnancies With Antihypertensive/Magsulph injection','5.3.3':'Number Of Complicated Pregnancies With Oxytocis','5.3.4':'Number Of Complicated Pregnancies With Blood Transfusion','6.1':'Women Getting Post Partum<48 Hours','6.2':'Women Getting Post Partum 48 hours and 14 days','6.3':'PNC Maternal Complications Attended','7.1.1':'Number Of MTPSs < 12 Weeks','7.1.2':'Number Of MTPSs >12 Weeks','7.1.3':'Total Number Of MTPSs','7.2':'Number Of MTPSs','8.1.a':'Number Of Cases RTI/STI In Males','8.1.b':'Number Of Cases RTI/STI In Females','8.1.c':'Total Number of RTI/STI','8.2':'Number Of Suspected RTI/STI','9.1.1.a':'Number Of NSV','9.1.1.b':'Number Of NSV','9.1.1.b':'Number Of NSV','9.1.1.c':'Number Of NSV','9.1.1.d':'Number Of NSVs','9.1.1.e':'Total Number Of NSVs','9.1.2':'Total Number Of NSVs','9.2.1.a':'Number Of Laparoscopic Sterilizations','9.2.1.b':'Number Of Laparoscopic Sterilizations','9.2.1.c':'Number Of Laparoscopic Sterilizations','9.2.1.d':'Number Of Laparoscopic Sterilizations','9.2.1.e':'Total Number Of Lapascopic Sterilization','9.2.2':'Number Of Laparoscopic Sterilizations','9.3.1.a':'Number Of Mini-lap Sterilizations','9.3.1.b':'Number Of Mini-lap Sterilizations','9.3.1.c':'Number Of Mini-lap Sterilizations','9.3.1.d':'Number Of Mini-lap Sterilizations','9.3.1.e':'Number Of Mini-lap Sterilizations','9.3.2':'Number Of Mini-lap Sterilizations','9.4.1.a':'Number Of Post-Partum Sterilizers','9.4.1.b':'Number Of Post-Partum Sterilizers','9.4.1.c':'Number Of Post-Partum Sterilizers','9.4.1.d':'Number Of Post-Partum Sterilizers','9.4.1.e':'Number Of Post-Partum Sterilizers','9.4.2':'Number  Of IUCD Insertions','9.5.1.a':'Number  Of IUCD Insertions','9.5.1.b':'Number Of IUCD Insertions','9.5.1.c':'Number Of IUCD Insertions','9.5.1.d':'Number Of IUCD Insertions','9.5.1.e':'Number Of IUCD Insertions','9.5.1.f':'Total Number Of IUCD Insertions','9.5.1A':'Number Of Post Partum IUC Insertions','9.5.2':'Number Of IUCD Insertions','9.06':'Number Of IUCD','9.07':'Number Of Oral Pill Cycles Distributed','9.08':'Number Of Condom Pieces Distributed','9.09':'Number Of Centchroman Pills','9.1':'Number Of Contraceptive Pills','9.11.1.a':'Number Of Cases Of Male Sterilization','9.11.1.b':'Number Of Cases Of Female Sterilizations','9.11.2.a':'Number Of Cases Of Male Sterilization','9.11.2.b':'Number Of Cases Of Female Sterilization','9.11.3.a':'Number Of Cases Of Male Sterilization','9.11.3.b':'Number Of Cases Of Female Sterilization','9.12':'Number Of Institutes-NSV Trained  Doctors','10.1.01':'Number Of Infants(0-11 Months Old)','10.1.02':'Number Of Infants(0-11 Months Old)','10.1.03':'Number Of Infants(0-11 Months Old)','10.1.04':'Number Of Infants(0-11 Months Old)','10.1.04A':'Number Of Infants(0-11 Months Old)','10.1.04B':'Number Of Infants(0-11 Months Old)','10.1.04C':'Number Of Infants(0-11 Months Old)','10.1.05':'Number Of Infants(0-11 Months Old)','10.1.06':'Number Of Infants(0-11 Months Old)','10.1.07':'Number Of Infants(0-11 Months Old)','10.1.08':'Number Of Infants(0-11 Months Old)','10.1.09A':'Number Of Infants(Upto 48 Hours Of Age)','10.1.09':'Number Of Infants(0-11 Months Old)','10.1.10':'Number Of Infants(0-11 Months Old)','10.1.11':'Number Of Infants(0-11 Months Old)','10.1.12':'Number Of Infants(0-11 Months Old)','10.1.12B':'Number Of Infants(More Than 16 Months Old)','10.1A':'Number Of Children(9-12 Months Old)','10.1.13.a':'Total Number Of Male Children(9-11 Months Old)','10.1.13.b':'Total Number Of Female Children(9-11 Months Old)','10.1.13.c':'Total Number Of Children(9-11 Months Old)','10.2.1':'Number Of Infants(More Than 16 Months Old)','10.2.2':'Number Of Infants(More Than 16 Months Old)','10.2.3':'Number Of Infants(More Than 16 Months Old)','10.3.1.a':'Total Number Of Male Children(12-23 Months Old)','10.3.1.b':'Total Number Of Female Children(12-23 Months Old)','10.3.1.c':'Total Number Of Children(12-23 Months Old)','10.3.2':'Number Of Children(More Than 5 Years Old)','10.3.3':'Number Of Children(More Than 10 Years Old)','10.3.4':'Number Of Children(More Than 16 Years Old)','10.3.5.a':'Number Of Cases Of Abscess','10.3.5.b':'Number Of Cases Of Death','10.3.5.c':'Number Of Cases Of Complications','10.4.1':'Number Of Immunization Sessions','10.4.2':'Number Of Immunization Sessions','10.4.1':'Number Of Immunization Sessions','10.4.2':'Number Of Immunization Sessions','10.4.3':'Number Of Immunization Sessions(ASHAs Presence)','10.5.1':'Number Of Children(More Than 16 Years Old)','11.1.1':'Number Of Children(9 Months to 5 Years Old)','11.1.2':'Number Of Children(9 Months to 5 Years Old)','11.1.3':'Number Of Children(9 Months to 5 Years Old)','12.1':'Number Of Cases Of Diptheria(Below 5 Years Age)','12.2':'Number Of Cases Of Pertusis(Below 5 Years Age)','12.3':'Number Of Cases Of Tetanus_Neonatarum(Below 5 Years Age)','12.4':'Number Of Cases Of Tetanus(Other Than Neonatarum)(Below 5 Years Age)','12.5':'Number Of Cases Of Polio(Below 5 Years Age)','12.6':'Number Of Cases Of Measles(Below 5 Years Age)','12.7':'Number Of Cases Of Diarrhoea And Dehydration(Below 5 Years Age)','12.8':'Number Of Cases Of Malaria(Below 5 Years Age)','12.9':'Number Of Cases Of Respiratory Infection(Below 5 Years Age)','13.1':'Number Of Patients Operated For Cataract','13.2':'Number Of IOL Implantations','13.3':'Number Of School Children With Refractive Errors','13.4':'Number Of Free Glasses','13.5':'Number Of Eyes Collected Through Eye Donation','13.6':'Number Of corneal Transplant','14.01':'Number Of CHCs Or SDHs Or DH','14.02':'Number Of PHCs(24X7 With Atleast 3 Nurse)','14.03':'Number Of Anganwadi Conducted VHNDs','14.04':'Number Of Facilities Having RKS','14.04':'Number Of RKS Meeting(Month)','14.05':'Number Of RKS Meetings','14.06':'Numbre Of Facilities RFS','14.07':'Number Of TImes Ambulance Used(Month)','14.08':'Number Of Institutes With SNCU','14.09':'Number Of Functional Laproscopes In CHC/SDH/DH','14.10.1.a':'Number Of Male Patient','14.10.1.b':'Number Of Female Patient','14.10.1.c':'Total Number Of Patient','14.10.2.a':'Number Of Cases Of Death Male(Inpatient)','14.10.2.b':'Number Of Cases Of Death Female(Inpatient)','14.10.2.c':'Number Of Cases Of Death(Inpatient)','14.11':'Inpatient Head Count At Midnight','14.12.1':'OPD Attendance','14.13.1':'Number Of Operations Using Anaesthesia','14.13.1A':'Gynecology-Hysterectomy Surgeries','14.13.2':'Number Of Operations Without Anaesthesia','14.14.a':'Number Of Patient Given AYUSH Treatment','14.14.b':'Number Of Patients With Dental Procedures','14.14.c':'Number Of Adolescents Counselled','15.1.1.a':'Number Of HBb Test','15.1.1.b':'Number Of Cases With Hb<7gm/dl','15.1.2.a':'Number Of HIV Test On Male','15.1.2.b':'Number Of HIV Test on Women(Non Pregnant Woman)','15.1.2.c':'Number Of HIV Test on Women(Pregnant Woman)','15.1.2.d':'Total Number Of HIV Test','15.2':'Number Of WIDAL Test','15.3.a':'Number Of VDRL Test On Male','15.3.b':'Number Of VDRL On Female(Non Pregnant Woman)','15.3.c':'Number Of VDRL On Female(Pregnant Woman)','15.3.d':'Total Number Of VDRL Test','15.4.1':'Number Of Blood Smears Examined For Malaria','15.4.2':'Number Of Blood Smears test Positive For Plasmodium Vivax','15.4.3':'Number Of Blood Smears test Positive For Plasmodium Falciparum','16.1.1':'DPT Vaccines','16.1.1A':'Pentavalent','16.1.2':'OPV Vaccines','16.1.3':'TT Vaccines','16.1.4':'DT Vaccines','16.1.5':'BCG Vaccines','16.1.6':'Measles Vaccine','16.1.7':'JE Vaccine','16.1.8':'Hepatitis B Vaccine','16.2.1':'IU 380 A','16.2.2':'Condoms','16.2.3':'Oral Contraceptive','16.2.4':'Emergency Contraceptive','16.2.5':'Tubal Rings','16.3.01':'Oxygen Injection','16.3.02':'Gloves','16.3.03':'MVA Syringes','16.3.04':'Fluconazole Tables','16.3.05':'Blood Transfusion Set','16.3.06':'Gluteradehyde Solutiom Of 2% Concentration','16.3.07':'IFA Tablets','16.3.08':'IFA Syrup(Paediatric)','16.3.09':'Paediatric Antibiotics(Cotrimaxozole And Injectable Gentamicin)','16.3.10':'Vitamin A Solution','16.3.11':'ORS(New WHO Formulation)','16.4.1':'Syringes 0.1ml(AD)','16.4.2':'Syringes 0.5ml(AD)','16.4.3':'Syringes 5.0ml(Disposable)','17.1':'Number Of Cases Of Infant Death Within 24 Hours Of Birth','17.2.1':'Number Of Cases Of Infant Death 24 Hours to 4 Weeks-Cause Sepsis','17.2.2':'Number Of Cases Of Infant Death 24 Hours to 4 Weeks-Cause Asphyxia','17.2.3':'Number Of Cases Of Infant Death 24 Hours to 4 Weeks-Cause LBW','17.2.4':'Number Of Cases Of Infant Death 24 Hours to 4 Weeks-Cause Sepsis,Asphyxia And LBW','17.3.1':'Number Of Cases Of Infant Death 1 Month to 5 Years-Cause Pneumonia','17.3.2':'Number Of Cases Of Infant Death 1 Month to 5 Years-Cause Diarrhoea','17.3.3':'Number Of Cases Of Infant Death 1 Month to 5 Years-Cause Fever Related','17.3.4':'Number Of Cases Of Infant Death 1 Month to 5 Years-Cause Measles','17.3.5':'Number Of Cases Of Infant Death 1 Month to 5 Years-Cause Pneumonia,Diarrhoea,Fever Related And Measles','17.4.1':'Number Of Cases Of Adult Death(Above 6 Years)-Cause Diarrhoeal Diseases','17.4.2':'Number Of Cases Of Adult Death(Above 6 Years)-Cause Diarrhoeal Tuberclosis','17.4.3':'Number Of Cases Of Adult Death(Above 6 Years)-Cause Respiratory Diseases Including Infections','17.4.4':'Number Of Cases Of Adult Death(Above 6 Years)-Cause Malaria','17.4.5':'Number Of Cases Of Adult Death(Above 6 Years)-Cause Other Fever Related','17.4.6':'Number Of Cases Of Adult Death(Above 6 Years)-Cause HIV/AIDS','17.4.7':'Number Of Cases Of Adult Death(Above 6 Years)-Cause Heart Disease Or Related To Hypertension','17.4.8':'Number Of Cases Of Adult Death(Above 6 Years)-Cause Neurological Disease Including Strokes','17.4.9(a)':'Number Of Cases Of Maternal Death(15-49 Years)- Cause Abortion','17.4.9(b)':'Number Of Cases Of Maternal Death(15-49 Years)- Cause Obstructed Or Prolonged Labour','17.4.9(c)':'Number Of Cases Of Maternal Death(15-49 Years)- Cause Severe hypertension Or Fits','17.4.9(d)':'Number Of Cases Of Maternal Death(15-49 Years)- Cause Bleeding','17.4.9(e)':'Number Of Cases Of Maternal Death(15-49 Years)- Cause High Fever','17.4.9(f)':'Number Of Cases Of Maternal Death(15-49 Years)- Cause Other Causes','17.4.10':'Number Of Cases Of Adult Death(Above 6 Years)-Cause Trauma Or Accidents Or Burn Cases','17.4.11':'Number Of Cases Of Adult Death(Above 6 Years)-Cause Suicide','17.4.12':'Number Of Cases Of Adult Death(Above 6 Years)-Cause Animal Bites Or Sting','17.4.13(a)':'Number Of Cases Of Adult Death(Above 6 Years)-Cause Known Acute Disease','17.4.13(b)':'Number Of Cases Of Adult Death(Above 6 Years)-Cause Known Chronic Disease','17.4.13(c)':'Number Of Cases Of Adult Death(Above 6 Years)-Cause Not Known'}
    relationship_dict={'1.1':'REGISTERED','1.1.1':'REGISTERED','1.2':'REGISTERED','1.3':'RECEIEVED','1.4.1':'PROVISIONED','1.4.2':'PROVISIONED','1.5':'PROVISIONED','1.6.1':'DETECTED','1.6.2':'MANAGED','1.7.1':'TESTED','1.7.2':'TREATED','1.8':'USED','2.1.1.a':'DELEVERIES_AT_HOME','2.1.1.b':'DELEVERIES_AT_HOME','2.1.1.c':'DELEVERIES_AT_HOME','2.1.2':'DELEVERIES_AT_HOME','2.1.3':'DELEVERIES_AT_HOME','2.2':'DELEVERIES_AT_PUBLIC_INSTITUTIONS','2.2.1':'DELEVERIES_AT_PUBLIC_INSTITUTIONS','2.2.2.a':'DELEVERIES_AT_PUBLIC_INSTITUTIONS','2.2.2.b':'DELEVERIES_AT_PUBLIC_INSTITUTIONS','2.2.2.c':'DELEVERIES_AT_PUBLIC_INSTITUTIONS','2.3':'DELEVERIES_AT_PRIVATE_INSTITUTIONS','2.3.1.a':'DELEVERIES_AT_PRIVATE_INSTITUTIONS','2.3.1.b':'DELEVERIES_AT_PUBLIC_INSTITUTIONS','2.3.1.c':'DELEVERIES_AT_PRIVATE_INSTITUTIONS','3.1.1':'DELEVERIES_AT_PHCs','3.1.2':'DELEVERIES_AT_CHCs','3.1.3':'DELEVERIES_AT_SDHs','3.1.4':'DELEVERIES_AT_PUBLIC_INSTITUTIONS','3.1.5':'DELEVERIES_AT_PUBLIC_INSTITUTIONS','3.2':'DELEVERIES_AT_PRIVATE_INSTITUTIONS','4.1.1.a':'BIRTH','4.1.1.b':'BIRTH','4.1.1.c':'BIRTH','4.1.2':'BIRTH','4.1.3':'BIRTH','4.2.1':'BIRTH','4.2.2':'BIRTH','4.3':'BIRTH','5.1.1':'DELEVERIES_AT_PUBLIC_INSTITUTIONS','5.1.2':'DELEVERIES_AT_PUBLIC_INSTITUTIONS','5.1.3':'DELEVERIES_AT_PUBLIC_INSTITUTIONS','5.1.4':'DELEVERIES_AT_PUBLIC_INSTITUTIONS','5.1.5':'DELEVERIES_AT_PUBLIC_INSTITUTIONS','5.2':'DELEVERIES_AT_PRIVATE_INSTITUTIONS','5.3.1':'TREATED','5.3.2':'TREATED','5.3.3':'TREATED','5.3.4':'TREATED','6.1':'POSTPARTUM','6.2':'POSTPARTUM','6.3':'POSTPARTUM','7.1.1':'CONDUCTED_AT_PUBLIC','7.1.2':'CONDUCTED_AT_PUBLIC','7.1.3':'CONDUCTED_AT_PUBLIC','7.2':'DELEVERIES_AT_PRIVATE','8.1.a':'TREATMENT_INTIATED','8.1.b':'TREATMENT_INTIATED','8.1.c':'TREATMENT_INTIATED','8.2':'CONDUCTED_WET_MOUNT','9.1.1.a':'CONDUCTED_AT_PHCs','9.1.1.b':'CONDUCTED_AT_CHCs','9.1.1.c':'CONDUCTED_AT_SDHs','9.1.1.d':'CONDUCTED_AT_STATE_INSTITUTIONS','9.1.1.e':'CONDUCTED_AT_PUBLIC_INSTITUTIONS','9.1.2':'CONDUCTED_AT_PRIVATE','9.2.1.a':'CONDUCTED_AT_PHCs','9.2.1.b':'CONDUCTED_AT_CHCs','9.2.1.c':'CONDUCTED_AT_SDHs','9.2.1.d':'CONDUCTED_AT_STATE_INSTITUTIONS','9.2.1.e':'CONDUCTED_AT_PUBLIC_INSTITUTIONS','9.2.2':'CONDUCTED_AT_PRIVATE','9.3.1.a':'CONDUCTED_AT_PHCs','9.3.1.b':'CONDUCTED_AT_CHCs','9.3.1.c':'CONDUCTED_AT_SDHs','9.3.1.d':'CONDUCTED_AT_STATE_INSTITUTIONS','9.3.1.e':'CONDUCTED_AT_PUBLIC_INSTITUTIONS','9.3.2':'CONDUCTED_AT_PRIVATE','9.4.1.a':'CONDUCTED_AT_PHCs','9.4.1.b':'CONDUCTED_AT_CHCs','9.4.1.c':'CONDUCTED_AT_SDHs','9.4.1.d':'CONDUCTED_AT_STATE_INSTITUTIONS','9.4.1.e':'CONDUCTED_AT_PUBLIC_INSTITUTIONS','9.4.2':'CONDUCTED_AT_PRIVATE','9.5.1.a':'CONDUCTED_AT_PHCs','9.5.1.b':'CONDUCTED_AT_CHCs','9.5.1.c':'CONDUCTED_AT_SDHs','9.5.1.d':'CONDUCTED_AT_STATE_INSTITUTIONS','9.5.1.e':'CONDUCTED_AT_PUBLIC_INSTITUTIONS','9.5.1.f':'CONDUCTED_AT_PUBLIC_FACILITIES','9.5.1A':'TOTAL','9.5.2':'CONDUCTED_AT_PRIVATE','9.06':'REMOVALS','9.07':'DISTRIBUTED','9.08':'DISTRIBUTED','9.09':'GIVEN','9.1':'DISTRIBUTED','9.11.1.a':'COMPLICATIONS','9.11.1.b':'COMPLICATIONS','9.11.2.a':'FAILURES','9.11.2.b':'FAILURES','9.11.3.a':'DEATHS','9.11.3.b':'DEATHS','9.12':'HAVING','10.1.01':'RECEIEVED_BCG_IMMUNIZATION','10.1.02':'RECEIEVED_DPT1_IMMUNIZATION','10.1.03':'RECEIEVED_DPT2_IMMUNIZATION','10.1.04':'RECEIEVED_DPT3_IMMUNIZATION','10.1.04A':'RECEIEVED_PENTAVALENT1_IMMUNIZATION','10.1.04B':'RECEIEVED_PENTAVALENT2_IMMUNIZATION','10.1.04C':'RECEIEVED_PENTAVALENT3_IMMUNIZATION','10.1.05':'RECEIEVED_OPV0_IMMUNIZATION','10.1.06':'RECEIEVED_OPV1_IMMUNIZATION','10.1.07':'RECEIEVED_OPV2_IMMUNIZATION','10.1.08':'RECEIEVED_OPV3_IMMUNIZATION','10.1.09A':'RECEIEVED_HEPATITIS-B0_IMMUNIZATION','10.1.09':'RECEIEVED_HEPATITIS-B1_IMMUNIZATION','10.1.10':'RECEIEVED_HEPATITIS-B2_IMMUNIZATION','10.1.11':'RECEIEVED_HEPATITIS-B3_IMMUNIZATION','10.1.12':'RECEIEVED_MEASLES_IMMUNIZATION','10.1.12B':'RECEIEVED_MEASLES_IMMUNIZATION','10.1A':'RECEIVED_JE_1st_DOSE','10.1.13.a':'FULLY_IMMUNIZED','10.1.13.b':'FULLY_IMMUNIZED','10.1.13.c':'FULLY_IMMUNIZED','10.2.1':'RECEIEVD_DPT_BOOSTER_DOSE','10.2.2':'RECEIEVED_OPV_BOOSTER_DOSE','10.2.3':'RECEIEVD_MMR_VACCINATION','10.3.1.a':'FULLY_IMMUNIZED','10.3.1.b':'FULLY_IMMUNIZED','10.3.1.c':'FULLY_IMMUNIZED','10.3.2':'GIVEN_DT5','10.3.3':'GIVEN_TT10','10.3.4':'GIVEN_TT16','10.3.5.a':'AEFI','10.3.5.b':'AEFI','10.3.5.c':'AEFI','10.4.1':'PLANNED','10.4.2':'HELD','10.4.3':'HELD','10.5.1':'RECEIEVED_JE_VACCINATION','11.1.1':'ADMINISTERED_VITAMIN_A_DOSE_1','11.1.2':'ADMINISTERED_VITAMIN_A_DOSE_2','11.1.3':'ADMINISTERED_VITAMIN_A_DOSE_3','12.1':'REPORTED','12.2':'REPORTED','12.3':'REPORTED','12.4':'REPORTED','12.5':'REPORTED','12.6':'REPORTED','12.7':'REPORTED','12.8':'REPORTED','12.9':'REPORTED','13.1':'OPERATED','13.2':'IMPLANTATIONS','13.3':'DETECTED','13.4':'PROVISIONED','13.5':'COLLECTED','13.6':'UTILISED','14.01':'FUNCTIONING','14.02':'FUNCTIONING','14.03':'CONDUCTED','14.04':'HAVING','14.05':'HELD','14.06':'HAVING','14.07':'USED','14.08':'HAVING','14.09':'FUNCTIONAL_LAPROSCOPES','14.10.1.a':'ADMITTED','14.10.1.b':'ADMITTED','14.10.1.c':'ADMITTED','14.10.2.a':'DEATH','14.10.2.b':'DEATH','14.10.2.c':'DEATH','14.11':'HEAD_COUNT','14.12.1':'OPD_ATTENDANCE','14.13.1':'MAJOR_OPERATIONS','14.13.1A':'GYNECOLOGY','14.13.2':'MINOR_OPERATIONS','14.14.a':'AYUSH_TREATMENT','14.14.b':'CONDUCTED','14.14.c':'COUNSELLED','15.1.1.a':'CONDUCTED','15.1.1.b':'CONDUCTED','15.1.2.a':'CONDUCTED','15.1.2.b':'CONDUCTED','15.1.2.c':'CONDUCTED','15.1.2.d':'CONDUCTED','15.2':'CONDUCTED','15.3.a':'CONDUCTED','15.3.b':'CONDUCTED','15.3.c':'CONDUCTED','15.3.d':'CONDUCTED','15.4.1':'EXAMIINED','15.4.2':'TESTED_POSITIVE','15.4.3':'TESTED_POSITIVE','16.1.1':'STOCK_POSITION','16.1.1A':'STOCK_POSITION','16.1.2':'STOCK_POSITION','16.1.3':'STOCK_POSITION','16.1.4':'STOCK_POSITION','16.1.5':'STOCK_POSITION','16.1.6':'STOCK_POSITION','16.1.7':'STOCK_POSITION','16.1.8':'STOCK_POSITION','16.2.1':'STOCK_POSITION','16.2.2':'STOCK_POSITION','16.2.3':'STOCK_POSITION','16.2.4':'STOCK_POSITION','16.2.5':'STOCK_POSITION','16.3.01':'STOCK_POSITION','16.3.02':'STOCK_POSITION','16.3.03':'STOCK_POSITION','16.3.04':'STOCK_POSITION','16.3.05':'STOCK_POSITION','16.3.06':'STOCK_POSITION','16.3.07':'STOCK_POSITION','16.3.08':'STOCK_POSITION','16.3.09':'STOCK_POSITION','16.3.10':'STOCK_POSITION','16.3.11':'STOCK_POSITION','16.4.1':'STOCK_POSITION','16.4.2':'STOCK_POSITION','16.4.3':'STOCK_POSITION','17.1':'INFANT_DEATH','17.2.1':'INFANT_DEATH','17.2.2':'INFANT_DEATH','17.2.3':'INFANT_DEATH','17.2.4':'INFANT_DEATH','17.3.1':'INFANT_DEATH','17.3.2':'INFANT_DEATH','17.3.3':'INFANT_DEATH','17.3.4':'INFANT_DEATH','17.3.5':'INFANT_DEATH','17.4.1':'ADULT_DEATH','17.4.2':'ADULT_DEATH','17.4.3':'ADULT_DEATH','17.4.4':'ADULT_DEATH','17.4.5':'ADULT_DEATH','17.4.6':'ADULT_DEATH','17.4.7':'ADULT_DEATH','17.4.8':'ADULT_DEATH','17.4.9(a)':'MATERNAL_DEATH','17.4.9(b)':'MATERNAL_DEATH','17.4.9(c)':'MATERNAL_DEATH','17.4.9(d)':'MATERNAL_DEATH','17.4.9(e)':'MATERNAL_DEATH','17.4.9(f)':'MATERNAL_DEATH','17.4.10':'ADULT_DEATH','17.4.11':'ADULT_DEATH','17.4.12':'ADULT_DEATH','17.4.13(a)':'ADULT_DEATH','17.4.13(b)':'ADULT_DEATH','17.4.13(c)':'ADULT_DEATH'}
    #===================================
    #File that stores the unformated information--------------------
    output_data_text=open('HMIS_unformated_text.txt','w')
    def strcmp(str1,str2):
        if(str1==str2):
            return True
        else:
            return False
    flag_eof=False
    #-----------------------------------------------------------------------------------------------------------------------
    header_list=[]
    final_header_list_temp=[]
    header_list+=data_text.split(',')
    #Gives a list of all the headings in the file, probable Labels:-------------
    for header_text in header_list:
        formated_text=header_text#.split('"')[1].split('"')[0]
        final_header_list_temp+=formated_text.split('\t')
        #print(formated_text)
    count_main_head=len(final_header_list_temp)
    final_header_list=[]
    month_head=None
    for text_head in final_header_list_temp:

        try:
            month_head=text_head.split('Difference-')[1].split(' ')[0]
        except Exception:
            task=None
        if str(text_head)=='Total Reported Facility':
            final_header_list+=[text_head+'_'+str(month_head)]
        else:
            final_header_list+=[text_head]


    print(final_header_list)
    print(len(final_header_list))
    #give the total number of headers in a file:----------------------
    #print(count_main_head)
    #graph.cypher.execute('MATCH (n) OPTIONAL MATCH (n)-[r]-(m) DELETE n,r,m')
    #-----------------------------------------------------------------------------------------------------------------------
   # print(final_header_list)

    #Function to return a list format of the row passed-------

    def list_maker(data_text):
        list_of_values=[]
        list_of_values+=data_text.split('\t')
        formated_list_of_values=[]
        #for value_text in list_of_values:
         #   print(value_text)
          #  formated_list_of_values+=(value_text.split('"')[1].split('"')[0]).split(',')
        return list_of_values

    # Main file being read for data analysis------------

    indicator_node_name='no_name'
    parameter_node_name='no_name'
    parameter_type_name='no_name'
    indicator_node=''
    parameter_node=''
    while not flag_eof:
        temp_data_text=data_text
        new_line=file_data.readline()
        data_text=file_data.readline()
        #print(data_text)
        if not (data_text==''):
            #print(data_text)
            data_text_list=[]
            data_text_list=list_maker(data_text)
            #print(data_text_list)
            if(data_text_list[0]=='\'\n') or(data_text_list[0]=='\'') :
                print("All data has been read\n")
                flag_eof=True
                continue
            indicator=data_text_list[0]#.split('[')[1].split(']')[0]
            #Check if the node has been already made in DATABASE---------Indicator
            if indicator_node_name!=indicator:
                graph.cypher.execute('MERGE(i:Indicator{name:"'+indicator+'",label_name:"'+"Indicator"+'"})')
                indicator_node=graph.find_one('Indicator','name',indicator)
                #indicator_node=Node('Indicator',region,state_name,name=indicator,label_name="Indicator")
                graph.create(Relationship(hmis_node,'RELATES',indicator_node))
            indicator_node_name=indicator

            #list.update({indicator})
            sr_no=data_text_list[1]
           #parameter=data_text_list[2]#.split('"')[1].split('"')[0]
            parameter=parameter_dict[sr_no]
            relationship=relationship_dict[sr_no]
            relationship=relationship.replace('-','_').replace(' ','_')
            #--------------------------------------------
            output_data_text.write(indicator)
            output_data_text.write('\n')
            output_data_text.write(parameter)
            output_data_text.write('\n')
            output_data_text.write(str(data_text_list))
            output_data_text.write('\n')
            #---------------------------------------------
            parameter_type=data_text_list[3]#.split('"')[1].split('"')[0]

            #Check if the node has been already made in DATABASE---------Parameter
            if parameter_node_name!=parameter or parameter_node_name!= parameter_type:
                graph.cypher.execute('MERGE(i:Parameter{name:"'+parameter+'",parameter_type:"'+parameter_type+'",sr_NO:"'+str(sr_no)+'"}) ON CREATE SET i.label_name="Parameter"')
                parameter_node=graph.find_one('Parameter','name',parameter)
                #parameter_node=Node('Parameter',parameter_type,region,state_name,name=parameter,sr_No=sr_no,label_name='Parameter')
                #graph.create(parameter_node)
                #parameter_node=graph.cypher.execute(query,{'parameter_text':parameter})
                #graph.create(parameter_node)
            index_property_list=4
            query=''
            while(index_property_list<count_main_head-1):
                if(data_text_list[index_property_list]!="Na"):
                    query+=str(final_header_list[index_property_list]).replace(' ','_').replace('-','_')+':"'+data_text_list[index_property_list]+'",'
                index_property_list+=1
            if(data_text_list[index_property_list]!="Na"):
                query+=str(final_header_list[count_main_head-1]).replace(' ','_').replace('-','_').replace("\\r\n",'')+':"'+data_text_list[index_property_list]+'"'
            else:
                query=query[0:-1]
            #print('MATCH(i:Indicator{name:"'+indicator+'"})'+',(p:Parameter{name:"'+parameter+'",parameter_type:"'+parameter_type+'",sr_NO:"'+str(sr_no)+'"}) WITH i,p ' +'CREATE(i)-[r:'+relationship+'{state_name:"'+state_name+'",region_name:"'+region+'",'+query+'}]->(p)')
            graph.cypher.execute('MATCH(i:Indicator{name:"'+indicator+'"})'+',(p:Parameter{name:"'+parameter+'",parameter_type:"'+parameter_type+'",sr_NO:"'+str(sr_no)+'"}) WITH i,p ' +'CREATE(i)-[r:'+relationship+'{state_name:"'+state_name+'",region_name:"'+region+'",'+query+'}]->(p)')
            #print(query)
                #batch.AddNodeLabelsJob(parameter_node,parameter_type)
            #graph.create(Relationship(indicator_node,relationship,parameter_node,sr_No=sr_no))
            indicator_node_name=indicator
            parameter_node_name=parameter
            parameter_type_name=parameter_type

                #output_data_text.write(temp_data_text)
                #output_data_text.write('\n')
        else:
            flag_eof=True


    output_data_text.close()
    file_data.close()

#########################################################################################
def main(task_field,task_tree,progress):
    print('here')
    Head_data_file=open(repositroy_url+'/Head_data_file.txt','r')
    state=''
    state_name=''
    task_field.config(state='normal')
    task_field.replace(1.0,END,'Clearing neo4j nodes...')
    task_field.config(state='disabled')
    task_tree.config(state='normal')
    task_tree.replace(1.0,END,'Working...')
    task_tree.config(state='disabled')
    graph.cypher.execute("MATCH(n) OPTIONAL MATCH(n)-[r]->() DELETE n,r")
    global file_exit_flag
    task_field.config(state='normal')
    task_field.replace(1.0,END,'Graph database creation in progress...')
    task_field.config(state='disabled')
    progress_count=IntVar()
    progress.config(mode='determinate',maximum=file_download_count,value=0,variable=progress_count)
    graph.cypher.execute('MERGE(c:Country{country_name:"India",label_name:"Country"})')
    country_name=graph.find_one("Country",'country_name',"India")
    while file_exit_flag and not kill_flag:
        Head_data_read=Head_data_file.readline()
        if(Head_data_read!=''):
            #print(Head_data_read)
            #print(Head_data_read)
            if(Head_data_read=='STATE\n') and not kill_flag:
                Head_data_read=Head_data_file.readline()
                state_name=Head_data_read.replace('\n','')
                task_tree.config(state='normal')
                task_tree.replace(1.0,END,'Updating database for state-'+state_name+'\n')
                task_tree.config(state='disabled')
                print('State-'+state_name)
                #state=Node("State",state_name=state_name,label_name="State")
                #graph.create(state,Relationship(country_name,"CONTAIN",0))
                graph.cypher.execute('MERGE(s:State{state_name:"'+state_name+'",label_name:"State"})')
                state=graph.find_one("State","state_name",state_name)
                graph.create(Relationship(country_name,"CONTAIN",state))
            else:
                if(Head_data_read=='FILE NAME START HERE\n') and not kill_flag:
                    while(Head_data_read!='FILE NAME END HERE\n'):
                        Head_data_read=Head_data_file.readline()
                        if(Head_data_read!='FILE NAME END HERE\n'):
                            region=Head_data_read.replace('\n','')
                            task_tree.config(state='normal')
                            task_tree.insert(END,'Updating region-'+region+'\n')
                            print('Region-'+region)
                            region_file_name=Head_data_file.readline()
                            #print(region)#region_file_name.split('.csv')[0])
                            data_parser(region,region_file_name.split('.csv')[0],state,state_name,progress_count)
                            global count
                            count+=1
                            progress_count.set(count)

                #print('done')
                #Head_data_read=Head_data_file.readline()
        else:
            file_exit_flag=False
        #data_parser(repositroy_url)
    task_field.config(state='normal')
    task_tree.config(state='normal')
    task_field.replace(1.0,END,'Database creation is complete!')
    task_tree.replace(1.0,END,'Database updated!')
    task_field.config(state='disabled')
    task_field.config(state='disabled')
#if __name__=='__main__':main()