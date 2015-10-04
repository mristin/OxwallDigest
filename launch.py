#!/usr/bin/env python
__author__ = 'marko'

import sys, os, datetime, smtplib, json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import sqlalchemy
from sqlalchemy import and_

import model
from model import Forum_post, Forum_section, Forum_group, Forum_topic, User
import configuration


def seconds_since_epoch(a_datetime):
    """
    :param a_datetime: datetime.datetime
    :return: long
    """
    """
    :param a_datetime: datetime.datetime
    :return: long
    """
    epoch = datetime.datetime.utcfromtimestamp(0)
    return long((a_datetime - epoch).total_seconds())


datetime_format = '%Y-%m-%dT%H-%M-%S'


def read_last_insterval_end_from_log():
    if not os.path.exists(os.path.dirname(configuration.log_path)):
        sys.stderr.write('The directory %s of the log file %s must exist.' % (
            os.path.dirname(configuration.log_path), configuration.log_path))
        sys.exit(1)

    try:
        if not os.path.exists(configuration.log_path):
            fid = open(configuration.log_path, 'w')
            fid.close()
    except IOError:
        sys.stderr.write('The log file %s could not be written with empty content.' % configuration.log_path)
        sys.exit(1)

    lines = []
    try:
        fid = open(configuration.log_path, 'r')
        lines = [line for line in fid.readlines() if not line.startswith('#') and not len(line.strip()) == 0]
        fid.close()
    except IOError:
        sys.stderr.write('The log file %s could not be opened for reading.' % configuration.log_path)
        sys.exit(1)

    def extract_timestamps(enumerated_line):
        (line_number, line) = enumerated_line
        try:
            entry = json.loads(line)
            return datetime.datetime.strptime(entry['interval_end'], datetime_format)
        except Exception as exception:
            sys.stderr.write('Line %d in log file %s is invalid: %s.' % (
                line_number, configuration.log_path, repr(exception)
            ))
            sys.exit(1)

    timestamps = [configuration.exclude_content_before] + map(extract_timestamps, enumerate(lines))
    return max(timestamps)


def main():
    if len(sys.argv) != 1:
        sys.stderr.write('Usage: launch.py {no arguments}')
        sys.exit(1)

    interval_begin = read_last_insterval_end_from_log()
    interval_end = datetime.datetime.now()

    engine = sqlalchemy.create_engine(configuration.database_url)

    model.Base.metadata.bind = engine
    DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
    session = DBSession()

    # Cache
    session.query(Forum_section).all()
    session.query(Forum_group).all()
    session.query(Forum_topic).all()
    session.query(User).all()

    message = ['<html><head></head><body>\n']

    # Digest the forum content
    forum_post_count = 0
    for post in session.query(Forum_post).filter(
            and_(Forum_post.create_stamp >= seconds_since_epoch(interval_begin),
                 Forum_post.create_stamp < seconds_since_epoch(interval_end))).order_by(Forum_post.create_stamp):

        if not post.topic.group.is_private and not post.topic.group.section.is_hidden:
            message.append('<strong>Benutzer %s schrieb am %s im Forum zum Thema \'%s\':</strong>\n' % (
                post.user.username, datetime.datetime.fromtimestamp(post.create_stamp).strftime('%Y-%m-%d %H:%M'),
                post.topic.title
            ))
            message.append('<div style=\'padding-bottom: 10px; background-color: #F0F8FF;\'>\n')
            message.append(post.text)
            message.append('</div>\n')
            forum_post_count += 1

    if forum_post_count == 0:
        message.append('<em>Keine neuen Forum-Posts</em>')

    message.append('</body></html>')


    # Send digests
    recipient_list = []
    if configuration.send_to_all_oxwall_users == True:
        for user in session.query(User).all():
            recipient_list.append(user.email)

    recipient_list.extend(configuration.additional_recipients)
    excluded_recipient_set = set(configuration.excluded_recipients)
    recipient_list = [recipient for recipient in recipient_list if recipient not in excluded_recipient_set]

    s = smtplib.SMTP(configuration.smtp_server)
    for recipient in recipient_list:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Nena1 Oxwall Zusammenfassung von %s bis %s' % (
            interval_begin.strftime('%Y-%m-%d %H:%M'),
            interval_end.strftime('%Y-%m-%d %H:%M')
        )
        msg['From'] = configuration.sender
        msg['To'] = recipient
        msg.attach(MIMEText(
            'Dein Email-Klient kann leider keine HTML-Nachrichten anzeigen. ' + \
            'Bitte wende Dich an: %s' % (
                configuration.admin_email), 'plain'))
        msg.attach(MIMEText(''.join(message), 'html'))

        s.sendmail(configuration.sender, recipient, msg.as_string())

    s.quit()

    # Log
    try:
        fid = open(configuration.log_path, 'a')
        fid.write('\n{"interval_begin": "%s", "interval_end": "%s", "forum_post_count": %d, "recipient_count": %d}' % (
            interval_begin.strftime(datetime_format), interval_end.strftime(datetime_format),
            forum_post_count, len(recipient_list)))
        fid.close()
    except IOError:
        sys.stderr.write('The log file %s could not be opened for appending.' % configuration.log_path)
        sys.exit(1)


if __name__ == '__main__':
    main()
