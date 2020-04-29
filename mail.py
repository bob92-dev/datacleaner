import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def mailMe(exp,dest,log, mdp, subject, my_message, join_piece):
    msg = MIMEMultipart()
    msg['From'] = exp
    msg['To'] = dest
    msg['Subject'] = subject
    message = my_message
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(log, mdp)
    mailserver.sendmail(exp,dest, msg.as_string())
    mailserver.quit()


