#!/usr/bin/env python3

import psycopg2

DBNAME = "news"

POPULAR_ARTICLES = """
SELECT a.title, COUNT(l.*) AS views
FROM log l
JOIN articles a ON CONCAT('/article/', a.slug) = l.path
WHERE l.status = '200 OK'
GROUP BY l.path, a.title
ORDER BY views DESC
LIMIT 3;
"""
POPULAR_AUTHORS = """
SELECT t.name, COUNT(l.*) AS views
FROM log l
JOIN articles a ON CONCAT('/article/', a.slug) = l.path
JOIN authors t ON a.author = t.id
WHERE l.status = '200 OK'
GROUP BY t.name
ORDER BY views DESC;
"""
ERROR_PCT = """
WITH
    TOTAL AS (SELECT DATE(l.time) AS day, count(l.*)
        FROM log l GROUP BY DATE(l.time) ORDER BY DATE(l.time)),
    ERRORS AS (SELECT DATE(l.time) AS day, count(l.*)
        FROM log l
        WHERE l.status != '200 OK'
        GROUP BY DATE(l.time)
        ORDER BY DATE(l.time)),
    PCT AS (SELECT TOTAL.day,
        ERRORS.count::NUMERIC / TOTAL.count ::NUMERIC * 100 AS ERROR_PCT
        FROM TOTAL,
        ERRORS
        WHERE TOTAL.day = ERRORS.day)
    SELECT day, TRUNC(ERROR_PCT, 2)
FROM PCT
    WHERE ERROR_PCT > 1
    ORDER BY ERROR_PCT;
"""


def executeQuery(query):
    conn = psycopg2.connect(
        dbname=DBNAME)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


def getMostPopularArticles():
    """Get the three most popular articles and the amount of views."""
    return executeQuery(POPULAR_ARTICLES)


def getMostPopularAuthors():
    """Get the autors and sum of views of your articles,
     sorted by the amount of views."""
    return executeQuery(POPULAR_AUTHORS)


def getErrorPercentile():
    """Show which days has more than 1% of
     errors and the percentage of error."""
    return executeQuery(ERROR_PCT)


def main():
    print("1. What are the most popular three articles of all time?\n")
    for title, views in getMostPopularArticles():
        print('{} - {:,} views.'.format(title, views))

    print("\n")
    print("2. Who are the most popular article authors of all time?\n")
    for author, views in getMostPopularAuthors():
        print('{} - {:,} views.'.format(author, views))

    print("\n")
    print("3. On which days did more than 1% of requests lead to errors?\n")
    for day, error_pct in getErrorPercentile():
        print('{} - {:,}% errors.'.format(day, error_pct))


if __name__ == '__main__':
    main()
