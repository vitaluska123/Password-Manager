import math
import sqlite3
from tkinter import Tk
import cryptocode

import pyperclip
import customtkinter as CTk
from PIL import Image
from time import perf_counter, perf_counter_ns

CTk.set_appearance_mode("Dark")
CTk.set_default_color_theme("blue")

conn = sqlite3.connect('passwords.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Passwords(Num INT,For TEXT,Login TEXT,Password TEXT, Mail TEXT, Description TEXT);")
conn.commit()
cur.execute("SELECT Num FROM Passwords;")
Num_count = len(cur.fetchall())
cur.close()
conn.close()

conn = sqlite3.connect('passwords.db')
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Settings(LANGUAGE TEXT);")
conn.commit()
cur.execute("SELECT LANGUAGE FROM Settings;")
Language = cur.fetchall()
cur.close()
conn.close()
page = 0
inpage = 4
dbdata = 0
password = ""
updateDB = False
logs = [[0]*3]*Num_count


#*			--------view-------
class ViewPass(CTk.CTk):
	def __init__(self):
		super().__init__()
		self.geometry("630x300")
		self.title("ViewPass")
		self.resizable(False,False)
		self.main_Frame = CTk.CTkFrame(master=self,fg_color="#343a40")
		self.main_Frame.grid(row=0,column=0,sticky="nsew",padx=(5,5),pady=(5,5))
		
	Num = 0
	def addinBufM(self):
		global dbdata
		pyperclip.copy(dbdata[3])

	def addinBufL(self):
		global dbdata
		pyperclip.copy(dbdata[1])

	def addinBufP(self):
		global dbdata
		pyperclip.copy(dbdata[2])

	def addNum(self,Num):
		conn = sqlite3.connect('passwords.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS Passwords(Num INT,For TEXT,Login TEXT,Password TEXT, Mail TEXT, Description TEXT);")
		conn.commit()
		global dbdata
		data = cur.execute("SELECT For, Login, Password, Mail, Description FROM Passwords WHERE Num == ?",(Num,)).fetchone()
		dbdata = data
		global password
		self.For_label = CTk.CTkLabel(master=self.main_Frame,text=f"- {cryptocode.decrypt(data[0],password)} -",font=CTk.CTkFont(size=30, weight="bold"),width=620)
		self.For_label.grid(row=0,column=0,columnspan=2,padx=(5,5),pady=(5,5))

		self.Mail_label = CTk.CTkLabel(master=self.main_Frame,text="Mail:",font=CTk.CTkFont(size=20, weight="bold"),width=130)
		self.Mail_label.grid(row=1,column=0,padx=(5,5),pady=(5,5))
		self.Mail_Button = CTk.CTkButton(master=self.main_Frame,text=cryptocode.decrypt(data[3],password),fg_color="transparent",width=470,command=self.addinBufM)
		self.Mail_Button.grid(row=1,column=1,padx=(5,5),pady=(5,5))

		self.Login_label = CTk.CTkLabel(master=self.main_Frame,text="Login:",font=CTk.CTkFont(size=20, weight="bold"),width=130)
		self.Login_label.grid(row=2,column=0,padx=(5,5),pady=(5,5))
		self.Login_Button = CTk.CTkButton(master=self.main_Frame,text=cryptocode.decrypt(data[1],password),fg_color="transparent",width=470,command=self.addinBufL)
		self.Login_Button.grid(row=2,column=1,padx=(5,5),pady=(5,5))

		self.Pass_label = CTk.CTkLabel(master=self.main_Frame,text="Password:",font=CTk.CTkFont(size=20, weight="bold"),width=130)
		self.Pass_label.grid(row=3,column=0,padx=(5,5),pady=(5,5))
		self.Pass_Button = CTk.CTkButton(master=self.main_Frame,text=cryptocode.decrypt(data[2],password),fg_color="transparent",width=470,command=self.addinBufP)
		self.Pass_Button.grid(row=3,column=1,padx=(5,5),pady=(5,5))

		self.Description_label = CTk.CTkLabel(master=self.main_Frame,text="Description:",font=CTk.CTkFont(size=20, weight="bold"),width=130)
		self.Description_label.grid(row=4,column=0,columnspan=2,padx=(5,5),pady=(5,5))
		self.Description_Button = CTk.CTkLabel(master=self.main_Frame,text=cryptocode.decrypt(data[4],password),fg_color="transparent",width=470,height=80)
		self.Description_Button.grid(row=5,column=0,columnspan=2,padx=(5,5),pady=(5,5))




#*			-------Settings-------
class Settings(CTk.CTk):
	def __init__(self):
		super().__init__()
		self.geometry("430x400")
		self.title("Settings")
		self.resizable(False,False)
		self.main_Frame = CTk.CTkFrame(master=self,fg_color="#343a40")
		conn = sqlite3.connect('passwords.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS Settings(LANGUAGE TEXT);")
		conn.commit()
		optionmenu_var = CTk.StringVar(value="English")

		self.Settings_Frame = CTk.CTkFrame(master=self, fg_color="#343a40")
		self.Settings_Frame.grid(row=0,column=0,sticky="nsew",padx=(5,5),pady=(5,5))

		self.Title = CTk.CTkLabel(master=self.Settings_Frame,text="-Settings-",font=CTk.CTkFont(size=20, weight="bold"))
		self.Title.grid(row=0,column=0,columnspan=2,sticky="nsew",padx=(5,5),pady=(5,5))

		
		self.Language_Title = CTk.CTkLabel(master=self.Settings_Frame,text="Language:",width=260)
		self.Language_Title.grid(row=1,column=0,sticky="nsew",padx=(5,5),pady=(5,5))

		self.Language = CTk.CTkOptionMenu(master=self.Settings_Frame,values=["English", "Russian"],
                                       command=self.optionmenu_callback,
                                       variable=optionmenu_var)
		self.Language.grid(row=1,column=1,sticky="nsew",padx=(5,5),pady=(5,5))

	def optionmenu_callback(self,choice):
		print("optionmenu dropdown clicked:", choice)


#*			-------Окно с добавлением пороля-------
class Pass(CTk.CTk):
	def __init__(self):
		super().__init__()
		self.geometry("430x300")
		self.title("Add Password")
		self.resizable(False,False)

		self.passAdd = CTk.CTkFrame(master=self, fg_color="#343a40")
		self.passAdd.grid(row=0,column=0,sticky="nsew",padx=(5,5),pady=(5,5))

		self.text = CTk.CTkLabel(master=self.passAdd,text="Pass for:",width=130,font=CTk.CTkFont(size=20))
		self.text.grid(row=0,column=0,padx=(5),pady=(5))

		self.text1 = CTk.CTkLabel(master=self.passAdd,text="Login:",width=130,font=CTk.CTkFont(size=20))
		self.text1.grid(row=1,column=0,padx=(5),pady=(5))

		self.text2 = CTk.CTkLabel(master=self.passAdd,text="Password:",width=130,font=CTk.CTkFont(size=20))
		self.text2.grid(row=2,column=0,padx=(5),pady=(5))

		self.text3 = CTk.CTkLabel(master=self.passAdd,text="mail:",width=130,font=CTk.CTkFont(size=20))
		self.text3.grid(row=3,column=0,padx=(5),pady=(5))
		self.text3 = CTk.CTkLabel(master=self.passAdd,text="description:",width=130,font=CTk.CTkFont(size=20))
		self.text3.grid(row=4,column=0,columnspan=2,padx=(5),pady=(5))


		self.e = CTk.CTkEntry(master=self.passAdd,width=270)
		self.e.grid(row=0,column=1,padx=(5),pady=(5))

		self.e1 = CTk.CTkEntry(master=self.passAdd,width=270)
		self.e1.grid(row=1,column=1,padx=(5),pady=(5))

		self.e2 = CTk.CTkEntry(master=self.passAdd,width=270)
		self.e2.grid(row=2,column=1,padx=(5),pady=(5))

		self.e3 = CTk.CTkEntry(master=self.passAdd,width=270)
		self.e3.grid(row=3,column=1,padx=(5),pady=(5))

		self.e4 = CTk.CTkEntry(master=self.passAdd,width=400,height=50,border_color="#565b5e",border_width=2)
		self.e4.grid(row=5,column=0,columnspan=2,padx=(5),pady=(5))

		self.add_button = CTk.CTkButton(master=self.passAdd,text="Add",width=200,font=CTk.CTkFont(size=20, weight="bold"),command=self.addPass)
		self.add_button.grid(row=6,column=0,columnspan=2,padx=(5),pady=(5))

	def addPass(self):
		global password
		conn = sqlite3.connect('passwords.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS Passwords(Num INT,For TEXT,Login TEXT,Password TEXT, Mail TEXT, Description TEXT);")
		conn.commit()
		
		cur.execute("SELECT Num FROM Passwords;")
		Num_count = len(cur.fetchall())
		PassToAdd = (Num_count+1,cryptocode.encrypt(self.e.get(),password),cryptocode.encrypt(self.e1.get(),password),cryptocode.encrypt(self.e2.get(),password),cryptocode.encrypt(self.e3.get(),password),cryptocode.encrypt(self.e4.get(),password))
		cur.execute("INSERT INTO Passwords VALUES(?, ?, ?, ?, ?, ?);",PassToAdd)
		conn.commit()
		cur.close()
		conn.close()
		global updateDB
		updateDB = True




#*			-------Основное окно-------			
class App(CTk.CTk):
	def __init__(self) -> None:
		super().__init__()
		self.view = CTk.CTkImage(dark_image= Image.open("./images/view.png"),size=(20,20))
		self.bucket = CTk.CTkImage(dark_image = Image.open("./images/delete.png"), size=(20,20))
		self.next = CTk.CTkImage(dark_image = Image.open("./images/next-button.png"), size=(20,20))
		self.back = CTk.CTkImage(dark_image = Image.open("./images/back-button.png"), size=(20,20))
		self.geometry("645x250")
		self.title("Password manager")
		self.resizable(False,False)
		global password

		self.pass_get = CTk.CTkInputDialog(title="LOCK",text="Please Enter Password:")

		self.button_frame = CTk.CTkFrame(master=self, fg_color="#343a40")
		self.button_frame.grid(row=0,column=0,sticky="nsew",padx=(5,5),pady=(5,5))

		self.button_addNewPass = CTk.CTkButton(master=self.button_frame,text="Add New Password",width=120,command=self.addPass)
		self.button_addNewPass.grid(row=0,column=0,padx=(5),pady=(5))

		self.button_Settings = CTk.CTkButton(master=self.button_frame,text="Search",width=120,command=self.deleter)
		self.button_Settings.grid(row=0,column=1,padx=(5),pady=(5))

		self.button_update = CTk.CTkButton(master=self.button_frame,text="Settings",width=120,command=self.openSettings)
		self.button_update.grid(row=0,column=2,padx=(5),pady=(5))

		self.button_update = CTk.CTkButton(master=self.button_frame,text="Update",width=180,command=self.update)
		self.button_update.grid(row=0,column=3,padx=(5),pady=(5))

		self.page_lable = CTk.CTkLabel(master=self.button_frame,text=f"{int(math.ceil(page/inpage))+1}/{int(math.ceil(Num_count/inpage))}")
		self.page_lable.grid(row=0,column=4,padx=(3),pady=(5))

		self.pass_list = CTk.CTkFrame(master=self,fg_color="#343a40")
		self.pass_list.grid(row=1,column=0,sticky="nsew",padx=(5,5),pady=(0,5))

		self.numHeader = CTk.CTkLabel(master=self.pass_list,text="№",width=7,font=CTk.CTkFont(size=15, weight="bold"))
		self.numHeader.grid(row=1,column=0,padx=(5),pady=(5))

		self.textHeader = CTk.CTkLabel(master=self.pass_list,text="Password for",width=160,font=CTk.CTkFont(size=15, weight="bold"))
		self.textHeader.grid(row=1,column=1,padx=(5),pady=(5))

		self.text1Header = CTk.CTkLabel(master=self.pass_list,text="Login",width=160,font=CTk.CTkFont(size=15, weight="bold"))
		self.text1Header.grid(row=1,column=2,padx=(5),pady=(5))

		self.text2Header = CTk.CTkLabel(master=self.pass_list,text="Password",width=160,font=CTk.CTkFont(size=15, weight="bold"))
		self.text2Header.grid(row=1,column=3,padx=(5),pady=(5))

		self.text3Header = CTk.CTkLabel(master=self.pass_list,text="",width=10,font=CTk.CTkFont(size=15, weight="bold"))
		self.text3Header.grid(row=1,column=4,padx=(5),pady=(5))


		self.button_Backpage = CTk.CTkButton(master=self.pass_list,text="",width=40,image=self.back,fg_color="transparent",command=self.	backPage)
		self.button_Backpage.grid(row=1,column=4,padx=(5),pady=(5))

		self.button_Nextpage = CTk.CTkButton(master=self.pass_list,text="",width=40,image=self.next,fg_color="transparent",command=self.		nextPage)
		self.button_Nextpage.grid(row=1,column=5,padx=(5),pady=(5))

		self.pass_listT = CTk.CTkFrame(master=self,fg_color="#343a40")
		self.pass_listT.grid(row=2,column=0,sticky="nsew",padx=(5,5),pady=(0,5))
		global updateDB
		updateDB = True

		password = self.pass_get.get_input()

		self.list()
		

	def openSettings(self):
		settings = Settings()
		settings.mainloop()

	def list(self):
		global password
		conn = sqlite3.connect('passwords.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS Passwords(Num INT,For TEXT,Login TEXT,Password TEXT, Mail TEXT, Description TEXT);")
		conn.commit()
		self.pass_listT.destroy()
		self.pass_listT = CTk.CTkFrame(master=self,fg_color="#343a40")
		self.pass_listT.grid(row=2,column=0,sticky="nsew",padx=(5,5),pady=(0,5))
		global page
		cur.execute("SELECT Num FROM Passwords;")
		Num = cur.fetchall()
		global logs
		
		global updateDB
		if updateDB:
			logs=[]
			if len(Num) == 0:
				self.lable = CTk.CTkLabel(master=self.pass_listT,text="Empty",width=160,font=CTk.CTkFont(size=50, weight="bold"),text_color="#495057")
				self.lable.grid(row=0,column=0,padx=230,pady=(47,48))

			updateDB = False
			for fcasheshe,f in enumerate(Num):
				fcasheshe+=1
				if f[0] != fcasheshe:
					cur.execute(f"UPDATE Passwords SET Num = {fcasheshe} WHERE Num = {f[0]}")
					conn.commit()
			cur.execute("SELECT Num FROM Passwords;")
			Num = cur.fetchall()
			for S in Num:
				logs.append([0,0,0])
				data = cur.execute("SELECT For, Login, Password FROM Passwords WHERE Num == ?",(S[0],)).fetchone()
				for decod,dataf in enumerate(data):
					logs[S[0]-1][decod] = cryptocode.decrypt(dataf,password)
			
		for sop in range(page,inpage+page,1):
			try:
				d0 = "very long" if len(logs[sop][0]) > 20 else logs[sop][0]
				d1 = "very long" if len(logs[sop][1]) > 20 else logs[sop][1]
				d2 = "very long" if len(logs[sop][2]) > 20 else logs[sop][2]
				self.num = CTk.CTkLabel(master=self.pass_listT,text=f"{sop+1}",width=7)
				self.num.grid(row=sop-page,column=0,padx=(5),pady=(5))

				self.text = CTk.CTkLabel(master=self.pass_listT,text=f"{d0}",width=160)
				self.text.grid(row=sop-page,column=1,padx=(5),pady=(5))

				self.text1 = CTk.CTkLabel(master=self.pass_listT,text=f"{d1}",width=160)
				self.text1.grid(row=sop-page,column=2,padx=(5),pady=(5))

				self.text2 = CTk.CTkLabel(master=self.pass_listT,text=f"{d2}",width=160)
				self.text2.grid(row=sop-page,column=3,padx=(5),pady=(5))
				if sop-page == 0:
					delcom = self.deleterpass1
					ViewThis = self.vewer1
				if sop-page == 1:
					delcom = self.deleterpass2
					ViewThis = self.vewer2
				if sop-page == 2:
					delcom = self.deleterpass3
					ViewThis = self.vewer3
				if sop-page == 3:
					delcom = self.deleterpass4
					ViewThis = self.vewer4
				self.button_Delete = CTk.CTkButton(master=self.pass_listT,text="",width=40,image=self.bucket,fg_color="transparent",command=delcom)
				self.button_view = CTk.CTkButton(master=self.pass_listT,text="",width=40,image=self.view,fg_color="transparent",command=ViewThis)
				self.button_Delete.grid(row=sop-page,column=4,padx=(5),pady=(5))
				self.button_view.grid(row=sop-page,column=5,padx=(5),pady=(5))
			except: break


		cur.close()
		conn.close()



	def vewer1(self):
		global page
		Num = 1+page
		vp = ViewPass()
		vp.addNum(Num)
		vp.mainloop()
	def vewer2(self):
		global page
		Num = 2+page
		vp = ViewPass()
		vp.addNum(Num)
		vp.mainloop()
	def vewer3(self):
		global page
		Num = 3+page
		vp = ViewPass()
		vp.addNum(Num)
		vp.mainloop()
	def vewer4(self):
		global page
		Num = 4+page
		vp = ViewPass()
		vp.addNum(Num)
		vp.mainloop()




	def deleterpass1(self):
		global updateDB
		updateDB = True
		global page
		conn = sqlite3.connect('passwords.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS Passwords(Num INT,For TEXT,Login TEXT,Password TEXT, Mail TEXT, Description TEXT);")
		conn.commit()
		cur.execute(f"DELETE FROM Passwords WHERE Num={1+page};")
		conn.commit()
		cur.execute("SELECT Num FROM Passwords;")
		Num_count = len(cur.fetchall())
		cur.close()
		conn.close()
		if Num_count > page:
			self.page_lable.configure(text=f"{int(math.ceil(page/inpage))+1}/{int(math.ceil(Num_count/inpage))}")
			self.list()
		else:
			page-=4
			self.page_lable.configure(text=f"{int(math.ceil(page/inpage))+1}/{int(math.ceil(Num_count/inpage))}")
			self.list()
		
		pass
	def deleterpass2(self):
		global updateDB
		updateDB = True
		global page
		conn = sqlite3.connect('passwords.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS Passwords(Num INT,For TEXT,Login TEXT,Password TEXT, Mail TEXT, Description TEXT);")
		conn.commit()
		cur.execute(f"DELETE FROM Passwords WHERE Num={2+page};")
		conn.commit()
		cur.execute("SELECT Num FROM Passwords;")
		Num_count = len(cur.fetchall())
		cur.close()
		conn.close()
		if Num_count > page:
			self.page_lable.configure(text=f"{int(math.ceil(page/inpage))+1}/{int(math.ceil(Num_count/inpage))}")
			self.list()
		else:
			page-=4
			self.page_lable.configure(text=f"{int(math.ceil(page/inpage))+1}/{int(math.ceil(Num_count/inpage))}")
			self.list()
		pass
	def deleterpass3(self):
		global updateDB
		updateDB = True
		global page
		conn = sqlite3.connect('passwords.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS Passwords(Num INT,For TEXT,Login TEXT,Password TEXT);")
		conn.commit()
		cur.execute(f"DELETE FROM Passwords WHERE Num={3+page};")
		conn.commit()
		cur.execute("SELECT Num FROM Passwords;")
		Num_count = len(cur.fetchall())
		cur.close()
		conn.close()
		if Num_count > page:
			self.page_lable.configure(text=f"{int(math.ceil(page/inpage))+1}/{int(math.ceil(Num_count/inpage))}")
			self.list()
		else:
			page-=4
			self.page_lable.configure(text=f"{int(math.ceil(page/inpage))+1}/{int(math.ceil(Num_count/inpage))}")
			self.list()
		pass
	def deleterpass4(self):
		global updateDB
		updateDB = True
		global page
		conn = sqlite3.connect('passwords.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS Passwords(Num INT,For TEXT,Login TEXT,Password TEXT, Mail TEXT, Description TEXT);")
		conn.commit()
		cur.execute(f"DELETE FROM Passwords WHERE Num={4+page};")
		conn.commit()
		cur.execute("SELECT Num FROM Passwords;")
		Num_count = len(cur.fetchall())
		cur.close()
		conn.close()
		if Num_count > page:
			self.page_lable.configure(text=f"{int(math.ceil(page/inpage))+1}/{int(math.ceil(Num_count/inpage))}")
			self.list()
		else:
			page-=4
			self.page_lable.configure(text=f"{int(math.ceil(page/inpage))+1}/{int(math.ceil(Num_count/inpage))}")
			self.list()
		pass
	
	def deleter(self):
		pass
		

	def nextPage(self):
		conn = sqlite3.connect('passwords.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS Passwords(Num INT,For TEXT,Login TEXT,Password TEXT, Mail TEXT, Description TEXT);")
		conn.commit()
		cur.execute("SELECT Num FROM Passwords;")
		Num_count = len(cur.fetchall())
		cur.close()
		conn.close()
		global page
		page +=inpage
		if Num_count > page:
			self.page_lable.configure(text=f"{int(math.ceil(page/inpage))+1}/{int(math.ceil(Num_count/inpage))}")
			self.list()
		else:
			page-=inpage
		pass

	def backPage(self):
		conn = sqlite3.connect('passwords.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS Passwords(Num INT,For TEXT,Login TEXT,Password TEXT, Mail TEXT, Description TEXT);")
		conn.commit()
		cur.execute("SELECT Num FROM Passwords;")
		Num_count = len(cur.fetchall())
		cur.close()
		conn.close()
		global page
		global inpage
		if page >= inpage:
			page -=inpage
			self.page_lable.configure(text=f"{int(math.ceil(page/inpage))+1}/{int(math.ceil(Num_count/inpage))}")
			self.list()
		pass






	def update(self):
		global updateDB
		updateDB = True
		global page
		conn = sqlite3.connect('passwords.db')
		cur = conn.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS Passwords(Num INT,For TEXT,Login TEXT,Password TEXT, Mail TEXT, Description TEXT);")
		conn.commit()
		cur.execute("SELECT Num FROM Passwords;")
		Num_count = len(cur.fetchall())
		cur.close()
		conn.close()
		self.page_lable.configure(text=f"{int(math.ceil(page/4))+1}/{int(math.ceil(Num_count/4))}")
		self.list()
		pass

	def addPass(self):
		new = Pass()
		new.mainloop()



if __name__ == "__main__":
	app = App()
	app.mainloop()


