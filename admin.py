import streamlit as st
import pandas as pd


# Security
#passlib,hashlib,bcrypt,scrypt
import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def reviews():
	st.header("Mess Reviews Here: ")
	c.execute('Select * from messreview')
	user_result = c.fetchall()
	clean_db = pd.DataFrame(user_result,columns=["Username","Taste","Hygiene","Quantity"])
	st.dataframe(clean_db)
	st.header("Sweepers Review Here: ")
	c.execute('Select * from rateSweepers')
	user_result = c.fetchall()
	clean_db = pd.DataFrame(user_result,columns=["Username","Rating","Suggestion"])
	st.dataframe(clean_db)
	st.header("Laundry Reviews Here: ")
	c.execute('Select * from rateLaundry')
	user_result = c.fetchall()
	clean_db = pd.DataFrame(user_result,columns=["Username","Rate","Timing","Suggestion"])
	st.dataframe(clean_db)


def addStudent():
    st.subheader("Add New Students")
    new_user = st.text_input("Username")
    new_password = st.text_input("PassCode",type='password')
    if st.button("Signup"):
        create_usertable()
        add_userdata(new_user,make_hashes(new_password))
        st.success("You have successfully created a valid Account")
        st.info("Go to Login Menu to login")

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM admintable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""Simple Login App"""

	st.title("Quality Quorum Admin's Page")

	menu = ["Home","Login"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logged In as {}".format(username))

				task = st.selectbox("Task",["Add Students","See All Reviews","Profiles"])
				if task == "Add Students":
					addStudent()
				elif task == "See All Reviews":
					reviews()
			else:
				st.warning("Incorrect Username/Password")


		



if __name__ == '__main__':
	main()
