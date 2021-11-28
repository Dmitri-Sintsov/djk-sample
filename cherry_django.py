#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import webbrowser
from threading import Timer
import django
import cherrypy
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler

os.environ["DJANGO_SETTINGS_MODULE"] = "djk_sample.settings"
# tdir = os.path.abspath(os.path.dirname(__file__))
django.setup()


class DjangoApplication:
    HOST = "127.0.0.1"
    PORT = 8001

    def mount_static(self, url, root):
        """
        :param url: Relative url
        :param root: Path to static files root
        """
        config = {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': root,
            'tools.expires.on': True,
            'tools.expires.secs': 86400
        }
        cherrypy.tree.mount(root=None, script_name=url, config={'/': config})

    def open_browser(self):
        Timer(3, webbrowser.open, ("http://%s:%s" % (self.HOST, self.PORT),)).start()

    def run(self):
        # https://stackoverflow.com/questions/35443289/prevent-cherrypy-from-automatically-reloading#
        cherrypy.config.update({
            'server.socket_host': self.HOST,
            'server.socket_port': self.PORT,
            # 'server.ssl_module': 'builtin',
            # 'server.ssl_certificate': os.path.join(tdir, 'ssl_cert.pem'),
            # 'server.ssl_private_key': os.path.join(tdir, 'ssl_key.pem'),
            'engine.autoreload.on': settings.DEBUG,
            'log.screen': True,
            # 'response.stream': True,
            'server.max_request_body_size': 1000 * 1024 * 1024,
            'server.socket_timeout': 60,
        })

        if settings.DEBUG:
            # Do not forget to run ./manage.py collectstatic
            self.mount_static(settings.STATIC_URL, settings.STATIC_ROOT)

        cherrypy.log("Loading and serving Django application")
        cherrypy.tree.graft(WSGIHandler())
        cherrypy.engine.start()

        # if settings.DEBUG:
        #     self.open_browser()

        cherrypy.engine.block()


if __name__ == "__main__":
    DjangoApplication().run()
