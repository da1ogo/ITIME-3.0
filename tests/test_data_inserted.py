from model.database import Database


def test_data_inserted():
    db = Database("test_clock.db")
    db.drop_tables()
    db.create_tables()
    db.init_values()
    cur = db.conn.cursor()

    cur.execute("SELECT * FROM questions WHERE id = 29")
    assert cur.fetchone() is not None

    cur.execute("SELECT * FROM questions WHERE id = 15")
    assert cur.fetchone() is not None

    cur.execute("SELECT * FROM questions WHERE id = 1")
    assert cur.fetchone() is not None

    cur.execute("SELECT * FROM times WHERE id = 2")
    assert cur.fetchone() is not None

    cur.close()
    db.close()
