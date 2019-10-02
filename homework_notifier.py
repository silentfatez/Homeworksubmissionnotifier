import smtplib, ssl
import pandas as pd
import sys
import numpy as np
from password import password
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


if len (sys.argv)==2:
    cohort_num=sys.argv[1]
    filename='F'+'0'+cohort_num+'.csv'
elif len(sys.argv)==3:
    cohort_num=sys.argv[1]
    filename=sys.argv[2]
else:
    print('not 2 or 3 arguments given')
    exit()


homework_not_set=True #boolean to check if type of homework is set
Homework_number_not_set=True #boolean to check if homework number is set
is_homework=False
while homework_not_set==True:
    userinput_homework=input('Type of work to update, 1 for Homework, 2 for Mindmap, 3 for Reflection and 4 for Math Modelling')
    if userinput_homework=='1':
        worknumber=input('Homework Number?(From 1 to 10)')
        worknumberint=int(worknumber)
        if worknumberint in range(1,11):
            type_of_homework=f'HW{worknumber}'
            homework_not_set=False
            is_homework=True
        else:
            print('wrong number range')
    elif userinput_homework=='2':
        worknumber=input('Mindmap Number(1 or 2)')
        worknumberint=int(worknumber)
        if worknumberint in range(1,3):
            type_of_homework=f'MM{worknumber}'
            homework_not_set=False
        else:
            print('wrong number range')
    elif userinput_homework=='3':
        worknumber=input('Reflection Number(1 or 2)')
        worknumberint=int(worknumber)
        if worknumberint in range(1,3):
            type_of_homework=f'R{worknumber}'
            homework_not_set=False
        else:
            print('wrong number range')
    elif userinput_homework=='4':
        worknumber=input('Math Modelling Number?(From 1 to 6)')
        worknumberint=int(worknumber)
        if worknumberint in range(1,6):
            type_of_homework=f'MindMap {worknumber}'
            homework_not_set=False
        else:
            print('wrong number range')
    else:
        print('wrong not in range 1 to 4')


df=pd.read_csv(filename)
col_list=[]
for col in df.columns:
    split_col=col.split(' ')
    col_list.append(split_col[0])
selected_index=col_list.index(type_of_homework)
column_of_interest = df.iloc[: , selected_index]
mean=column_of_interest.mean()
median=column_of_interest.median()
min_score=column_of_interest.min()
max_score=column_of_interest.max()
namelist= df.iloc[:,0]
index_empty_cells=np.where(pd.isnull(column_of_interest.values))
list_names_empty=namelist.iloc[(index_empty_cells)].values
if index_empty_cells[0].size==0:
    bad_students='None'
else:
    bad_students=list_names_empty[0]
    if len(list_names_empty)>1:
        if len(list_names_empty)==2:
            bad_students=bad_students+'and '+list_names_empty[1]
        for listnames in list_names_empty[1:]:
            bad_students=bad_students+','+ listnames

port = 465  # For SSL
sender_email = "sender@gmail.com"  # Enter your address
receiver_email = "receiver@gmail.com"  # Enter receiver address
message = MIMEMultipart("alternative")
message["Subject"] = f"Cohort{cohort_num} {type_of_homework} is graded"
message["From"] = sender_email
message["To"] = receiver_email
if is_homework==True:
    text = f"""\
        Cohort {cohort_num} {type_of_homework} has been graded! Hooray.\n
        Here is the mean score: {mean}  \n
        Here is the median score: {median} \n
        Here is the min score: {min_score} \n
        Here is the max score: {max_score} \n
        Here are the students who did not do the work {bad_students}
        """
else:
    text = f"""\
        Cohort {cohort_num} {type_of_homework} has been graded! Hooray.\n
        Here are the students who did not do the work {bad_students}
        """

part1 = MIMEText(text, "plain")


# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
