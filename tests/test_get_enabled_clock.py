from model.database import Database


def test_get_enabled_clock():
    db = Database("test_clock.db")
    db.drop_tables()
    db.create_tables()
    db.init_values()
    cur = db.conn.cursor()

    cur.execute("UPDATE times SET time = '11:11:00', is_enable = 1 WHERE id = 1")
    cur.execute("UPDATE times SET time = '00:10:00', is_enable = 1 WHERE id = 3")
    db.conn.commit()

    assert db.get_enables_clocks() == [("11:11:00",), ("00:10:00",)]


    cur.close()
    db.close()
