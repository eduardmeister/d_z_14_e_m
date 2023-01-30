import sqlite3
from flask import jsonify

#
def get_data_from_the_table(query):
    """Принимает параметры запроса к sql и возвращает данные"""

    with sqlite3.connect('netflix.db') as con:
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result



def get_movie_by_title(movie_name):
    """Принимает название фильма и возвращает словарь с данными о нём"""

    query = (f"""
                SELECT title, country, release_year, listed_in, description
                FROM netflix
                WHERE title LIKE '{movie_name}'
                GROUP BY release_year, title
                ORDER BY release_year DESC
                LIMIT 1
                """)

    result = get_data_from_the_table(query)[0]

    movie_data = {
        "title": result[0],
        "country": result[1],
        "release_year": result[2],
        "genre": result[3],
        "description": result[4]
    }
    return movie_data



def get_movies_by_years(start_year, finish_year):
    """ Принимает стартовый год и конечный.
    Возвращает список словарей с названияит и годами выпуска фильмов."""

    if start_year > finish_year:
        return "DATA ERROR"
    query = (f"""
                SELECT title,release_year
                FROM netflix
                WHERE "type" = 'Movie'
                AND release_year BETWEEN {start_year} AND {finish_year}
                LIMIT 100
                """)
    result = get_data_from_the_table(query)
    movies_data = [{'title': movie[0], 'release_year': movie[1]} for movie in result]

    return movies_data


def get_movies_by_rating(value):
    """Принимает рейтинг и возращает список словарей
    с названиями, рейтингом и описаниями фильмов """

    query = """
                SELECT title, rating, description
                FROM netflix
                """

    if value == 'children':
        query += 'WHERE rating = "G"'
    elif value == 'family':
        query += 'WHERE rating = "G" or rating = "PG" or rating = "PG-13"'
    elif value == 'adult':
        query += 'WHERE rating = "R" or rating "NC-17"'
    else:
        return jsonify(status=400)

    movies_data = get_data_from_the_table(query)
    result = []
    for movie in movies_data:
        dict_data = {
            'title': movie[0],
            'rating': movie[1],
            'description': movie[2],
            }
        result.append(dict_data)
    return result

def get_movies_by_genre(genre):
    """Принимает жанр и возращает список словарей
        с названиями и описаниями фильмов"""

    query = f"""
                SELECT title, description
                FROM netflix
                WHERE listed_in LIKE '%{genre}%'
                ORDER BY release_year DESC
                LIMIT 10
                """
    movies_data = get_data_from_the_table(query)

    result = [{'title': movie[0], 'description': movie[1]} for movie in movies_data]
    return result

def get_my_dudes(dude_1, dude_2):
    """Получает в качестве аргумента имена двух актеров,
    сохраняет всех актеров из колонки cast и возвращает список тех,
    кто играет с ними в паре больше 2 раз"""

    query = f"""
    SELECT "cast"
    FROM netflix
    WHERE "cast" LIKE '%{dude_1}%'AND "cast" LIKE '%{dude_2}%'    
    """

    movies_data = get_data_from_the_table(query)
    actors =[]

    for tuple_cast in movies_data:
        for str_actors in tuple_cast:
            actors.append(str_actors)

    my_dudes = []

    for str_actors in actors:
        my_dudes += str_actors.split(', ')

    for dude in my_dudes:
        if my_dudes.count(dude) > 3 or dude == dude_1 or dude == dude_2:
                my_dudes.remove(dude)


    return [dude for dude in set(my_dudes)]


def search_movies(type, release_year, genre):
    """Получает тип картины (фильм или сериал), год выпуска и ее жанр.
    Возвращает список названий картин с их описаниями в JSON"""

    query = f"""
                SELECT title, description
                FROM netflix
                WHERE "type" = '{type}'
                AND release_year = {release_year}
                AND listed_in LIKE '%{genre}%'   
                """

    movies_data = get_data_from_the_table(query)
    return jsonify(movies_data)


