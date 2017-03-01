# fptokens py.test configuration
import pytest
import fptokens as fpt


@pytest.fixture(scope='session')
def tokens():
    t1 = fpt.Token('$token$')
    t2 = fpt.Token('$token$')
    t3 = fpt.Token('>token>', escape='>')
    t4 = fpt.Token('$alt_token$')
    return (t1, t2, t3, t4)


@pytest.fixture(scope='session')
def filename():
    fp = fpt.Filename(root='',
                      folders=['$token$', 'subfolder'],
                      base=['this', 'file', '$token2$'])
    return fp
