# fptokens tests
import pytest
from path import Path
import fptokens as fpt


def test_token_init():
    token = fpt.Token(name='$token$')
    assert token
    assert token.name == 'token'
    assert token.token == '$token$'


def test_token_change():
    token = fpt.Token(name='$token$')
    token.name = '$replace_token$'
    assert token.name == 'replace_token'
    assert token.token == '$replace_token$'


def test_token_invalid_init():
    with pytest.raises(ValueError):
        fpt.Token(name='>token>')
    with pytest.raises(ValueError):
        fpt.Token(name='$token$', escape='>')


def test_tokens(tokens):
    assert tokens[0] == tokens[1]
    assert tokens[0] != tokens[2]
    assert tokens[0] != tokens[3]
    assert tokens[0].name == 'token'
    assert tokens[0] != True


def test_filename_init(tmpdir):
    fp = fpt.Filename(root=tmpdir,
                      folders=['this', 'folder'],
                      base=['this', 'file'],
                      separator='_',
                      extension='png')
    assert fp

def test_filename_equality(tmpdir):
    fp1 = fpt.Filename(root=tmpdir,
                       folders=['$token$', 'subfolder'],
                       base=['this', 'file', '$token2$'])
    fp2 = fpt.Filename(root=tmpdir,
                       folders=['$token$', 'subfolder'],
                       base=['this', 'file', '$token2$'])
    assert fp1 == fp2
    fp2.folders.append('another_subfolder')
    assert fp1 != fp2
    assert fp1 != True


def test_root(filename, tmpdir):
    filename.root = tmpdir
    assert isinstance(filename.root, Path)
    assert filename.root.exists()


def test_dirname(filename):
    assert isinstance(filename.dirname, Path)
    assert not filename.dirname.exists()
    filename.make()
    assert filename.dirname.exists()


def test_basename(filename):
    assert filename.basename == 'this_file_$token2$.jpg'


def test_abspath(filename):
    assert isinstance(filename.dirname, Path)
    assert filename.abspath == (filename.dirname / filename.basename).abspath()
    assert not filename.abspath.exists()


def test_parsing(filename):
    filename.parse()
    assert len(filename.tokens) == 2
    assert all([token for token in filename.tokens if isinstance(token,
        fpt.Token)])


def test_second_parsing(filename):
    filename.parse()
    assert len(filename.tokens) == 2
    assert all([token for token in filename.tokens if isinstance(token,
        fpt.Token)])


def test_make_invalid(filename):
    with pytest.raises(ValueError):
        filename.make()


def test_parsing_invalid(tmpdir):
    fp = fpt.Filename(root=tmpdir,
                      folders=['$token$$token$', 'subfolder'],
                      base=['this', 'file', '$token2$'])
    with pytest.raises(ValueError):
        fp.parse()


def test_permutations_invalid(tmpdir, data_invalid):
    fp = fpt.Filename(root=tmpdir,
                      folders=['assets', '$sizes$', '$colors$'],
                      base=['untitled', '$sizes$', '$colors$'])
    assert not fp.tokens
    with pytest.raises(fpt.TokenError):
        for perm in fp.resolve():
            perm
    fp.parse()
    with pytest.raises(fpt.TokenError):
        for perm in fp.resolve(**data_invalid):
            perm


def test_permutations(tmpdir, data, results):
    fp = fpt.Filename(root=tmpdir,
                      folders=['assets', '$sizes$', '$colors$'],
                      base=['untitled', '$sizes$', '$colors$'])
    fp.parse()
    permutations = list(fp.resolve(**data))
    assert len(permutations) == len(results)
    for perm in permutations:
        match = False
        for result in results:
            if perm.abspath.endswith(result):
                match = True
        assert match == True
