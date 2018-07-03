import pandas
import pandas as pd
import sklearn
from backend import db_connection2 as db
from backend import db_connection2
import sys

conn, meta, session = db.connect("postgres", "1234", db="luther_survey") #temp2

all = session.query(db.Process_Rate_Flex_Test_User).all()
process1 = all[1]
t_p_o = all[1].task_parameters_obj
print t_p_o.body_of_task
print t_p_o.result
evaluated_content = process1.get_content_produced_by_this_process()
content = []
for i in evaluated_content:
    if i.associated_user == None:
        continue
    if len(i.results) > 0:

        print i
        #print i.associated_user.name
        print i.associated_user.alias
        print i.associated_user.password
        if process1.is_user_content_acceptable(i) == True:
            result = 0
            if i.results == "Issue":
                result = -2
            else:
                result = float(i.results)
            content.append(result)

            #print result.is_completed
import numpy as np

content = np.array(content)
a = pd.DataFrame(data=content.transpose())



l=session.query(db.User).all()
total=0

user_list=[] #name, and if they were successful at basic task
for i in xrange(len(l)):
    if len(l[i].name)>4:
        single_user_stuff=l[i].associated_content

        relevant = [s for s in single_user_stuff]

        if len(relevant)>0:
            if len(relevant)>=3:
                user_list.append([l[i].name,True,len(relevant)])

            elif len(relevant)<2:
                user_list.append([l[i].name,False,len(relevant)])

            else:
                is_fine=False
                first = relevant[0].origin_process.is_user_content_acceptable(relevant[0])
                second = relevant[1].origin_process.is_user_content_acceptable(relevant[1])
                if first and second:
                    is_fine=True
                user_list.append([l[i].name,is_fine,len(relevant)])


        if len(relevant)>0:
            total+=1
            print l[i].name
            print l[i].password
            print relevant
            #print relevant
           # print relevant[0].origin_process.task_parameters_obj.body_of_task
            #print relevant[0]
            print "next"
            #print relevant[1].origin_process.task_parameters_obj.body_of_task
            #print relevant[1]

from string import printable
b="haha"

printable = set(printable)

filter_ascii=lambda words: filter(lambda x: x in printable, words)


print total