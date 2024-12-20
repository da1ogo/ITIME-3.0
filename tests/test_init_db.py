from model.database import Database


def test_init_db():
    db = Database("test_clock.db")
    db.drop_tables()
    db.create_tables()
    cur = db.conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='questions';")
    assert cur.fetchone() is not None

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='times';")
    assert cur.fetchone() is not None

    cur.close()
    db.close()
