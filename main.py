import sqlite3

import flask


def run_sql(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row

        return connection.execute(sql).fetchall()


def search_by_name(title):
    sql = f'''SELECT title, country, release_year, listed_in AS genre, description 
          FROM netflix 
          WHERE title='{title}'
          ORDER BY date_added DESC 
          limit 1'''
    result = None
    for item in run_sql(sql):
        result = dict(item)

    return flask.jsonify(result)


def range_of_years_of_release(year1, year2):
    sql = f'''SELECT title, release_year
          FROM netflix 
          WHERE release_year
          BETWEEN {year1} AND {year2} 
          ORDER BY release_year DESC 
          '''
    result = []
    for item in run_sql(sql):
        result.append(dict(item))

    return flask.jsonify(result)


def search_by_rating(rating):
    my_dict = {
        "children": ("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }
    sql = f'''SELECT title, rating, description
          FROM netflix 
          WHERE rating IN {my_dict.get(rating, ('G', 'PG'))}         
          '''
    result = []
    for item in run_sql(sql):
        result.append(dict(item))

    return flask.jsonify(result)


def search_by_genre(genre):
    sql = f'''SELECT title, description
          FROM netflix 
          WHERE listed_in
          LIKE '%{genre.title()}%'
          '''
    result = []
    for item in run_sql(sql):
        result.append(dict(item))

    return flask.jsonify(result)


def search_by_actors(name1, name2):
    sql = f'''SELECT "cast"
          FROM netflix 
          WHERE "cast"
          LIKE '%{name1}%' AND "cast"
          LIKE '%{name2}%'
          '''
    result = []
    for item in run_sql(sql):
        result.append(dict(item))

    main_name = {}
    for item in result:
        name = item.get('cast').split(", ")
        for names in name:
            if names in main_name.keys():
                main_name[names] += 1
            else:
                main_name[names] = 1

    total = []
    for item in main_name:
        if item not in (name1, name2) and main_name[item] >= 2:
            total.append(item)

    return total


def search_by_all(typ, year, genre):
    sql = f"""
          SELECT title, description
          FROM netflix 
          WHERE type = {typ}
          AND release_year = {year}
          AND listed_in LIKE '%{genre}%'
          """
    result = []
    for item in run_sql(sql):
        result = dict(item)

    return flask.jsonify(result)

