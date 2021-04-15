#!/bin/sh
cd app_holder/corsaurus/backend_
source bin/activate
uwsgi --ini uwsgi.ini

