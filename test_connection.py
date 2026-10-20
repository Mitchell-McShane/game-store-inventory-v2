from db.connection import get_connection

with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT title, platform, stock_quantity FROM games;"
        )

        games = cursor.fetchall()

        for game in games:
            print(game)
