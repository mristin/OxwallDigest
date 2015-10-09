__author__ = 'marko'

import datetime

database_url = 'mysql://marko:espasswort@localhost:3306/oxwall?charset=utf8'
smtp_server = 'localhost'
sender = 'zusammenfassung@nena1.ch'
state_path = '/home/marko/digest.state.json'
error_log_path = '/home/marko/digest.error.json'

admin_email = 'marko.ristin@gmail.com'
max_message_size = 1024 * 1024

send_to_all_oxwall_users = False
additional_recipients = ['marko.ristin@gmail.com']
excluded_recipients = []

exclude_content_before = datetime.datetime(2012,10,1)