#!/usr/bin/env python
import os
import subprocess

from flask_script import Manager, Server, Shell

from app import create_app, db
def make_shell_context():
    return dict(app=app, db=db)


app = create_app(os.getenv('FLASK_CONFIG') or 'development')
manager = Manager(app)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(host="0.0.0.0", port=5000))


if __name__ == '__main__':
    manager.run()
