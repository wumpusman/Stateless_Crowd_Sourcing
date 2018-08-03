from backend.db_connection2 import *

conn, meta, session = connect("postgres", "1234", db="match_girl_suggestions") #temp2


print "OK"

names=["ARSIA4TRDJNMP","AD3176YJTD639","A1JJNB108BPMRN","A29GAVKOZCEEXL","A19ER2VMLUO4D6",
       "A30RLMU6S57XR0","A1RE6E3594S2KZ","A3RCNWIPHVUNRZ","A1E8UHTVL7X3IT"]

for name in names:
    the_user=session.query(User).filter(User.name==name)[0]
    print the_user.name
    print len(the_user.associated_content)
    print the_user.associated_content
    print "\n"