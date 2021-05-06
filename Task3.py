# -*- coding: utf-8 -*-
"""
Created on Sun May  2 19:08:30 2021

@author: inbar
"""
import json
 
def creat_dict_messages(line_chat,i,conta): #Creates a message dictionary
    text=line_chat[17:].strip("-").split(":")
    flag="Null"
    try:
        line = dict()
        line["datetime"]=line_chat[:17].strip("-")
        if text[0] in conta:
            line["id"]=conta.index(text[0])+1
            print(text[0])
        else:
            flag=text[0]
            line["id"]=i
        line["text"]=text[1].strip("\n")
    except:
        line=False
        
    ret=[line,flag]
    return ret
    
def creat_metadata(line,chat_text): #Creates a metadata dictionary
    meta = dict()
    meta["chat_name"]=line.split('"')[1]
    meta["creation_date"]=line[:17].strip("-")
    meta["num_of_participants"]=0
    creator_phone=line.find("נוצרה על ידי")+len("נוצרה על ידי")
    meta["creator"]=line[creator_phone:].strip("\n")
    return meta
    
def num_par(text):
    counts=dict()
    for line in text :
        counts[line] = counts.get(line[17:].strip("-").split(":")[0], 0) + 1
    return counts

def creat_data(chat_text): #creating the data chat
    the_dict=dict()
    messages = []
    contacts = []
    inde=1
    last_datetime=" "
    for line in chat_text: #For each line, create the dictionary and add it to the list
        this_line=creat_dict_messages(line,inde,contacts)
        if this_line[0]!=False: #If this is a standard message
            messages.append(this_line[0])
            last_datetime= this_line[0]["datetime"]
            if this_line[1]!="Null":
                inde+=1
                contacts.append(this_line[1])
        if "נוצרה על ידי" in line: #If it's a group creation message
            metadata=creat_metadata(line,chat_text)
        if last_datetime[:5] not in line:
            messages[len(messages)-1]["text"]=messages[len(messages)-1]["text"]+" "+line.strip("\n")
            
            
            
    metadata["num_of_participants"]=len(contacts)
    the_dict["messages"]= messages 
    the_dict["metadata"]= metadata
    print(the_dict)
    return(the_dict)


def creat_output(data):    #Create a file with the data
    info = json.dumps(data,ensure_ascii = False)
    file_name=data["metadata"]["chat_name"]+".txt"
    f = open(file_name, "w",encoding= "utf-8")
    f.write(info)
    f.close() 


###  MAIN
#Import text
path_chat_WhatsApp="C:/Users/inbar/Desktop/Third_year/Second_Semester/Knowledge_data_engineering/Task/task3/files/WhatsAppגאונים לכאן.txt"#input("Enter your path:")
chat_text = open(path_chat_WhatsApp,"r",encoding= "utf-8")


data=creat_data(chat_text)
creat_output(data)
chat_text.close()
    
    
    


 