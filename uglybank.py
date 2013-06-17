#!/usr/bin/python
# -*- coding: utf-8 -*-

from imaplib import IMAP4_SSL
import sys, os, re, time
from datetime import datetime, timedelta, date
from ConfigParser import ConfigParser
import quopri

config = 'default'


def main():
	conf = ConfigParser()
	conf.read('config.ini')
	server = "imap.gmail.com"
	user = conf.get(config, "username")
	password = conf.get(config, "password")

	gmail = IMAP4_SSL(server)
	gmail.login(user, password)
	gmail.select(conf.get(config, "label"))

	type, data = gmail.search(None, '(UNSEEN)')
	msgs = []
	p_spankki = re.compile("(\d{1,2}\.\d{1,2}\.\d{4}\ \d{1,2}\:\d{1,2}\:\d{1,2}).*?Saldosi\ .+?\ (.+)?\ on\ (.+?) EUR", flags=re.MULTILINE)
	p_tapiola = re.compile("(\d{1,2}\.\d{1,2}\.\d{4}\ \d{1,2}\:\d{1,2}\:\d{1,2}).*?tilillä\ (.+)?\ on\ tänään\ (.+?)\.", flags=re.MULTILINE)
	con = None

	for num in data[0].split():
	        type, data = gmail.fetch(num, '(BODY[TEXT])')
	        msgs.append(data[0][1])
		msg = quopri.decodestring(data[0][1]).decode('iso-8859-1').replace("\n", " ").replace("\r", " ").encode("utf-8")

		m_spankki = p_spankki.match(msg)
		m_tapiola = p_tapiola.match(msg)

		m = None
		if m_spankki:
			m = m_spankki
		if m_tapiola:
			m = m_tapiola
		if m:
	        	dt = time.strptime(m.group(1),"%d.%m.%Y %H:%M:%S")
			account = m.group(2)
			pattern = re.compile('[^0-9,.]', re.UNICODE)
			sum = str(pattern.sub(' ', m.group(3)))
			sum = float(sum.replace(" ","").replace(",","."))
	        	stamp = int(time.mktime(dt))
			print "%s	%s	%.2f" % (datetime.fromtimestamp(stamp).strftime("%Y-%m-%d %H:%M:%S"), account, sum)
		#else:
		        #print 'Message %s: %s\n' % (num, msg)

	gmail.close()
	gmail.logout()


if __name__ == "__main__":
	main()
