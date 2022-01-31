from urllib import parse
from flask import Flask, render_template, request, redirect, url_for
from flask.wrappers import Request
import mysql.connector
from mysql.connector.pooling import PooledMySQLConnection

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="40.117.248.43",
    user="root",
    password="Pass@123r",
    port=3306,
    database="movieapp"
)

print(mydb)
mycursor = mydb.cursor()


@app.route("/")
def index():
    return redirect(url_for('movie_list'))

# Movie List

# @app.template_filter(name='get_search_params')

# @app.template_filter("get_search_parms")
# def get_search_params(url, key):
#     temp = dict(parse.parse_qsl(url))
#     return temp.get(key, False)


@app.route("/movie_list", methods=['GET', 'POST'])
def movie_list():
    curr_page = request.args.get('page_no')
    order = request.args.get('order')
    sortby = request.args.get('type')

    if sortby is None:
        sortby = "id"

    print(order)
    print(sortby)
    print(curr_page)
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
        offset = (curr_page-1) * limit
        if order == "desc":
            # sql = "SELECT * FROM movies_list LIMIT %s, %s"
            sql = "SELECT * FROM movies_list ORDER BY " + sortby + " DESC LIMIT %s, %s"
        else:
            sql = "SELECT * FROM movies_list ORDER BY " + sortby + " LIMIT %s, %s"

    val = (offset, limit)
    mycursor.execute(sql, val)
    # mycursor.execute(sql)
    print(mycursor.statement)

    myresult = mycursor.fetchall()

    return render_template("/movie_list.html", data=myresult, curr_page=curr_page)

# Movie Add


@app.route("/add_movie", methods=['GET', 'POST'])
def add_movie():
    if request.method == "POST":
        movie_name = request.form.get('Movie_name')
        director_name = request.form.get('Director_name')
        genres = request.form.get('Genres')
        release_date = request.form.get('Release_date')
        running_time = request.form.get('Running_time')

        print("Movie_Name:", movie_name)
        print("Director_Name", director_name)
        print("Genres", genres)
        print("Release_Date", release_date)
        print("Running_Time", running_time)

        sql = "INSERT INTO movies_list (movie_name, director_name, genres, release_date, running_time) VALUES (%s, %s, %s, %s, %s)"

        val = (movie_name, director_name, genres, release_date, running_time)

        mycursor.execute(sql, val)

        mydb.commit()

        print(mycursor.rowcount, "record inserted.")

        return redirect(url_for("movie_list"))

    return render_template("/add_movie.html")

# Edit Movie


@app.route("/edit_movie/<id>", methods=['GET', 'POST'])
def edit_movie(id):
    print(id)

    if request.method == "POST":
        movie_name = request.form.get('Movie_name')
        director_name = request.form.get('Director_name')
        genres = request.form.get('Genres')
        release_date = request.form.get('Release_date')
        running_time = request.form.get('Running_time')

        sql = "UPDATE movies_list SET movie_name = %s, director_name= %s, genres= %s, release_date= %s, running_time= %s  WHERE id = %s"

        val = (movie_name, director_name, genres,
               release_date, running_time, id)

        mycursor.execute(sql, val)

        mydb.commit()

        return redirect(url_for("movie_list"))

    else:
        sql = "SELECT * FROM movies_list WHERE id= %s"
        val = (id,)

        mycursor.execute(sql, val)

        doc = mycursor.fetchone()

        print(doc)

        return render_template("/edit_movie.html", movie=doc)

# Delete Movie


@app.route("/delete_movie/<id>", methods=['POST'])
def delete_movie(id):
    if request.method == "POST":
        sql = "DELETE FROM movies_list WHERE id = %s"
        val = (id,)

        mycursor.execute(sql, val)

        mydb.commit()

        return redirect(url_for("movie_list"))

# View Movie


@app.route("/view_movie/<id>", methods=['GET'])
def view_movie(id):
    sql = "SELECT * FROM movies_list WHERE id = %s"
    val = (id,)

    mycursor.execute(sql, val)

    doc = mycursor.fetchone()

    return render_template("/view_movie.html", movie=doc)

# Search


@app.route("/search")
def search():
    curr_page = request.args.get('page_no')
    order = request.args.get('order')
    sortby = request.args.get('type')
    q = request.args.get('search')
    print("Search:", q)
    print("Current_Pg:", curr_page)
    print("Order:", order)
    print("SortBy:", sortby)

    if q is None and curr_page is None:
        curr_page = 1
        # curr_page = int(curr_page)
        if order == "desc":
            mycursor.execute(
                "SELECT * FROM movies_list ORDER BY " + sortby + " DESC")

        # mycursor.execute("SELECT * FROM movie_list ")
        myresult = mycursor.fetchall()

        print("Search_Result:", myresult)

        return render_template("/movie_list.html", data=myresult, curr_page=curr_page)
    else:
        curr_page = 1
        mycursor.execute(
            "SELECT * FROM movies_list WHERE movie_name LIKE CONCAT('%', %s, '%') ", (q,))

        print(mycursor.statement)

        myresult = mycursor.fetchall()
        return render_template("/movie_list.html", data=myresult, curr_page=curr_page)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
