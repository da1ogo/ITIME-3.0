from model.database import Database


def test_get_question():
    db = Database("test_clock.db")
    db.drop_tables()
    db.create_tables()
    db.init_values()

    assert db.get_random_question() is not None

    db.close()
