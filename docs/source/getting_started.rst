Getting Started
===============

To get started with ``fptokens``, type:

.. code-block:: python

    import fptokens as fpt

To create a file name, type:

.. code-block:: python

    filename = fpt.Filename(root='/Users/demo/Desktop',
                            folders=['assets', '$colors$'],
                            base=['asset', '$colors$', '1200px'])

This created a file name with default settings, ``_`` as the separator,
``jpg`` as the extension and ``$`` as the escape character for the tokens.

To parse and convert the tokens of the file name to actual tokens, type:

.. code-block:: python

    filename.parse()

To get the results of the parsing, type:

.. code-block:: python

    print filename.tokens
    [<Token: $color$>]

The list of tokens could now be used to create permutations of the tokenised
file name for example for batch output of image assets.

To create a generator of all permutations, define a set of data for each of the
tokens with the token name as the argument name:

.. code-block:: python

    for permutation in filename.resolve(colors=['white', 'black', 'red', 'blue']):
        # do something with the permutation
        print permutation.abspath
    # prints
    # /Users/demo/Desktop/assets/white/asset_white_1200px.jpg
    # /Users/demo/Desktop/assets/black/asset_black_1200px.jpg
    # /Users/demo/Desktop/assets/red/asset_red_1200px.jpg
    # /Users/demo/Desktop/assets/blue/asset_blue_1200px.jpg

Once tokens have been replaced with real-world data to create permutations,
the relevant folders can be created by typing:

.. code-block:: python

    permutation.make()
