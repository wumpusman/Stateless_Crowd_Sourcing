import pandas
import pandas as pd
import sklearn
from backend import db_connection2 as db
from backend import db_connection2
import sys

conn, meta, session = db.connect("postgres", "1234", db="match_girl") #temp2

all_text_manipulations=session.query(db.Process_Text_Manipulation).all()

top_level=session.query(db.Process_Text_Manipulation).filter(db.Process_Text_Manipulation.id==90).all()
#get result - result.result
result=top_level.get_final_results()[0]
right_node=top_level.task_parameters_obj.context
p_id=top_level.task_parameters_obj.context.process_that_selected_this_content_id
next_level=session.query(db.Process_Text_Manipulation).filter(db.Process_Text_Manipulation.id==p_id).all()[0]

next_right_node=next_level.task_parameters_obj.context