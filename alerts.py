#Send warning alerts and notify throguh mail

#libraries 
from tkinter import *
from tkinter import ttk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def warning_message():
#Create an instance of tkinter frame
     win = Tk()
     #Set the geometry of tkinter frame
     win.geometry("750x270")
     win.title("WARNING")
     Label(win, text= "--Insert warning message to be displayed",font=('Helvetica 18 bold')).pack(pady=40)

     #Automatically close the window after 3 seconds
     win.after(2000,lambda:win.destroy())

     win.mainloop()

#send email

def send_mail(filename,snap_num):
    fromaddr = "--From address"
    toaddr = "--To address"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "--Subject of mail"
    body = "--Body of mail "+str(snap_num)+"."
    msg.attach(MIMEText(body, 'plain'))
    attachment = open(filename, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
   
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "--Password")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)