def test_db_reads(mocker):
    VALUE = 2607
    KEY = 9
    init = mocker.patch('pycaboose.database.Database.__init__')
    init.return_value = None
    read = mocker.patch('pycaboose.database.Database.read')
    read.return_value = None
    from pycaboose import Value
    v = Value(VALUE)  # THIS MUST STAY ON LINE 9
    read.assert_called_with(KEY)
    assert v.value == VALUE


def test_db_reads_stored_value(mocker):
    VALUE = 2607
    KEY = 'key'
    init = mocker.patch('pycaboose.database.Database.__init__')
    init.return_value = None
    read = mocker.patch('pycaboose.database.Database.read')
    read.return_value = VALUE+1
    from pycaboose import Value
    v = Value(VALUE, KEY)
    read.assert_called_with(KEY)
    assert v.value == VALUE+1


def test_db_writes(mocker):
    VALUE = 2607
    KEY = 'key'
    init = mocker.patch('pycaboose.database.Database.__init__')
    init.return_value = None
    read = mocker.patch('pycaboose.database.Database.read')
    read.return_value = None
    write = mocker.patch('pycaboose.database.Database.write')
    write.return_value = None
    from pycaboose import Value
    v = Value(VALUE, KEY)
    read.assert_called_with(KEY)
    assert v.value == VALUE
    v.value += 1
    write.assert_called_with(KEY, VALUE+1)
    assert v.value == VALUE+1
