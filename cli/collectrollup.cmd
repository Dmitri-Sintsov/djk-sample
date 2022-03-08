if not defined DENO_INSTALL (
set DENO_INSTALL=%USERPROFILE%\.deno
)

set DJANGO_DEBUG=False

python %VIRTUAL_ENV%/djk-sample/manage.py collectrollup --noinput --clear
