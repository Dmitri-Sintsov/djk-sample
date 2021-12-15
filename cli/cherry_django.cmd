if defined DJANGO_DEBUG (
set _DJANGO_DEBUG=%DJANGO_DEBUG%
)
set DJANGO_DEBUG='False'

if defined CHERRYPY_STATIC (
set _CHERRYPY_STATIC=%CHERRYPY_STATIC%
)
set CHERRYPY_STATIC='True'

python %VIRTUAL_ENV%/djk-sample/cherry_django.py

if defined _DJANGO_DEBUG (
set DJANGO_DEBUG=%_DJANGO_DEBUG%
) else (
set DJANGO_DEBUG=
)

if defined _CHERRYPY_STATIC (
set CHERRYPY_STATIC=%_CHERRYPY_STATIC%
) else (
set CHERRYPY_STATIC=
)
