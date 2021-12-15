if not defined DENO_INSTALL (
set DENO_INSTALL=%USERPROFILE%\.deno
)

if defined DJANGO_DEBUG (
set _DJANGO_DEBUG=%DJANGO_DEBUG%
)
set DJANGO_DEBUG='False'

python %VIRTUAL_ENV%/djk-sample/manage.py collectrollup --noinput --clear

if defined _DJANGO_DEBUG (
set DJANGO_DEBUG=%_DJANGO_DEBUG%
) else (
set DJANGO_DEBUG=
)
