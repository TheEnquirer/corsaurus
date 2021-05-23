#!/bin/sh
cd app_holder/corsaurus/backend_
source .venv/bin/activate
uwsgi --ini uwsgi.ini

