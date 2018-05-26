import smtplib


class Email:

    def __init__(self, host, port, email, password):
        self.host = host
        self.port = port
        self._email = email
        self._password = password
        self.smtp = smtplib.SMTP(self.host, self.port)

    def authenticate_login(self):
        try:
            self.smtp.connect(self.host, self.port)
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.login(self._email, self._password)
            return True

        except Exception as error:
            print(error)
            return False