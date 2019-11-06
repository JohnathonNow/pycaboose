def test_db_empty(mocker):
    KEY = 'key'
    from pycaboose.database import Database
    init = mocker.patch('pycaboose.tailwriter.TailWriter.__init__')
    init.return_value = None
    read = mocker.patch('pycaboose.tailwriter.TailWriter.read')
    read.return_value = []

    db = Database()
    read.assert_called_with()
    assert not db._db
    assert not db.read(KEY)


def test_db_with_keys(mocker):
    KEY = 'key'
    VALUE = 'value'
    POS = 2607
    STR = 'BLOB'
    from pycaboose.database import Database
    init = mocker.patch('pycaboose.tailwriter.TailWriter.__init__')
    init.return_value = None
    read = mocker.patch('pycaboose.tailwriter.TailWriter.read')
    read.return_value = [(POS, STR)]
    marshal_d = mocker.patch('pycaboose.marshal.decode')
    marshal_d.return_value = (KEY, VALUE)

    db = Database()
    marshal_d.assert_called_with(STR)
    assert KEY in db._db
    assert db._db[KEY].value == VALUE
    assert db._db[KEY].comment == STR
    assert db._db[KEY].pos == POS
    assert db.read(KEY) == VALUE


def test_db_write_one(mocker):
    POS = 2607
    KEY = 'key'
    VALUE = 'value'
    STR = 'BLOB'
    from pycaboose.database import Database
    init = mocker.patch('pycaboose.tailwriter.TailWriter.__init__')
    init.return_value = None
    read = mocker.patch('pycaboose.tailwriter.TailWriter.read')
    read.return_value = []
    write = mocker.patch('pycaboose.tailwriter.TailWriter.write')
    write.return_value = POS
    marshal_e = mocker.patch('pycaboose.marshal.encode')
    marshal_e.return_value = STR

    db = Database()
    db.write(KEY, VALUE)
    marshal_e.assert_called_with((KEY, VALUE))
    write.assert_called_with(STR)
    assert KEY in db._db
    assert db._db[KEY].value == VALUE
    assert db._db[KEY].comment == STR
    assert db._db[KEY].pos == POS
    assert db.read(KEY) == VALUE


def test_db_write_two(mocker):
    POS = 2607
    KEY = 'key'
    VALUE = 'value'
    STR = 'BLOB'
    from pycaboose.database import Database
    init = mocker.patch('pycaboose.tailwriter.TailWriter.__init__')
    init.return_value = None
    read = mocker.patch('pycaboose.tailwriter.TailWriter.read')
    read.return_value = []
    write = mocker.patch('pycaboose.tailwriter.TailWriter.write')
    write.return_value = POS
    shrink = mocker.patch('pycaboose.tailwriter.TailWriter.shrink')
    shrink.return_value = None
    marshal_e = mocker.patch('pycaboose.marshal.encode')
    marshal_e.return_value = STR

    db = Database()
    db.write(KEY, VALUE)
    write.return_value = POS+1
    marshal_e.return_value = STR + '!'
    db.write(KEY+'!', VALUE+'!')
    write.assert_called_with(STR + '!')
    write.return_value = POS+2
    marshal_e.return_value = STR + '!!'
    db.write(KEY, VALUE+'!!')
    shrink.assert_called_with(POS)
    write.assert_called_with(STR + '!!')
    assert KEY in db._db
    assert db._db[KEY].value == VALUE + '!!'
    assert db._db[KEY].comment == STR + '!!'
    assert db._db[KEY].pos == POS+2
    assert db.read(KEY) == VALUE + '!!'
    assert KEY + '!' in db._db
    assert db._db[KEY + '!'].value == VALUE + '!'
    assert db._db[KEY + '!'].comment == STR + '!'
    assert db._db[KEY + '!'].pos == POS+2
    assert db.read(KEY + '!') == VALUE + '!'
