Getting Started
===============

To get started with ``fptokens``, type:

.. code-block:: python

    >>> import fptokens as fpt

To create a file name, type:

.. code-block:: python

    >>> filename = fpt.Filename(root='/Users/demo/Desktop',
                                folders=['assets', '$colors$'],
                                base=['asset', '$colors$', '1200px'])

This created a file name with default settings, ``_`` as the separator,
``jpg`` as the extension and ``$`` as the escape character for the tokens.

To parse and convert the tokens of the file name to actual tokens, type:

.. code-block:: python

    >>> filename.parse()

To get the results of the parsing, type:

.. code-block:: python

    >>> print filename.tokens
    >>> [<Token: $color$>]

The list of tokens could now be used to create permutations of the tokenised
file name for example for batch output of image assets.

ONce tokens have been replaced with real-world data to create permutations,
the relevant folders can be created by typing:

.. code-block:: python

    >>> filename.make()
