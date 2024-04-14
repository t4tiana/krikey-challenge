from flask import Flask, jsonify, request
import psycopg2

app = Flask(__name__)

def db_connection():
  try:
    conn = psycopg2.connect(dbname="krikey-challenge", user="postgres", password="tiana123", host="localhost")
    return conn
  except Exception as ex:
    print(f"Database connection error: {ex}")
    return None

@app.route("/authors/top", methods=["GET"])
def get_top_authors():
  author_name = request.args.get("author_name")
  
  conn = db_connection()
  if conn is None:
    return jsonify({"error": "Database connection failed"}), 500

  try:
    cursor = conn.cursor()
    sql_string = """
      SELECT authors.name AS author_name, SUM(sale_items.item_price * sale_items.quantity) AS total_sales
      FROM sale_items
      JOIN books ON sale_items.book_id = books.id
      JOIN authors ON books.author_id = authors.id"""
    
    #included only if author_name is provided
    if author_name:
      sql_string = sql_string + f" WHERE authors.name ILIKE '{author_name}%'"
    
    sql_string = sql_string + """
      GROUP BY authors.name
      ORDER BY total_sales DESC
      LIMIT 10;"""
    
    cursor.execute(sql_string)
    rows = cursor.fetchall()
    if len(rows) == 0:
      return jsonify({"error": f"'{author_name}' not found."}), 404
    else:
        for row in rows:
            data = [
            {"author_name": row[0],
            "total_sales": row[1]}
            ]
        return jsonify(data), 200
    
  except Exception as ex:
    print(f"Error occurred in database: {ex}")
    return jsonify({"error": "Internal server error"}), 500
  
  finally:
    conn.close()

if __name__ == "__main__":
  app.run()
