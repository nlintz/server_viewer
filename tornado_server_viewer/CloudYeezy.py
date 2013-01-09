import os.path
import os

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import urllib2

import ui_methods
import oauthMain


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
	
	def get(self):
		FileNames=list(os.walk(os.path.join(os.path.dirname(__file__), "static/testfiles")))[0][2]
		FileSizes=[os.path.getsize("static/testfiles/"+file) for file in FileNames],
		FilePriority=["file-element-priority-high" for i in FileNames],

		self.render(
		'index.html',
		title="Cloud Yeezy",
		# fileNames = list(os.walk(os.path.join(os.path.dirname(__file__), "downloads")))[0][2],
		fileNames = FileNames,
		lessURI = "static/stylesheets/styles.less",
		pageSetupJSURI = "static/javascript/pageSetupJS.js",
		yeezyUtilsJSURI = "static/javascript/yeezyUtils.js",
		fitTextJSURI = "static/javascript/jquery.fittext.js",
		# fileSizes=[os.stat("static/testfiles/"+file).st_size for file in FileNames],
		# fileSizes=os.stat("static/testfiles/test.txt").st_size
		fileSizes=FileSizes[0],
		fileData = zip(list(FileNames),(FileSizes[0]), FilePriority[0]),
		filePriority = FilePriority,
		downloadsURI = "static/testfiles/"


		)

		print fileSizes

class oauth_request_token(tornado.web.RequestHandler):
	def get(self):
		(requestToken, appInfo, requestURL)=oauthMain.start_oauth()
		self.write(requestURL+" "+str(requestToken))


class oauth_access_token(tornado.web.RequestHandler):
	def get(self):		
		app_info = self.get_argument('app_info')
		request_token = self.get_argument('request_token')
		access_token=oauthMain.get_access_token(request_token, app_info)
	


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/oauth_request_token", oauth_request_token),
			(r"/oauth_access_token", oauth_access_token),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
			autoescape=None,
			ui_methods=ui_methods
			)
		tornado.web.Application.__init__(self, handlers, **settings)



def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
	main()
