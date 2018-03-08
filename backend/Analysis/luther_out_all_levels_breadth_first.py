import pandas
import pandas as pd
import sklearn
from backend import db_connection2 as db
from backend import db_connection2
import sys

conn, meta, session = db.connect("postgres", "1234", db="sedaris_2") #temp2

all_text_manipulations=session.query(db.Process_Text_Manipulation).all()

top_level=session.query(db.Process_Text_Manipulation).filter(db.Process_Text_Manipulation.id==127).all()[0]
#get result - result.result
result=top_level.get_final_results()[0]
right_node=top_level.task_parameters_obj.context
p_id=top_level.task_parameters_obj.context.process_that_selected_this_content_id
next_level=session.query(db.Process_Text_Manipulation).filter(db.Process_Text_Manipulation.id==p_id).all()[0]

next_right_node=next_level.task_parameters_obj.context

top_level=session.query(db.Process_Text_Manipulation).filter(db.Process_Text_Manipulation.id==127).all()[0]

base_case=[]
base_case.append(top_level)
all_levels=[]
current_case=base_case
while len(current_case)>0:
    all_levels.append(current_case)
    new_list=[]
    for el in current_case:
        left_process=el.task_parameters_obj.body_of_task.process_that_selected_this_content
        right_process=el.task_parameters_obj.context.process_that_selected_this_content



        if left_process!=None:
            new_list.append(left_process)
        if right_process!=None:
            new_list.append(right_process)
        else:
            break
    current_case=new_list

all_results=[]


def recurse_down(parent="NA", el=None):
    if el == None:
        return



    final= str(el.id) #str(el.get_final_results()[0].id)
    recreate=final +" underlying structure"
    recreate=str(parent)+" "+final +" retold"

    all_results.append(recreate)

    left_process = el.task_parameters_obj.body_of_task.process_that_selected_this_content
    right_process = el.task_parameters_obj.context.process_that_selected_this_content

    recurse_down(el.id,left_process)
    recurse_down(el.id,right_process)





    '''
    if el.left process is null and el right process is null
        Do One Extra step of taking result of current task

    STep A For el - alt.result create task where have to write underlying meaning (el.result)
    Step B (parent, el.result + alt.result) -> P (Create process that represents remapping el.result + alt.result )

    recurse Down (el, el.left)
    Step A (el.left) elA
    Step B (el, el.left.result, elA result)

    recurse Down(el, el.right)
    Step A (el.right) erA
    Step B (el, el.right.result, erA)

    For left and right node

    :param el:
    :return:
    '''

recurse_down("NA",top_level)
print all_results
def left_recurse(process,list):

    left_process = process.task_parameters_obj.body_of_task.process_that_selected_this_content
    if left_process !=None:
        list.append(left_process)
        left_recurse(left_process,list)
    else:
        return

list= [top_level]
left_recurse(top_level,list)

#print list

#for i in list:
#    print i.task_parameters_obj.body_of_task.results
#print "OK"
#get children Context and Other

#Add to list of lists
'''
base case [] = Add top level 
all_list=[]
current_case=base_case
while len(current_case) >0:
    all_list.append(current_case)
    new_list=[]
    for i in current_case:
        if i.context.results!=""
            new_list.append(i.context.results)
    
    current_case=new_list
    
'''

print "ready"
for level in all_levels:
    print "Next Level"
    for process in level:
        print process.get_final_results()[0].results  #+ " \n id "+ str(process.id)

#For each element in list
#add children to list
