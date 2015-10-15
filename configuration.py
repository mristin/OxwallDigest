__author__ = "marko"

import datetime

# Database connection "mysql://{user name}:{password}@{host name}:{port}/{database name}?charset=utf8
database_url = "mysql://marko:espasswort@localhost:3306/oxwall?charset=utf8"

# SMTP server to be used for sending emails. Can include a port.
smtp_server = "localhost"

# The email address of the digest sender. Best you chose a real address, as users might respond to it.
sender = "zusammenfassung@nena1.ch"

# Path to the state file that will be updated with a checkpoint everytime the application has run.
# The path can be either absolute or relative.
# Each line in the state file is a valid JSON-encoded object.
state_path = "/home/marko/digest.state.json"

# Path to the log. You can specify either a relative or an absolute path.
# Each line is a valid JSON-encoded object.
log_path = "/home/marko/digest.log.json"

# Email address of the administrator. Shows whenever a mail client can not display HTML and
# at the end of the digest mail to direct the user for opting out.
admin_email = "marko.ristin@gmail.com"

# The digest email will not be sent if the message exceeds this number of bytes.
max_message_size = 1024 * 1024

# If true, the digest email will be sent to all users stored in the Oxwall users (except excluded_recipients).
send_to_all_oxwall_users = False

# allows you to include users who are not registered in Oxwall, but who would like
# to receive the email. In case you are not sending an email to all users (see send_to_all_oxwall_users),
# you can cherry-pick to whom the digest should be sent.
additional_recipients = ["marko.ristin@gmail.com"]

# list of email addresses which are excluded from the digest recipient list.
excluded_recipients = []

# all the content posted before this date/time is excluded from the digest. Use this option to prevent a huge
# digest when you start with the service.
exclude_content_before = datetime.datetime(2012,10,1)

# the url prefix appended to all Oxwall links (e.g., to forum posts or blog posts)
url_prefix = "http://oxwall.nena1.ch"