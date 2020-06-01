from src.controllers import render

class UserController:
    @staticmethod
    def index(username):
        return render("users/main.html")
