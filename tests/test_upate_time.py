from model.database import Database


def test_init_db():
    db = Database("test_clock.db")
    db.drop_tables()
    db.create_tables()
    db.init_values()
    cur = db.conn.cursor()

    cur.execute("UPDATE times SET time = '10:10:00', is_enable = 1 WHERE id = 1")
    db.conn.commit()

    cur.execute("SELECT id, time, is_enable FROM times WHERE id = 1")

    assert cur.fetchone() == (1, "10:10:00", 1)


    cur.close()
    db.close()
