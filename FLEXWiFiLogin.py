import Tkinter 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import *
import tkMessageBox
from Tkinter import *
import subprocess
import os


top = Tkinter.Tk()
top.minsize(width=420, height=170)
top.wm_title("Flex WiFi Login")
#main window
main_panel_window = PanedWindow()
main_panel_window.pack(fill=BOTH,expand =1)
#top_panel
top_main_panel = PanedWindow()
top_main_panel.pack(fill=BOTH,expand =1)
main_panel_window.add(top_main_panel)
top_main_panel.place(bordermode = INSIDE, x = 40)
#bottom_panel
bottom_main_panel = PanedWindow()
bottom_main_panel.pack(fill=BOTH,expand =1)
main_panel_window.add(bottom_main_panel)
bottom_main_panel.place(bordermode = INSIDE,x=50,y=50)
#inf_panel
top_panel_window = PanedWindow()
top_panel_window.pack(fill=BOTH,expand =1)
Label(top_panel_window, text="Welcome to FLEX Visitor WiFi Login").grid(row=1)
Label(top_panel_window, text="*** FOR CHROME ONLY ***").grid(row=2)
Label(top_panel_window, text="Please save your username and password for first time only!!!").grid(row=3)
top_main_panel.add(top_panel_window)
#label_panel
left_mid_panel_window = PanedWindow(orient=VERTICAL)
left_mid_panel_window.pack(fill=BOTH,expand =1)
Label(left_mid_panel_window, text='Username: ',bd=5).pack()
Label(left_mid_panel_window, text="Password:",bd=5).pack()
Label(left_mid_panel_window, text="Expiry(format:yyyy-mm-dd):",bd=5).pack()
bottom_main_panel.add(left_mid_panel_window)
#entry_panel
right_mid_panel_window = PanedWindow()
right_mid_panel_window.pack(fill=BOTH,expand =1)
UE = Tkinter.Entry(right_mid_panel_window, bd =5)
PE = Tkinter.Entry(right_mid_panel_window, bd =5,show='*')               
DE = Tkinter.Entry(right_mid_panel_window, bd =5)
UE.pack()
PE.pack()
DE.pack()

bottom_main_panel.add(right_mid_panel_window)

def login_web():
    try:
        browser = webdriver.Chrome()
        browser.get('https://1.1.1.1/fs/customwebauth/login.html?switch_url=https://1.1.1.1/login.html')
        assert 'Web Authentication' in browser.title
        try:
            today = date.today()
            f = open('info.txt','r')
            info = f.read()
            username = info.split('|')[0]
            password = info.split('|')[1]
            future_year = int(info.split('|')[2].split('-')[0])
            future_month = int(info.split('|')[2].split('-')[1])
            future_day = int(info.split('|')[2].split('-')[2])
                    
            future = date(future_year,future_month,future_day)
            diff = future - today
            
            browser.find_element_by_name('username').send_keys(username)
            browser.find_element_by_name('password').send_keys(password)
            browser.find_element_by_name('Submit').click()
            try:
                assert 'https://www.flextronics.com' in browser.current_url
                print 'Logged In'
                browser.quit()
                tkMessageBox.showinfo('Logged In','Logged in. Your wifi account is expiring in %s days'%diff.days)
            except AssertionError:
                browser.quit()
                tkMessageBox.showerror("Login Failed","Already login?")
        except ValueError:
            browser.quit()
            tkMessageBox.showerror('UserID and Pass not found!','No records found! Please register again!')
        except IOError:
            browser.quit()
            tkMessageBox.showerror('create a info.txt file','No info found! Please create info.txt to store ur pasword')
            assert 'Web Authentication' in browser.title
    except AssertionError:
        browser.quit()
        tkMessageBox.showerror('Error connected to wifi!','Are you connected to flex wifi?')
    except:
        browser.quit()
        tkMessageBox.showerror("Startup failed","got problem?")
        
        
def logout_web():
    browser = webdriver.Chrome()
    try:
        browser.get('https://1.1.1.1/logout.html')   
        assert 'Logout' in browser.title
        browser.find_element_by_name('Logout').click()
        browser.quit()
        tkMessageBox.showinfo("Logged out","You have logged out successfully")
    except AssertionError:
        browser.quit()
        tkMessageBox.showinfo( "Logout Failed", "Already logged out?")
        

def register_ID():
    try:
        if UE.get() and PE.get() and DE.get() is not None:
            with open("info.txt", "w") as text_file:
                text_file.write('{}|{}|{}'.format(UE.get(),PE.get(),DE.get()))
                tkMessageBox.showinfo('Saved','Your info is now stored in info.txt')
        else:
            tkMessageBox.showerror('Registation failed','Please do not insert empty info')
    except IOError:
        tkMessageBox.showerror('Registration failed','Please try again')

def open_vpn():
    cmd = [r"C:\Program Files (x86)\Cisco\Cisco AnyConnect Secure Mobility Client\vpnui.exe", "param1", "param2"]
    abc = subprocess.call(cmd)

#button_panel
bottom_panel = PanedWindow()
bottom_panel.pack(fill=BOTH,expand =1)
Button(bottom_panel, text= 'Login', command = login_web).pack()
Button(bottom_panel, text= 'Logout', command = logout_web).pack()
Button(bottom_panel, text= 'Register', command = register_ID).pack()
Button(bottom_panel, text= 'VPN on', command = open_vpn).pack()
bottom_main_panel.add(bottom_panel)
top.mainloop()


