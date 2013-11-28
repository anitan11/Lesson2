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

#see lesson 5 for comments
def render_str(template, **params):
	t=JINJA_ENVIRONMENT.get_template(template)
	return t.render(params)

class MainHandler(webapp2.RequestHandler):
	
	#see lesson 5 for comments
	def render(self, template, **kw):
		self.response.write(render_str(template, **kw))
	#see lesson 5 for comments	
	def write(self, *a, **kw):
		self.response.write(*a, **kw)

#rot13
#This is the handler that handles the requests on /rot13. I've tried
#to make it able to handle utf8 and unicode, but no luck. Methods that
#worked for others, did somehow not work for me. The code that I have
#tried is still here. I spent 20 hours one week but did not still 
#manage to find a solution.
class Rot13(MainHandler):
		
	utf_chars = Set('ÆØÅ') 						#makes a set of the characters æ, ø and å
	#this function is part of a method that did not work
	def check(self, text): 
		text = text.decode('utf-8', 'ignore') 	#takes the text decodes it to utf-8 and ignores any errors.
		if Set(text).issubset(self.utf_chars): 	#if the characters in the set utf_chars is present in the text variable, 
			return False						#the function returns False
		else:									#if not
			return True							#the function returns true
	
	#simply renders the rot13.html when the /rot13 with any given parameters url is entered
	def get(self): 
		self.render('rot13.html')
		
	def post(self):
		rot13 = ''								#rot13 = empty sting
		text = self.request.get('text')			#text is set by the value in text field in rot13.html
		text = text.encode('utf-8', 'strict')	#text is encoded to utf-8 and any error messages is handled strictly. This is also default error handling.
		rot13 = text.encode('rot13')			#the rot13-encoded version of text is put in the variable rot13
		error = ""								#error= empty string
		
		#this is several methods that didn't work. All put in one. I tried them by commenting out the parts 
		#that I did not try when i worked on this issue.
		#if self.check(text):					#if text does not contains æ, ø or/and å
			#rot13 = text.encode('rot13') 		#encode text to rot13
			#error = ""							#error is set to empty string
		#elif not self.check(text):				#if text contaings æ, ø or/and å
			#utf_8_dict = {'æ': 'ae', 'ø': 'o', 'å': 'aa'}	#the æøå letters will be replaced by respictively ae, o and aa
			#text.replace('æ', 'ae') 			#tried the replace function found in string
			#text = text.decode('utf-8', 'ignore')	#tried to decode the utf-8. Also tried encode here
			#rot13 = text						#rot13 is set to the content of text
			#error = "Remember, remember the fifth of November? Hint: Look further up!" #The error variable is set to the given string

		#rot13.html is rendered. The parameters text as the variable rot13, and error as the variable error
		#is sent to the html-file.
		self.render('rot13.html', text = rot13, error = error) 	

#--------End rot13-----------

#see lesson 5 for comments	
class Signup (MainHandler):
	
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
	PASS_RE = re.compile(r"^.{3,20}$")
	EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
	
	def valid_username(self, username):
		return username and self.USER_RE.match(username)

	def valid_password(self, password):
		return password and self.PASS_RE.match(password)

	def valid_email(self, email):
		return not email or self.EMAIL_RE.match(email)
	
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
			self.redirect('/welcome?username=' + username)

#see lesson 5 for comments			
class Welcome(Signup):
	def get(self):
		username = self.request.get('username')
		if self.valid_username(username):
			self.render('/welcome.html', username=username)
		else:
			self.redirect('/signup')
	
#see lesson 5 for comments
app = webapp2.WSGIApplication([('/rot13', Rot13), ('/signup', Signup),	('/welcome', Welcome)], debug=True)
