def make_error(*args):
    out = ''
    for cond, msg in args:
        if not cond:
            out += msg + '\n'
            
    assert not out, out