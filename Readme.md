# Summary

A simple python script which is able to produce a digest HTML mail on the most recent activities of an oxwall community software platform (see http://www.oxwall.org/).

The mail is sent either to all users (excluding a configurable blacklist) or to a configurable whitelist of mail addresses.


# Installation

Since there are no dependencies to the oxwall php scripts, these digest scripts can be run on an arbitrary machine. It only must have access to the oxwall database and to an SMTP server.

Copy the scripts to a folder of your choice, e.g.
```bash
/opt/oxdigest/
```

Create a folder where you want to have the log file, e.g.
```bash
/var/log/oxdigest/
```

Install the following python dependencies:
```bash
sudo apt-get install python-mysqldb
sudo apt-get install python-sqlalchemy
sudo apt-get install python-jinja2
```

Adapt the configuration.py to fit your system settings.

Add the script to the cron:
```bash
crontab -e
```

For example running it all Friday morning at 2 a.m.:
```bash
0 2 * * 5 python /opt/oxdigest/launch.py
```
