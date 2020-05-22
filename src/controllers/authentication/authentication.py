from flask import render_template, request, redirect, url_for
from src.db import db

class AuthenticationController:
    @staticmethod
    def register():
        return render_template("authentication/register.html")