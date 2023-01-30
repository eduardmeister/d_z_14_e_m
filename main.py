from flask import Flask, jsonify
import utils
#
app = Flask(__name__)


@app.route('/movie/<title>')
def movie_page(title):
    movie_data = utils.get_movie_by_title(title)
    return jsonify(movie_data)


@app.route('/movie/<int:start_year>/to/<int:finish_year>')
def movies_from_years_page(start_year, finish_year):
    movies_data = utils.get_movies_by_years(start_year, finish_year)
    return jsonify(movies_data)


@app.route('/rating/<value>')
def rating_page(value):
    movies_data = utils.get_movies_by_rating(value)
    return jsonify(movies_data)


@app.route('/genre/<genre>')
def genre_page(genre):
    movies_data = utils.get_movies_by_genre(genre)
    return jsonify(movies_data)


@app.route('/')
def index_page():
    query = "SELECT * FROM netflix"
    movies_data = utils.get_data_from_the_table(query)
    return jsonify(movies_data)


if __name__ == '__main__':
    app.run(port=5003)
