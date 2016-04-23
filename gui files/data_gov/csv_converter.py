import csv
from time import sleep
from tkinter import END
from tkinter import IntVar
directory_path=None
file_download_count=0
file_to_convert='file_'
file_count=1
given_chance=0
def main(task_field,task_tree,progress):
    progress_count=IntVar()
    progress.config(mode='determinate',maximum=file_download_count,value=0,variable=progress_count)
    repository_path=directory_path
    global file_count
    global given_chance
    task_field.config(state='normal')
    task_tree.replace(1.0,END,'Converting files...')
    task_field.config(state='disabled')
    while file_count<=file_download_count:
        try:
            task_tree.config(state='normal')
            task_tree.replace(1.0,END,'Working...\n')
            task_tree.config(state='disabled')
            with open(repository_path+'/'+file_to_convert+str(file_count)+'.csv', 'r') as csvfile:
                file_to_create=open(repository_path+'/'+file_to_convert+str(file_count)+'.txt','w')
                file=csv.writer(file_to_create,quotechar='|',delimiter='\t',quoting=csv.QUOTE_NONE)
                spamreader = csv.reader(csvfile)
                #print(spamreader)
                for row in spamreader:
                    #print(row)
                    file.writerow(row)
                print("DONE-"+str(file_count))
            file_count+=1
            progress_count.set(file_count)
        except Exception:

            if(given_chance<3):
                print("Somethng went wrong while processing file-"+str(file_count))
                print('If the file Do not exist ignore the message, or check else database will be corrupted. Converting file-'+str(file_count+1))
                task_tree.config(state='normal')
                task_tree.insert(END,"Somethng went wrong while processing file-"+str(file_count)+'\n')
                task_tree.insert(END,'If the file Do not exist ignore the message, or check else database will be corrupted. Converting file-'+str(file_count+1)+'\n')
                task_tree.config(state='disabled')
                file_count+=1
                given_chance+=1
                sleep(5)

    print("The task is Complete")
    task_field.config(state='normal')
    task_field.replace(1.0,END,'File conversion is complete...')
    task_field.config(state='disabled')
    task_tree.config(state='normal')
    task_tree.replace(1.0,END,'Done!\n')
    task_tree.config(state='disabled')
    file_count=0
