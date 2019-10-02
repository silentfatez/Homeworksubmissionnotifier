import smtplib, ssl
import pandas as pd
import sys
import numpy as np
from password import password
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#assumption file format is the same
#name arrangement is the same



if len(sys.argv)==4:
    cohort_num=sys.argv[1]
    file1=sys.argv[2]
    file2=sys.argv[3]
    splitname1=file1.split('.')
    splitname2=file2.split('.')
    if splitname1[1]!=('csv') or splitname2[1]!=('csv'):
        print('wrong filename provided, it needs to have .csv extension')
        exit()
else:
    print('needs to have class number as first argument followed by old file and new file')
    exit()

def bad_student_lister():
    namelist= old.iloc[:,0]
    index_empty_cells=np.where(pd.isnull(column_of_interest_new.values))
    if index_empty_cells[0].size==0:
        return 'None'
    list_names_empty=namelist.iloc[(index_empty_cells)].values
    bad_students=list_names_empty[0]
    if len(list_names_empty)>1:
        if len(list_names_empty)==2:
            bad_students=bad_students+'and '+list_names_empty[1]
        for listnames in list_names_empty[1:]:
            bad_students=bad_students+','+ listnames
    return bad_students
def homework_stats():
    mean=column_of_interest_new.mean()
    median=column_of_interest_new.median()
    min_score=column_of_interest_new.min()
    max_score=column_of_interest_new.max()
    return mean,median,min_score,max_score

def message_hw(text,index):
    text += f"""\
        Cohort {cohort_num} {selected_columns} has been {did_it_change_list[index]}! Hooray.\n
        Here is the mean score: {mean}  \n
        Here is the median score: {median} \n
        Here is the min score: {min_score} \n
        Here is the max score: {max_score} \n
        Here are the students who did not do the work {bad_students}\n
        """
    return text



def message_others(text,index):
    text += f"""\
        Cohort {cohort_num} {selected_columns} has been {did_it_change_list[index]}! Hooray.\n
        Here are the students who did not do the work {bad_students}\n
        """
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    return text
old=pd.read_csv(file1)
new=pd.read_csv(file2)
#setup for email
port = 465  # For SSL
sender_email = "sender@gmail.com"  # Enter your address
receiver_email = "receiver@sutd.edu.sg"  # Enter receiver address
message = MIMEMultipart("alternative")
message["From"] = sender_email
message["To"] = receiver_email
changed_list=[]
did_it_change_list=[]
col_list=[]
text=''
for cols in old.columns:
    split_col=cols.split('[')
    col_list.append(split_col[0][:-1])
interested_list=['HW','MM','Mindmap','R']
items_to_remove=['Mindmap','HW_Cerebry','Reflection']#requires manual intervention
col_of_interest=[]
for col in col_list:
    for items in interested_list:
        if col[:len(items)]==items:
            col_of_interest.append(col)
for item in items_to_remove:
    col_of_interest.remove(item)
index=0
for selected_columns in col_of_interest:
    selected_index=col_list.index(selected_columns)
    column_of_interest_old = old.iloc[: , selected_index]
    column_of_interest_new = new.iloc[: , selected_index]

    if (column_of_interest_old.isnull().sum()!=len(column_of_interest_old)):
        changes='changed'
    else:
        changes='graded'
    did_it_change_list.append(changes)
    if pd.Series.equals(column_of_interest_old,column_of_interest_new)==0:
        changed_list.append(selected_columns)
        if 'HW' in selected_columns:
            mean,median,min_score,max_score=homework_stats()
            bad_students=bad_student_lister()
            text=message_hw(text,index)
        else:
            bad_students=bad_student_lister()
            text=message_others(text,index)
    index+=1
# Create secure connection with server and send email
if len(changed_list)==1:
    message["Subject"] = f"Cohort{cohort_num} {column_of_interest[1]}  is graded"
else:
    list_of_work=''
    for selected_column in changed_list:
        list_of_work+=selected_column+', '
    message["Subject"] = f"Cohort {cohort_num}  {list_of_work[:-2]} is graded"
part2 = MIMEText(text, "plain")
# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part2)
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
