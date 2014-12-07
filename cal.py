# -*- coding: utf-8 -*-
#__author__ = 'kxekxe'

import httplib2
import sys
import os

from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from oauth2client import tools
from oauth2client import client
from apiclient.discovery import build
import apiclient.errors
import socket

scope = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRETS = 'client_secrets.json'

class cmd_flags(object):
    """Set some flags for oAuth2 flow"""
    def __init__(self):
        self.short_url = True
        self.noauth_local_webserver = False
        self.logging_level = 'DEBUG'
        self.auth_host_name = 'localhost'
        self.auth_host_port = [8080, 9090]

class GCal():
	cacert = None
	proxy = None

	def __init__(self):
		self.h = httplib2.Http(proxy_info=self.proxy, ca_certs=self.cacert)
		self.storage = Storage('calendar.dat')
		self.credentials = self.storage.get()
		if self.credentials is None or self.credentials.invalid:
			credentials = tools.run_flow(flow, self.storage, cmd_flags(), http=self.h)

	def listCals(self, force=False):
		result= []
		if force:
			http = self.credentials.authorize(self.h)
			service = build("calendar", "v3", http=http)

			lists = service.calendarList().list().execute(http=http)
			index = 0
			if 'items' in lists:
				gcals = lists['items']
				for gcal in gcals:
					if (gcal['accessRole'] == "owner"
							and gcal['kind'] == "calendar#calendarListEntry"):
						result.append((index, gcal['id'], gcal['summary']))
						index = index + 1

		return result

	def listEvents(self, CalID = ''):
		if not CalID:
			raise 'Calendar not specified'
		result = []
		http = self.credentials.authorize(self.h)
		service = build("calendar", "v3", http=http)
		request = service.events().list(calendarId=CalID, timeMin = '2014-12-04T00:00:00+01:00', timeMax = '2014-12-05T00:00:00+01:00')
		while request != None:
			response = request.execute()
			for event in response.get('items', []):
				result.append(event.get('summary', 'NO SUMMARY'))
			request = service.events().list_next(request, response)

		return result
def main():
	if os.path.exists(CLIENT_SECRETS):
		flow = client.flow_from_clientsecrets(
					CLIENT_SECRETS,
					scope=[
						'https://www.googleapis.com/auth/calendar',
						'https://www.googleapis.com/auth/calendar.readonly',
					],
					# message=self.secretsMissings(CLIENT_SECRETS)
					)
	else:
		clientID = os.environ.get('clientID')
		sicret = os.environ.get('sicret')
		if not clientID or not sicret:
			raise 'ClientID or Sicret key not specified'
		flow = OAuth2WebServerFlow(clientID, sicret, scope)
	cal = GCal()
	events = cal.listEvents('shkipc@gmail.com')
	for ev in events:
		print ev


if __name__ == '__main__':
	main()

