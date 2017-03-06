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


@pytest.fixture(scope='session')
def results():
    results = [
        'assets/1200px/black/untitled_1200px_black.jpg',
        'assets/2500px/black/untitled_2500px_black.jpg',
        'assets/4096px/black/untitled_4096px_black.jpg',
        'assets/1200px/white/untitled_1200px_white.jpg',
        'assets/2500px/white/untitled_2500px_white.jpg',
        'assets/4096px/white/untitled_4096px_white.jpg',
        'assets/1200px/silver/untitled_1200px_silver.jpg',
        'assets/2500px/silver/untitled_2500px_silver.jpg',
        'assets/4096px/silver/untitled_4096px_silver.jpg']
    return results


@pytest.fixture(scope='session')
def data():
    data = {'sizes': ['1200px', '2500px', '4096px'],
            'colors': ['black', 'white', 'silver']}
    return data


@pytest.fixture(scope='session')
def data_invalid():
    data = {'sizes': ['1200px', '2500px', '4096px'],
            'color': ['black', 'white', 'silver']}
    return data
