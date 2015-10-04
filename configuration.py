__author__ = 'marko'

import datetime

database_url = 'mysql://marko:espasswort@localhost:3306/oxwall'
smtp_server = 'localhost'
sender = 'zusammenfassung@nena1.ch'
log_path = '/home/marko/digest.log.json'
admin_email = 'marko.ristin@gmail.com'

send_to_all_oxwall_users = False
additional_recipients = ['marko.ristin@gmail.com']
excluded_recipients = []

exclude_content_before = datetime.datetime(2015,10,1)