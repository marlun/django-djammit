=============
django-djamit
=============

A very basic way of handling javascript templates and including javascript
include tags in your django apps.

Usage
=====

You need to set a JAVSCRIPTS dictionary in your settings file which lists packages
and files which Djammit should add to the specific packages.::

    JAVASCRIPTS = {
        'core': (
            'js/libs/jquery-*.js',
            'js/libs/underscore*.js',
            'js/libs/*.js',
            'js/model/**/*.js',
            'js/views/**/*.js',
            'js/templates/**/*.jst',
        )
    }

Now you need to add ``{% include_javascript core %}`` for Djammit to load the package.
When Debug = True the include_javascript template tag will render all of the included
javascript include tags. It will also run Django's management command ``collectstatic`` on
every request which will move changed files to your static root folder.

As you can see in the above example the last pattern will include javascript templates
(*.jst). The templates will be included in a file named after the package (core.js in
this case).
