from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from config import dbHost, dbuser, dbpasswd, dbport, db

app = Flask(__name__)

mydb = mysql.connector.connect(host=dbHost, user=dbuser, password=dbpasswd, port=dbport, database=db)

mycursor = mydb.cursor()


@app.route("/")
def index():
    return redirect(url_for("movie_list"))


# Favicon Icon
@app.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="favicon.ico"))


# Movie List

# @app.template_filter(name='get_search_params')

# @app.template_filter("get_search_parms")
# def get_search_params(url, key):
#     temp = dict(parse.parse_qsl(url))
#     return temp.get(key, False)


@app.route("/movie_list", methods=["GET", "POST"])
def movie_list():
    curr_page = request.args.get("page_no")
    order = request.args.get("order")
    sortby = request.args.get("type")

    if sortby is None:
        sortby = "id"

    sql = ""
    limit = 5
    offset = 0

    if curr_page is None:
        curr_page = 1
        offset = 0
        # sql = "SELECT * FROM movies_list LIMIT %s OFFSET %s"
        if order == "desc":
            sql = "SELECT * FROM movies_list ORDER BY " + sortby + " DESC LIMIT %s, %s"
        else:
            sql = "SELECT * FROM movies_list ORDER BY " + sortby + " LIMIT %s, %s"

    else:

        curr_page = int(curr_page)
        offset = (curr_page - 1) * limit
        if order == "desc":
            # sql = "SELECT * FROM movies_list LIMIT %s, %s"
            sql = "SELECT * FROM movies_list ORDER BY " + sortby + " DESC LIMIT %s, %s"
        else:
            sql = "SELECT * FROM movies_list ORDER BY " + sortby + " LIMIT %s, %s"

    val = (offset, limit)
    mycursor.execute(sql, val)

    myresult = mycursor.fetchall()

    return render_template("/movie_list.html", data=myresult, curr_page=curr_page)


# Movie Add
@app.route("/add_movie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        movie_name = request.form.get("Movie_name")
        director_name = request.form.get("Director_name")
        genres = request.form.get("Genres")
        release_date = request.form.get("Release_date")
        running_time = request.form.get("Running_time")

        sql = "INSERT INTO movies_list (movie_name, director_name, genres, release_date, running_time) VALUES (%s, %s, %s, %s, %s)"

        val = (movie_name, director_name, genres, release_date, running_time)

        mycursor.execute(sql, val)

        mydb.commit()

        return redirect(url_for("movie_list"))

    return render_template("/add_movie.html")


# Edit Movie
@app.route("/edit_movie/<id>", methods=["GET", "POST"])
def edit_movie(id):

    if request.method == "POST":
        movie_name = request.form.get("Movie_name")
        director_name = request.form.get("Director_name")
        genres = request.form.get("Genres")
        release_date = request.form.get("Release_date")
        running_time = request.form.get("Running_time")

        sql = "UPDATE movies_list SET movie_name = %s, director_name= %s, genres= %s, release_date= %s, running_time= %s  WHERE id = %s"

        val = (movie_name, director_name, genres, release_date, running_time, id)

        mycursor.execute(sql, val)

        mydb.commit()

        return redirect(url_for("movie_list"))

    else:
        sql = "SELECT * FROM movies_list WHERE id= %s"
        val = (id,)

        mycursor.execute(sql, val)

        doc = mycursor.fetchone()

        return render_template("/edit_movie.html", movie=doc)


# Delete Movie
@app.route("/delete_movie/<id>", methods=["POST"])
def delete_movie(id):
    if request.method == "POST":
        sql = "DELETE FROM movies_list WHERE id = %s"
        val = (id,)

        mycursor.execute(sql, val)

        mydb.commit()

        return redirect(url_for("movie_list"))


# View Movie Details
@app.route("/view_movie/<id>", methods=["GET"])
def view_movie(id):
    sql = "SELECT * FROM movies_list WHERE id = %s"
    val = (id,)

    mycursor.execute(sql, val)

    doc = mycursor.fetchone()

    return render_template("/view_movie.html", movie=doc)


# Search Movie
@app.route("/search")
def search():
    curr_page = request.args.get("page_no")
    order = request.args.get("order")
    sortby = request.args.get("type")
    q = request.args.get("search")

    if q is None and curr_page is None:
        curr_page = 1
        # curr_page = int(curr_page)
        if order == "desc":
            mycursor.execute("SELECT * FROM movies_list ORDER BY " + sortby + " DESC")

        # mycursor.execute("SELECT * FROM movie_list ")
        myresult = mycursor.fetchall()

        return render_template("/movie_list.html", data=myresult, curr_page=curr_page)
    else:
        curr_page = 1
        mycursor.execute("SELECT * FROM movies_list WHERE movie_name LIKE CONCAT('%', %s, '%') ", (q,))

        myresult = mycursor.fetchall()
        return render_template("/movie_list.html", data=myresult, curr_page=curr_page)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
