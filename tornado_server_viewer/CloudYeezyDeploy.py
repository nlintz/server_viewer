import os.path
import os

import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import urllib2

import ui_methods


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
	
	def get(self):
		FileNames=list(os.walk(os.path.join(os.path.dirname(__file__), "/home/pybros/downloads")))[0][2]
		FileSizes=[os.path.getsize("/home/pybros/downloads/"+file) for file in FileNames],
		FilePriority=["file-element-priority-high" for i in FileNames],

		self.render(
		'index.html',
		title="Cloud Yeezy",
		# fileNames = list(os.walk(os.path.join(os.path.dirname(__file__), "downloads")))[0][2],
		fileNames = FileNames,
		lessURI = "static/stylesheets/styles.less",
		pageSetupJSURI = "static/javascript/pageSetupJS.js",
		# fileSizes=[os.stat("static/testfiles/"+file).st_size for file in FileNames],
		# fileSizes=os.stat("static/testfiles/test.txt").st_size
		fileSizes=FileSizes[0],
		fileData = zip(list(FileNames),(FileSizes[0]), FilePriority[0]),
		filePriority = FilePriority,
		# downloadsURI = os.path.join(os.path.dirname(__file__), "/home/pybros/downloads")
		downloadsURI = "http://95.211.155.71/~pybros/downloads"


		)

		print fileSizes

class fileTransfer(tornado.web.RequestHandler):
	def get(self):
		return
	# 	self.set_status(200)
	# 	self.set_header("Content-Disposition","attachment; filename = static/testfiles/test.")
	# 	# self.set_header('Content-type', 'audio/mpeg')
	# 	# response = urllib2.urlopen('static/testfiles/test.txt')
	# 	# File = open('static/testfiles/test.txt', 'rb')
	# 	# self.write(response.read())
	# 	# self.write(File.read())
	# 	# File.close()
	# 	self.finish()


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/getFile", fileTransfer),
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
