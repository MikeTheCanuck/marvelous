marvelous
=========

Marvel API python wrapper.

Contributing
------------

- To run the test suite, run `python -m nose` in the `tests` folder
- When running a new test for the first time, set the environment variables
  `PUBLIC_KEY` and `PRIVATE_KEY` to any Marel API keys. The result will be
  stored in the `testing_mock` database without your keys.

Examples
--------

This is a script which can be run at the beginning on the week to generate a
complete Marvel pull list, excluding any series the user doesn't want.

This script is included as example.py, and it's accompanied by a config.py file where 
you must paste in your Marvel API public and private keys between the single quote 
characters (dummy strings included to reduce guesswork).  I also extended the script to 
demonstrate handling of the series included in IGNORE.

Note: If you don't remember to substitute valid API keys, then you'll see this error 
at runtime: 
marvelous.exceptions.ApiError: The passed API key is invalid.

.. code-block:: python

    import os
    import marvelous

    # Your own config file to keep your private key local and secret
    from config import public_key, private_key

    # All the series IDs of comics I'm not interested in reading
    # I pull these out of the resulting pulls.txt file, then rerun this script
    IGNORE = set([
        19709, 20256, 19379, 19062, 19486, 19242, 19371, 19210, 20930, 21328,
        20834, 18826, 20933, 20365, 20928, 21129, 20786, 21402, 21018
    ])

    # Authenticate with Marvel, with keys I got from http://developer.marvel.com/
    m = marvelous.api(public_key, private_key)

    # Get all comics from this week, sorted alphabetically by title
    # Uses the same API parameters as listed in the official API documentation
    pulls = sorted(m.comics({
        'format': "comic",
        'formatType': "comic",
        'noVariants': True,
        'dateDescriptor': "thisWeek"}),
        key=lambda comic: comic.title)

    # Grab the sale date of any of the comics for the folder name
    directory = pulls[0].dates.on_sale.strftime('%Y-%m-%d')

    # If there's no folder by that name, create one
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create a pulls.txt file in that folder
    with open(directory + '/pulls.txt', 'w') as pull_checklist:
        # Check each comic that came out this week
        for comic in pulls:
            # If this series isn't in my ignore list
            if comic.series.id not in IGNORE:
                # Write a line to the file with the name of the issue, and the
                # id of the series incase I want to add it to my ignore list
                pull_checklist.write('{} (series #{})\n'.format(
                    comic.title.encode('utf-8'), comic.series.id))
