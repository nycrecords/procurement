# views.py
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from . import user
from ..models import Vendor
