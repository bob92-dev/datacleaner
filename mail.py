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


mailMe('boblepongedev92','svenlehamster@gmail.com','boblepongedev92@gmail.com','spongebob;', 'coucou', 'tu veux voir ma ?','tapiece.txt')
mailMe('boblepongedev92','casselboris92@gmail.com','boblepongedev92@gmail.com','spongebob;', 'coucou', 'tu veux voir ma ?','tapiece.txt')


