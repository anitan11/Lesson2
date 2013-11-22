# -*- coding: utf-8 -*-

import os
import re
import string
import codecs

import webapp2
import jinja2

from sets import Set

web_dir = os.path.join(os.path.dirname(__file__), 'web')
JINJA_ENVIRONMENT = jinja2.Environment(loader = jinja2.FileSystemLoader(web_dir), autoescape=True)

def render_str(template, **params):
	t=JINJA_ENVIRONMENT.get_template(template)
	return t.render(params)

class MainHandler(webapp2.RequestHandler):
	
	def render(self, template, **kw):
		self.response.write(render_str(template, **kw))
		
	def write(self, *a, **kw):
		self.response.write(*a, **kw)
		
class Rot13(MainHandler):
		
	utf_chars = Set('ÆØÅ')
	def check(self, text):
		text = text.decode('utf-8', 'ignore')
		if Set(text).issubset(self.utf_chars): #will not handle non-ascii
			return False
		else:
			return True
	
	def get(self):
		self.render('rot13.html')
		
	def post(self):
		rot13 = ''
		text = self.request.get('text')
		text = text.encode('utf-8', 'strict')
		rot13 = text.encode('rot13')
		error = ""
		
		
		#if self.check(text):
			#rot13 = text.encode('rot13') #will not handle non-ascii
			#error = ""
		#elif not self.check(text):
			#utf_8_dict = {'æ': 'ae', 'ø': 'o', 'å': 'aa'}
			#jinja2.string(text) 
			#text.replace('æ', 'ae') #will not handle non-ascii
			#text = text.decode('utf-8', 'ignore')
			#rot13 = text
			#error = "Remember, remember the fifth of November? Hint: Look further up!"

		self.render('rot13.html', text = rot13, error = error) #fuck non-ascii!!!!! fuck Python!!!!!!
		
class Signup (MainHandler):
	
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	PASS_RE = re.compile(r"^.{3,20}$")
	EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
	
	def valid_username(self, username):
		return username and USER_RE.match(username)

	def valid_password(self, password):
		return password and PASS_RE.match(password)

	def valid_email(self, email):
		return not email or EMAIL_RE.match(email)
	
	def get(self):
		self.render("signup-form.html")
	
	def post(self):
		have_error=False
		username = self.request.get('username')		
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')
		
		params = dict(username = username, email = email)
		
		if not self.valid_username(username):
			params['error_username'] = "That's not a valid username."
			have_error = True
		
		if not self.valid_password(password):
			params['error_password'] = "That wasn't a valid password."
			have_error = True
		elif password !=verify:
			params['error_verify'] = "Your passwords didn't match."
			have_error = True
		
		if not self.valid_email(email):
			params['error_email'] = "That's not a valid email."
			have_error = True
			
		if have_error:
			self.render('signup-form.html', **params)
		else:
			self.redirect('welcome?username=' + username)
		
class Welcome(MainHandler):
	def get(self):
		username = self.request.get('username')
		if valid_username(username):
			self.render('welcome.html', username=username)
		else:
			self.redirect('/signup')
	
app = webapp2.WSGIApplication([('/rot13', Rot13), ('/signup', Signup),	('/welcome', Welcome)], debug=True)
