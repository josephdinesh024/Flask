from letdeal import app
# from admin import admin_app,db

if __name__ == "__main__":
    # with admin_app.app_context():
    #     db.create_all()
    app.run(debug=True,port=1234)
    #admin_app.run(debug=True)
