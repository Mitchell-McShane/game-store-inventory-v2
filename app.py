from flask import Flask, render_template

from db.connection import get_connection

app = Flask(__name__)


@app.route("/")
def home():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM games;")
            total_games = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM games WHERE stock_quantity BETWEEN 1 AND 5;"
            )
            low_stock = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM games WHERE stock_quantity = 0;"
            )
            out_of_stock = cursor.fetchone()[0]

    return render_template("index.html", total_games=total_games, low_stock=low_stock, out_of_stock=out_of_stock)
