from sklearn.linear_model import LogisticRegression

y=["cat","dog"]
x=[[1,2],[0,1]]

l=LogisticRegression()
l.fit(x,y)
print l.classes_