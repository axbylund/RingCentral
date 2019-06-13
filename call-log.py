#!/usr/bin/python3

RINGCENTRAL_PHONE = '+15555555555'
RINGCENTRAL_EXT = '101'

RINGCENTRAL_LOGIN = '15555555555'
RINGCENTRAL_PASS = 'password'

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from tinydb import *
from time import *
#from calendar import timegm

#from threading import Timer,Thread,Event
#from time import sleep

from ringcentral.subscription import Events
from ringcentral.http.api_exception import ApiException
from ringcentral import SDK

import requests

RINGCENTRAL_SERVER_URL = 'https://platform.devtest.ringcentral.com'
RINGCENTRAL_CLIENT_ID = ''
RINGCENTRAL_CLIENT_SECRET = ''
#RINGCENTRAL_OAUTH_CALLBACK = 'http://localhost/callback'

class MyWindow(Gtk.Window):

	def __init__(self):
		self.db = TinyDB('database.json')

		self.sdk = SDK(RINGCENTRAL_CLIENT_ID, RINGCENTRAL_CLIENT_SECRET, RINGCENTRAL_SERVER_URL)
		#self.auth_url = RINGCENTRAL_SERVER_URL + '/restapi/oauth/authorize?response_type=code&client_id=' + RINGCENTRAL_CLIENT_ID + '&state=initialState'
		#self.response = requests.get(self.auth_url)
		self.platform = self.sdk.platform()
		self.platform.login(RINGCENTRAL_LOGIN, RINGCENTRAL_EXT, RINGCENTRAL_PASS)

		"""
		self.db.insert( {'id':'1', 'workiz':False, 'phnumber':"+one", 'cust_name':"blahblahblah"} ) 
		self.db.insert( {'id':'2', 'workiz':False, 'phnumber':"+two", 'cust_name':"blahblahblah"} ) 
		self.db.insert( {'id':'3', 'workiz':False, 'phnumber':"+three", 'cust_name':"blahblahblah"} ) 
		self.db.insert( {'id':'4', 'workiz':False, 'phnumber':"+one", 'cust_name':"blahblahblah"} ) 
		self.db.insert( {'id':'5', 'workiz':False, 'phnumber':"+two", 'cust_name':"blahblahblah"} ) 
		self.db.insert( {'id':'6', 'workiz':False, 'phnumber':"+three", 'cust_name':"blahblahblah"} ) 
		self.db.insert( {'id':'7', 'workiz':False, 'phnumber':"+one", 'cust_name':"blahblahblah"} ) 
		self.db.insert( {'id':'8', 'workiz':False, 'phnumber':"+two", 'cust_name':"blahblahblah"} ) 
		self.db.insert( {'id':'9', 'workiz':False, 'phnumber':"+three", 'cust_name':"blahblahblah"} ) 
		"""

		Gtk.Window.__init__(self, title="Documented Call Log")
		self.set_default_size(1000, 400)
		self.set_border_width(3)

		self.notebook = Gtk.Notebook()
		self.add(self.notebook)

		###################
		###### PAGE 1 #####
		###################
		self.page1 = Gtk.Box()
		self.page1.set_border_width(10)

		self.liststore = Gtk.ListStore(bool, str, str, str, str, str, str, str)

		treeview = Gtk.TreeView(model=self.liststore)

		renderer_toggle = Gtk.CellRendererToggle()
		renderer_toggle.connect("toggled", self.on_cell_toggled)
		column_toggle = Gtk.TreeViewColumn("Workiz", renderer_toggle, active=0)
		treeview.append_column(column_toggle)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Phone Number", renderer_text, text=1)
		treeview.append_column(column_text)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Customer Name", renderer_text, text=2)
		treeview.append_column(column_text)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("ID", renderer_text, text=3)
		treeview.append_column(column_text)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Date and Time", renderer_text, text=4)
		column_text.set_sort_column_id(4)
		treeview.append_column(column_text)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Action", renderer_text, text=5)
		treeview.append_column(column_text)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Result", renderer_text, text=6)
		treeview.append_column(column_text)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Length", renderer_text, text=7)
		treeview.append_column(column_text)

		self.liststore.set_sort_func(0, self.compare, None)

		#self.page1.add(treeview)
		scroll_list1 = Gtk.ScrolledWindow()
		scroll_list1.set_vexpand(True)
		scroll_list1.set_hexpand(True)
		scroll_list1.add(treeview)
		self.page1.add(scroll_list1)

		self.button1 = Gtk.Button(label="Refresh")
		self.button1.connect("clicked", self.on_subscription)
		self.page1.add(self.button1)

		self.notebook.append_page(self.page1, Gtk.Label('Inbox') )

		###################
		###### PAGE 2 #####
		###################

		self.page2 = Gtk.Box()
		self.page2.set_border_width(10)

		self.liststore2 = Gtk.ListStore(bool, str, str, str, str, str, str, str)

		treeview2 = Gtk.TreeView(model=self.liststore2)

		renderer_toggle2 = Gtk.CellRendererToggle()
		renderer_toggle2.connect("toggled", self.on_cell_toggled_2)
		column_toggle = Gtk.TreeViewColumn("Workiz", renderer_toggle2, active=0)
		treeview2.append_column(column_toggle)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Phone Number", renderer_text, text=1)
		treeview2.append_column(column_text)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Customer Name", renderer_text, text=2)
		treeview2.append_column(column_text)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("ID", renderer_text, text=3)
		treeview2.append_column(column_text)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Date and Time", renderer_text, text=4)
		column_text.set_sort_column_id(4)
		treeview2.append_column(column_text)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Action", renderer_text, text=5)
		treeview2.append_column(column_text)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Result", renderer_text, text=6)
		treeview2.append_column(column_text)

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Length", renderer_text, text=7)
		treeview2.append_column(column_text)

		self.liststore2.set_sort_func(0, self.compare, None)

		#self.page2.add(treeview2)
		scroll_list = Gtk.ScrolledWindow()
		scroll_list.set_vexpand(True)
		scroll_list.set_hexpand(True)
		scroll_list.add(treeview2)
		self.page2.add(scroll_list)
		###### PAGE 2 #####
		self.notebook.append_page(
		self.page2,
		Gtk.Image.new_from_icon_name(
			"help-about",
			Gtk.IconSize.MENU
			)
		)

		self.read_database()
		#res = self.platform.get('/account/~/call-log')
		#self.on_subscription()

	def compare(model, row1, row2, user_data):
		sort_column, _ = model.get_sort_column_id()
		value1 = model.get_value(row1, sort_column)
		value2 = model.get_value(row2, sort_column)
		if value1 < value2:
			return -1
		elif value1 == value2:
			return 0
		else:
			return 1

	def on_cell_toggled(self, widget, path):
		Workizq = Query()
		self.liststore[path][0] = not self.liststore[path][0]
		self.db.update( {'workiz': self.liststore[path][0] }, Workizq.id == self.liststore[path][3] )
		self.read_database()

	def on_cell_toggled_2(self, widget, path):
		Workizq = Query()
		self.liststore2[path][0] = not self.liststore2[path][0]
		self.db.update( {'workiz': self.liststore2[path][0] }, Workizq.id == self.liststore2[path][3] )
		self.read_database()

	def read_database(self):
		self.liststore.clear()
		self.liststore2.clear()

		workizq = Query()
		db_list = self.db.search( (workizq.workiz == False) )
		for list_item in (db_list):
			lenstr = str((int(list_item['length'])/60))
			lenstr2 = lenstr[:lenstr.find(".")+3]
			lctime = list_item['date_time'].replace("T", " ").replace("Z", "")
			lctimeT = strptime(lctime[:lctime.find(".") ], "%Y-%m-%d %H:%M:%S")
			lctime2 = strftime("%Y-%m-%d %H:%M:%S", localtime(timegm(lctimeT)))
			self.liststore.append( [list_item['workiz'], list_item['phnumber'], list_item['cust_name'], list_item['id'], lctime2, list_item['action'], list_item['result'], lenstr2] )

		db_list = self.db.search( (workizq.workiz == True) )
		for list_item in (db_list):
			lenstr = str((int(list_item['length'])/60))
			lenstr2 = lenstr[:lenstr.find(".")+3]
			lctime = list_item['date_time'].replace("T", " ").replace("Z", "")
			lctimeT = strptime(lctime[:lctime.find(".") ], "%Y-%m-%d %H:%M:%S")
			lctime2 = strftime("%Y-%m-%d %H:%M:%S", localtime(timegm(lctimeT)))
			self.liststore2.append( [list_item['workiz'], list_item['phnumber'], list_item['cust_name'], list_item['id'], lctime2, list_item['action'], list_item['result'], lenstr2] )

		self.liststore.set_sort_column_id(4, 1)
		self.liststore2.set_sort_column_id(4, 1)
		

	def on_subscription(self, widget=''):
		#res = self.platform.get('/account/~/phone-number')
		#list1 = res.json().records[0].phoneNumber
		#liststr = str(list1)
		#print('Phone Number: ' + liststr )

		#res = self.platform.get('/account/~/extension/' + RINGCENTRAL_EXT + '/call-log')
		res = self.platform.get('/account/~/call-log')
		#res = msg
		#print(res.json().records)
		
		idq_rc = Query()

		for record in res.json().records:
			db_list = self.db.search( (idq_rc.id == record.sessionId) )
			if not db_list:
				#if not record.from_.name:
				if not hasattr(record.from_, "name"):
					cust_name = 'CUSTOMER'

				#if 1 == 1:
				if record.to.phoneNumber == RINGCENTRAL_PHONE:
					self.db.insert( {
						'id':record.sessionId, 
						'workiz':False, 
						'phnumber':record.from_.phoneNumber, 
						'cust_name':cust_name,
						'date_time':record.startTime,
						'length':str(record.duration),
						'action':record.action,
						'result':record.result
					} )

		self.read_database()

win = MyWindow()
#win.liststore.append([True, "+asdf", "wahwahwah"])
win.connect("destroy", Gtk.main_quit)
win.show_all()

Gtk.main()




