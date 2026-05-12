"""WSGI entry point used by the django-framework rock/charm.

Bridges the paas-charm DJANGO_* env convention to the variable names that
dpaste.settings.base reads directly (no DJANGO_ prefix).  The bridges use
setdefault so an operator can still supply the unprefixed names if needed.

This module is used instead of dpaste.wsgi so that the defaults are correct
before Django settings are evaluated.
"""
import os

# Settings module – must resolve before any Django import.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dpaste.settings.base")

# Bridge paas-charm injected names to the names dpaste.settings.base reads.
_BRIDGES = {
    "DJANGO_DEBUG": "DEBUG",
    "DJANGO_SECRET_KEY": "SECRET_KEY",
    "DJANGO_ALLOWED_HOSTS": "ALLOWED_HOSTS",
    # User-defined app-url-prefix charm config → APP_URL_PREFIX → URL_PREFIX
    "APP_URL_PREFIX": "URL_PREFIX",
}
for _src, _dst in _BRIDGES.items():
    if _src in os.environ and _dst not in os.environ:
        os.environ[_dst] = os.environ[_src]

# Bridge the postgresql relation connect-string to DATABASE_URL.
if "DATABASE_URL" not in os.environ:
    _pg = os.environ.get("POSTGRESQL_DB_CONNECT_STRING")
    if _pg:
        os.environ["DATABASE_URL"] = _pg

# Static files pre-collected at rock build time.
os.environ.setdefault("STATIC_ROOT", "/django/app/staticfiles")

from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
