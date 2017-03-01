import os
import re
import attr

from path import Path

__version__ = '0.1.0'
__all__ = []


@attr.s(cmp=False, hash=False, repr=False)
class Token(object):
    """
    Token object for use in :class:`~fptokens.Filename`.

    :param name: Token name
    :type name: str
    :param escape: Escape character, default: ``$``
    :type escape: str
    """
    _name = attr.ib()
    escape = attr.ib(default='$')

    def __attrs_post_init__(self):
        self._name = self.__convert_token(self._name)

    @property
    def name(self):
        """
        Return the token name.

        :return: Token name
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Given a ``value``, strip the value of the escape character and set
        the token name.

        :param value: New token name
        :type value: str
        """
        self._name = self.__convert_token(value)

    @property
    def token(self):
        """
        Return the full token including the escape characters either side.

        :return: Token
        :rtype: str
        """
        return '{0}{1}{0}'.format(self.escape, self.name)

    def __convert_token(self, token):
        pattern = r'\{esc}(\w+)\{esc}'.format(esc=self.escape)
        match = re.match(pattern, token)
        if not match:
            raise ValueError('Invalid token')
        return match.group(1)

    def __key(self):
        return (self.name, self.escape)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return '<Token: {0}>'.format(self.token)


@attr.s(cmp=False, hash=False, repr=False)
class Filename(object):
    """
    Filenames with support for tokens.

    :param root: Root location
    :type root: str
    :param folders: Folder names, attribute supports tokens
    :type folders: list of str
    :param base: Basename of the file, attribute supports tokens
    :type base: list of str
    :param separator: Separator for basename elements
    :type separator: str
    :param extension: Filename extension
    :type extension: str
    :param escape: Escape character for tokens, default: ``$``
    :type escape: str
    """
    _root = attr.ib()
    folders = attr.ib(default=attr.Factory(list),
                      validator=attr.validators.instance_of(list))
    base = attr.ib(default=attr.Factory(list),
                   validator=attr.validators.instance_of(list))
    separator = attr.ib(default='_',
                        validator=attr.validators.instance_of(str))
    extension = attr.ib(default='jpg',
                        validator=attr.validators.instance_of(str))
    escape = attr.ib(default='$')

    def __attrs_post_init__(self):
        self._root = Path(self._root)

    @property
    def root(self):
        """
        Return the filename's root location.

        :return: Root location
        :rtype: :class:`~path.Path`
        """
        return self._root

    @root.setter
    def root(self, value):
        """
        Given a ``value``, convert the value to a :class:`~path.Path` and set
        the filename's root location.

        :param value: New root location
        :type value: str
        """
        self._root = Path(value)

    @property
    def dirname(self):
        """
        Return the filename's location.

        :return: Dirname
        :rtype: str
        """
        return self.root / os.path.sep.join(
            [str(folder) for folder in self.folders])

    @property
    def basename(self):
        """
        Return the filename's basename.

        :return: Basename
        :rtype: str
        """
        return '{0}.{1}'.format(self.separator.join(
            [str(base) for base in self.base]),
            self.extension)

    @property
    def tokens(self):
        """
        Return a list of all tokens in ``folders`` and ``base``.

        :return: List of tokens
        :rtype: list
        """
        folders = set([token for token in self.folders
                       if isinstance(token, Token)])
        basename = set([token for token in self.base
                        if isinstance(token, Token)])
        return [token for token in folders.union(basename)]

    @property
    def abspath(self):
        """
        Return the filename's full absolute path.

        :return: Absolute path
        :rtype: :class:`~path.Path`
        """
        return (self.dirname / self.basename).abspath()

    def make(self):
        """Create the filename's location if it does not exist."""
        self.dirname.makedirs_p()

    def parse(self):
        """
        Parse the filename's ``folders`` and ``base`` attributes, detect
        components that match the token pattern and replace these with
        :class:`fptokens.Token` objects.
        """
        for base_components in (self.folders, self.base):
            for component_idx, component in enumerate(base_components):
                if isinstance(component, Token):
                    continue
                pattern = r'(\{esc}\w+\{esc})'.format(esc=self.escape)
                tokens = re.findall(pattern, component)
                if tokens:
                    if len(tokens) > 1:
                        raise ValueError('Limit: one token per component.')
                    token = tokens[0]
                    base_components[component_idx] = Token(name=token,
                                                           escape=self.escape)

    def __key(self):
        return (self.root, self.folders, self.basename,
                self.separator, self.extension)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__key() == other.__key()
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__key())

    def __repr__(self):
        return '<Filename: {0}>'.format(self.abspath)
