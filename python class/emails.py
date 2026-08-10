import smtplib , mimetypes , os
from email.message import EmailMessage

sender = 'nikishdaniel1@gmail.com'
emailContainer = EmailMessage()
emailContainer['Subject'] = 'Sample Email'
emailContainer['From'] = sender
emailContainer['To'] = 'nikishdaniel77@gmail.com'
emailContainer.set_content('HI Best Regards')

files = [r'c:\Users\WELCOME\Pictures\Screenshots\Screenshot (566).png',r'c:\Users\WELCOME\Documents\mac1.xlsx']
if files:
    for i in files:
        with open(i,'rb') as file:data = file.read();fileName = file.name
        fileType = mimetypes.guess_type(fileName)[0]
        if fileType:maintype,subtype = fileType.split('/',1)
        else:maintype,subtype = 'application','octet-stream'
        emailContainer.add_attachment(data,maintype=maintype,subtype=subtype,filename=os.path.basename(i))

with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
    with open(r'C:\Users\WELCOME\Documents\New App Password.txt','r') as passwordFile:password = passwordFile.read()
    smtp.login(sender,password)
    smtp.send_message(emailContainer)
print('sent successfully')