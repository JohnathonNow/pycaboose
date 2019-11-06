def test_encode_decode():
    DATA = ('key', 2607)
    from pycaboose import marshal
    assert marshal.decode(marshal.encode(DATA)) == DATA
