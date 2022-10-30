import flask

from main import search_by_name, range_of_years_of_release, search_by_rating, search_by_genre, search_by_actors, \
    search_by_all

app = flask.Flask(__name__)


@app.route("/movie/<title>")
def movie_title(title):
    '''поиск по названию'''
    result = search_by_name(title)
    return result


@app.route("/movie/year/<int:year1>/to/<int:year2>")
def movie_year(year1, year2):
    '''поиск по диапазону лет выпуска'''
    result = range_of_years_of_release(year1, year2)
    return result


@app.route("/movie/rating/<rating>")
def movie_rating(rating):
    '''поиск по рейтингу'''
    result = search_by_rating(rating)
    return result


@app.route("/movie/genre/<genre>")
def movie_genre(genre):
    '''список название и описание каждого фильма'''
    result = search_by_genre(genre)
    return result


@app.route("/movie/actors/<name1>/to/<name2>")
def movie_actors(name1, name2):
    '''список тех, кто играет с ними в паре больше 2 раз'''
    result = search_by_actors(name1, name2)
    return result


app.run(debug=True)

