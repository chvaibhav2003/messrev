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
def rateMess(user):
	query = ('CREATE TABLE IF NOT EXISTS messreview(username TEXT,taste TEXT,hygiene TEXT,Quantity TEXT)')
	st.header("Rate Your Mess")
	c.execute(query)
	taste = st.selectbox('Rate Taste',('1 Star', '2 Star', '3 Star','4 Star','5 Star'))
	hygiene = st.selectbox('Rate Hygiene',('1 Star', '2 Star', '3 Star','4 Star','5 Star'))
	quantity = st.selectbox('Rate Quantity',('1 Star', '2 Star', '3 Star','4 Star','5 Star'))
	if st.button("Submit Review"):
		c.execute('INSERT INTO messreview(username,taste,hygiene,Quantity) VALUES (?,?,?,?)',(user,taste,hygiene,quantity))
		conn.commit()
		st.success("Data Submitted Successfully")
def rateSweepers(user):
	st.header("Rate Sweepers")
	c.execute('CREATE TABLE IF NOT EXISTS rateSweepers(username TEXT,rate TEXT,suggestion TEXT)')
	rating = st.selectbox('Rate Cleanliness',('1 Star', '2 Star', '3 Star','4 Star','5 Star'))
	suggest = st.text_input("Your Suggestions")
	if st.button("Submit Review"):
		c.execute('INSERT INTO rateSweepers(username,rate,suggestion) VALUES (?,?,?)',(user,rating,suggest))
		conn.commit()
		st.success("Review Sent Successfully!")
def rateLaundry(user):
	st.header("Rate Laundry")
	c.execute('CREATE TABLE IF NOT EXISTS rateLaundry(username TEXT,rate TEXT,timing TEXT,suggestion TEXT)')
	rating=st.selectbox('Rate Cleanliness',('1 Star','2 Star','3 Star','4 Star','5 Star'))
	timing=st.selectbox('Rate timing',('1 Star','2 Star','3 Star','4 Star','5 Star'))
	suggest=st.text_input("Your Suggestion")
	if st.button("Submit Review"):
		c.execute('INSERT INTO rateLaundry(username,rate,timing,suggestion) VALUES (?,?,?,?)',(user,rating,timing,suggest))	
		conn.commit()
		st.success("Review sent successfully!")

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data



def main():
	"""Simple Login App"""

	st.title("Quality Quorum User's Page")

	menu = ["Home","Login"]
	choice = st.sidebar.selectbox("Menu",menu)
	print(choice)

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

			if login_user(username,check_hashes(password,hashed_pswd)):

				st.success(f"Logged In as {username}")

				task = st.selectbox("Task",["Rate Mess Food","Rate Sweepers","Rate Laundry"])
				if task == "Rate Mess Food":
					rateMess(str(username))

				elif task == "Rate Sweepers":
					rateSweepers(str(username))
				elif task == "Rate Laundry":
					rateLaundry(str(username))
					
					
			else:
				st.warning("Incorrect Username/Password")





	elif choice == "SignUp":
		st.subheader("Create New Account")
		new_user = st.text_input("Username")
		new_password = st.text_input("Password",type='password')

		if st.button("Signup"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("You have successfully created a valid Account")
			st.info("Go to Login Menu to login")



if __name__ == '__main__':
	main()