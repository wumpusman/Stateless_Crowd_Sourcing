
import sqlalchemy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, ARRAY, Boolean, DateTime
from sqlalchemy.orm import relationship
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from enum import Enum
from sqlalchemy.orm import backref
from db_connection2 import connect


from db_connection2 import *
#Base=declarative_base()


def addList(session,list):
    for i in list:
        session.add(i)
if __name__ == '__main__':
    conn, meta, session = connect("postgres", "1234", db="Task_Crowd_Source")  # user='postgres', password='1234'
    #Base.metadata.create_all(conn)

    cont1_raw_data=buildContent("I want to be successful. But I don't know how",10,True)
    cont2_prompt=buildContent("Rewrite the following text to make it more depressing",11,True)
    cont3_context=buildContent("",12,True)

    basic_process=Process_Object(body_of_task=cont1_raw_data,prompt=cont2_prompt,context=cont3_context)
    basic_process.id=666
    basic_process.is_locked=False

    for i in xrange(2): #2 results
        text="I want to be successful, but I'm a failure at everything I do"
        id=20+i
        cont=buildContent(text,id,True)
        sub_pr=Process_Rate(body_of_task=cont,prompt=cont2_prompt,context=cont3_context)

        basic_process.get_content_produced_by_this_process().append(cont)

        basic_process.sub_process.append(sub_pr)

    #First sub_process_children
    sub_pr_cont11=buildContent("1",30,True)
    sub_pr_cont12 = buildContent("issue", 31,True)
    sub_pr_cont13=buildContent("2",32,False)

    basic_process.sub_process[0].get_content_produced_by_this_process().append(sub_pr_cont11)
    basic_process.sub_process[0].get_content_produced_by_this_process().append(sub_pr_cont12)
    basic_process.sub_process[0].get_content_produced_by_this_process().append(sub_pr_cont13)

    #Second Sub Process Children
    sub_pr_cont21 = buildContent("5", 33, True)
    sub_pr_cont22 = buildContent("4", 34, True)
    sub_pr_cont23= buildContent("5", 35, False)


    basic_process.sub_process[1].get_content_produced_by_this_process().append(sub_pr_cont21)
    basic_process.sub_process[1].get_content_produced_by_this_process().append(sub_pr_cont22)
    basic_process.sub_process[1].get_content_produced_by_this_process().append(sub_pr_cont23)

    session.add(basic_process)
    print basic_process.select_data_for_analysis(session)
