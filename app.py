from flask import Flask, render_template, request, redirect, url_for

from db.connection import get_connection

from decimal import Decimal, InvalidOperation

app = Flask(__name__)


def get_publishers():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name
                FROM publishers
                WHERE active = TRUE
                ORDER BY name;
            """)

            return cursor.fetchall()


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


@app.route("/games")
def games():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT
                    games.title,
                    games.platform,
                    games.stock_quantity,
                    games.buying_cost,
                    games.selling_price,
                    publishers.name
                FROM games
                JOIN publishers
                    ON games.publisher_id = publishers.id;
            """)

            game_list = cursor.fetchall()

    return render_template("games.html", games=game_list)


@app.route("/games/new", methods=["GET", "POST"])
def add_game():
    if request.method == "POST":
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        platform = request.form["platform"].strip()

        if not title or not platform:
            return render_template(
                "add_game.html",
                publishers=get_publishers(),
                error="Game title and platform are required",
                form_data=request.form
            ), 400

        try:
            stock_quantity = int(request.form["stock_quantity"])
            buying_cost = Decimal(request.form["buying_cost"])
            selling_price = Decimal(request.form["selling_price"])
            publisher_id = int(request.form["publisher_id"])

        except (ValueError, InvalidOperation):
            return render_template(
                "add_game.html",
                publishers=get_publishers(),
                error="Please enter valid numbers and select a publisher.",
                form_data=request.form
            ), 400

        if stock_quantity < 0:
            return render_template(
                "add_game.html",
                publishers=get_publishers(),
                error="Stock quantity cannot be negative.",
                form_data=request.form
            ), 400

        if (
            not buying_cost.is_finite()
            or not selling_price.is_finite()
            or buying_cost < 0
            or selling_price < 0
        ):
            return render_template(
                "add_game.html",
                publishers=get_publishers(),
                error="Prices must be valid, non-negative numbers.",
                form_data=request.form
            ), 400

        if publisher_id <= 0:
            return render_template(
                "add_game.html",
                publishers=get_publishers(),
                error="Please select a valid publisher.",
                form_data=request.form
            ), 400

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM publishers WHERE id = %s AND active = TRUE;",
                    (publisher_id,)
                )
                publisher = cursor.fetchone()

        if publisher is None:
            return render_template(
                "add_game.html",
                publishers=get_publishers(),
                error="The selected publisher does not exist or is inactive.",
                form_data=request.form
            ), 400

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO games (
                        title,
                        description,
                        platform,
                        stock_quantity,
                        buying_cost,
                        selling_price,
                        publisher_id
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                """, (
                    title,
                    description,
                    platform,
                    stock_quantity,
                    buying_cost,
                    selling_price,
                    publisher_id
                ))

        return redirect(url_for("games"))

    return render_template("add_game.html", publishers=get_publishers())
