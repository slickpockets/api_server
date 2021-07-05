#!/usr/bin/env python
import os
import subprocess
from flask import Flask

from app import create_app, db


app = create_app(os.getenv('FLASK_CONFIG') or 'development')


if __name__ == '__main__':
    Flask.run(app, debug=True)
