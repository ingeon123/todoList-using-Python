import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

#from db0 import create_table, add_data,view_all_data
conn=sqlite3.connect("testapp.db",check_same_thread=False)
cursor=conn.cursor()

def add_data(task, task_status, task_due_date):
    cursor.execute("INSERT into taskstable values(?,?,?)",(task, task_status, task_due_date))
    conn.commit()
    
def view_all_data():
    cursor.execute('select * from taskstable')
    data=cursor.fetchall()
    return data

def view_unique_data():
    cursor.execute("""select distinct task from taskstable""")
    data = cursor.fetchall()
    return data

def get_task(task):
    cursor.execute(f'select * from taskstable where task="{task}"')
    data=cursor.fetchall()
    return data

def edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date):
    cursor.execute("""
                    update taskstable set task=?, task_status=?, task_due_date=?
                    where task=? and task_status=? and task_due_date=? 
                   """,(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date))
    conn.commit()
    data = cursor.fetchall()
    return data

def delete_data(task):
    cursor.execute("delete from taskstable where task=?",(task,))
    conn.commit()

def main():
    st.title("ToDo App with Streamlit")
    menu=["Create","Read","Update","Delete","About"]
    #사이드 바
    choice=st.sidebar.selectbox("Menu",menu)
    #테이블 생성
    cursor.execute("""
        create table if not exists taskstable(
             task text,
             task_status text,
             task_due_date date                  
        )
                   """)
    
    if choice=="Create":
        st.subheader("Add Items")
        #layout
        col1,col2=st.columns(2)
        with col1:
            task=st.text_area("Task To Do")
        with col2:
            task_status=st.selectbox("Status",["ToDo","Doing","Done"])
            task_due_date=st.date_input("Due Date")
        if st.button("Add Task"):
            add_data(task,task_status, task_due_date)
            cursor.close()
            st.success("Sucessfully Added Data")

    elif choice=="Read":
        st.subheader("View Items")
        result=view_all_data()
        df=pd.DataFrame(result,columns=['Task','Status','date'])
        # 화면을 접어서 안보이게 만들기 누르면 펼쳐짐
        with st.expander('View All Data'):
            st.dataframe(df)
        # st.write(result)
        with st.expander('Task Status'):
            task_df = df['Status'].value_counts().to_frame()
            task_df=task_df.reset_index('Status')
            st.dataframe(task_df)
            p1=px.pie(task_df,names='Status',values="count")
            st.plotly_chart(p1)

    elif choice=="Update":
        st.subheader("Edit/Update Items")
        result=view_all_data()
        df=pd.DataFrame(result,columns=['Task','Status','date'])
        with st.expander('Current Data'):
            st.dataframe(df)
        # st.write(view_unique_data())
        list_of_task=[i[0] for i in view_unique_data()]
        # st.write(list_of_task)
        selected_task = st.selectbox("test to edit",list_of_task)
        st.write(selected_task)
        selcted_result = get_task(selected_task)
        st.write(selcted_result)
        if(selcted_result):
            task=selcted_result[0][0]
            task_status=selcted_result[0][1]
            task_due_date=selcted_result[0][2]

            col1,col2=st.columns(2)
            with col1:
                new_task=st.text_area("Task To Do",task)
            with col2:
                new_task_status=st.selectbox(task_status,["ToDo","Doing","Done"])
                new_task_due_date=st.date_input(task_due_date)
            if st.button("Update Task"):
                edit_task_data(new_task, new_task_status, new_task_due_date, task, task_status, task_due_date)
                cursor.close()
                st.success(f"Sucessfully Update {task} to {new_task}")

    elif choice=="Delete":
        st.subheader("Delete Item")
        result=view_all_data()
        df=pd.DataFrame(result,columns=['Task','Status','date'])
        with st.expander('Current Data'):
            st.dataframe(df)
        list_of_task=[i[0] for i in view_unique_data()]
        selected_task = st.selectbox("test to Delete",list_of_task)
        st.warning(f"Do you want to delete {selected_task}")
        if st.button("Delete task"):
            delete_data(selected_task)
            st.success("Task has been Sucessfully Delete ") 
            new_result = view_all_data()
            new_df = pd.DataFrame(new_result,columns=['Task','Status','date'])
            with st.expander('New Data'):
                st.dataframe(new_df)

    else:
        st.subheader("About")



if __name__ =='__main__':
    main()
    cursor.close()
    conn.close()