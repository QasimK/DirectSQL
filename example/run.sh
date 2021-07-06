#!/bin/sh

uwsgi \
	--http 127.0.0.1:9091 \
	--single-interpreter \
	--need-app \
	--honour-stdin \
	--wsgi-file app.py
