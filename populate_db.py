import mysql.connector
from config import dbHost, dbuser, dbpasswd, dbport, db

mydb = mysql.connector.connect(host=dbHost, user=dbuser, password=dbpasswd, port=dbport, database=db)

mycursor = mydb.cursor()

sql = "INSERT INTO movies_list (movie_name, director_name, genres, release_date, running_time ) VALUES (%s, %s, %s, %s, %s)"

val = [
    ('The Shawshank Redemption', 'Frank Darabont', 'Drama', '1994-09-10', '142'),
    ('The Godfather', 'Francis Ford Coppola', 'Crime', '1972-03-24', '175'),
    ('The Dark Knight', 'Christopher Nolan', 'Action', '2008-07-18', '152'),
    ('The Godfather: Part II', 'Francis Ford Coppola', 'Crime', '1974-12-20', '202'),
    ('12 Angry Boys', 'Sidney Lumet', 'Drama', '1957-04-10', '96'),
    ('Schindler\'s List', 'Steven Spielberg', 'Biography', '1993-02-04', '195'),
    ('The Lord of the Rings: The Return of the King ', 'Peter Jackson', 'Adventure', '2003-12-17', '201'),
    ('Pulp Fiction', 'Quentin Tarantino', 'Crime', '1994-10-14', '154'),
    ('The Lord of the Rings: The Fellowship of the Ring', 'Peter Jackson', 'Adventure', '2001-12-19', '178'),
    ('Forrest Gump', 'Robert Zemeckis', 'Drama', '1994-07-06', '142'),
    ('Inception', 'Christopher Nolan', 'Action', '2010-07-16', '148'),
    ('The Lord of the Rings: The Two Towers', 'Peter Jackson', 'Adventure', '2002-12-18', '179'),
    ('Star Wars: Episode V - The Empire Strikes Back', 'Irvin Kershner', 'Action', '1980-06-20', '124'),
    ('The Matrix', 'Lana Wachowski', 'Action', '1999-03-31', '136'),
    ('Goodfellas', 'Martin Scorsese', 'Biography', '1990-09-21', '146'),
]

mycursor.executemany(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")

mydb.close()

mydb.disconnect()