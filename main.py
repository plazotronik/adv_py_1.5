import email
import smtplib
import imaplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Email:
    def __init__(self, login, password):
        self.domain_smtp = 'smtp.yandex.ru'
        self.domain_imap = 'imap.yandex.ru'
        self.port_smtp = 465
        self.port_imap = 993
        self.login = login
        self.password = password
        try:
            self.smtp_message = \
                smtplib.SMTP_SSL(self.domain_smtp, self.port_smtp)
            self.smtp_message.login(self.login, self.password)
            self.imap_message = \
                imaplib.IMAP4_SSL(self.domain_imap, self.port_imap)
            self.imap_message.login(self.login, self.password)
        except Exception as err:
            print(err)

    def send_message(self, subject='Subject', recipients='',
                     message='message'):
        mime_message = MIMEMultipart()
        mime_message['From'] = self.login
        mime_message['To'] = recipients
        mime_message['Subject'] = subject
        mime_message.attach(MIMEText(message))
        try:
            self.smtp_message.sendmail(self.login, recipients.split(','),
                                       mime_message.as_string())
        except Exception as err:
            return err
        else:
            return 'Message successfully send'

    def receive_message(self, header=None, item='inbox', position_message=-1):
        try:
            self.imap_message.select(item)
            criterion = f'(HEADER Subject {header if header else "ALL"})'
            typ, data = self.imap_message.search(None, criterion)
            assert data[0], 'There are no letters with current header'
        except AssertionError:
            return 'There are no letters with current header'
        except Exception as err:
            return err
        else:
            latest_email_uid = data[0].split()[position_message]
            typ, data = self.imap_message.fetch(latest_email_uid, '(RFC822)')
            return email.message_from_bytes(data[0][1])

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.smtp_message.quit()
        self.imap_message.close()
        self.imap_message.logout()


if __name__ == '__main__':
    # Change to your credentials.
    user_name = Email('user_name@yandex.ru', 'password')
    print(user_name.send_message(subject='Subject', message='Hello friend',
                                 recipients='login@domain.ru'))
    print(user_name.receive_message())
