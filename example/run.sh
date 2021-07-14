#!/bin/sh

uwsgi \
	--http 127.0.0.1:9091 \
	--strict ${IFS# Raise errors with uWSGI config} \
	--need-app ${IFS# Raise errors with app init} \
	--single-interpreter \
	--vacuum \
	--honour-stdin ${IFS# Allow debugging prompts in terminal} \
	--enable-threads \
	--wsgi-file app.py
