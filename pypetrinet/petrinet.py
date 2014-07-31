import cherrypy
from cherrypy.lib.static import serve_file
from  cherrypy.lib import sessions
from cherrypy import _cperror
from cherrypy import tools
import functools
import numpy as np
import os
import webbrowser
from jinja2 import Environment, FileSystemLoader

from corepetrinet import PetriNet

sess = sessions
PATH = os.path.join(os.path.abspath("."), u"media")
env = Environment(loader=FileSystemLoader('media'))

#Посмотреть макросы в jinja
class HelloWeb:
	#http://jinja.pocoo.org/docs/
	@cherrypy.expose
	def index(self):
		p = PetriNet(['s1', 's2', 's3', 's4'], ['t1', 't2', 't3'])
		p.connect('t3', [(2,'s2'), 's4'], [(2,'s1'), 's3'])
		p.connect('t1', ['s1'], ['s2'])
		p.connect('t2', ['s3'], ['s4'])
		#p.add_property(place=['s1', 's2', 's3', 's4'], moves=moves)
		#p.add_property(ins = [['s1', 't1', 's2'], ['s3', 't2', 's4']])
		#Add template
		tmpl = env.get_template('petri.html')
		#return open(os.path.join(PATH, u'petri.html'))
		return tmpl.render(pos=list(range(0,4 * 1000,300)), names=['t1', 't2', 't3'], \
			circles=['s1', 's2', 's3', 's4'], circlepos = list(range(0,4 * 1000,300)),\
			lines = p.web_output())

	@cherrypy.expose
	def create(self):
		return "Under construction"

	@cherrypy.expose
	def stream(self):
		return "<html><head><body><h3>Nice</h3></body></head></html>"

	@cherrypy.expose
	def ident(self):
		return "VALUE"

	@cherrypy.expose
	def petri(self):
		tmpl = env.get_template('petri.html')
		return tmpl.render()

	index.exposed = True


def handle_error():
	cherrypy.response.status = 500
	cherrypy.response.body = ["<html><body>Sorry, an error occured</body></html>"]

class Root:
	_cp_config = {'request.error_response': handle_error}


cherrypy.tree.mount(Root(), '/', config={
        '/': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': PATH,
                'tools.staticdir.index': '.s/index.html',
            },
    })

def test_petrinet_builder():
	p = PetriNet()
	p.add_property(place=['s1', 's2', 's3', 's4'], moves=['t1', 't2', 't3'])
	p.add_property(ins = [['s1', 't1', 's2'], ['s3', 't2', 's4']])
	p.connect('s1', 't1')
	p.connect({'s1': ['t1', 't2']})


config = {'/media': {
	'tools.staticdir.on': True,
	'tools.staticdir.dir': PATH,
}

	
}

cherrypy.tree.mount(HelloWeb(), '/', config=config)
cherrypy.engine.start()


