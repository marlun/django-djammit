==============
django-djammit
==============

A very basic way of handling javascript templates and including javascript
include tags in your django apps.

VERY EARLY ALPHA RELASE! Actually, it might not work at all.

The name Djammit and the code (or atleast the ideas) has pretty much been ripped from
`DocumentCloud's Jammit <http://documentcloud.github.com/jammit/>`_ which is a much more 
advanced and mature tool for Ruby on Rails.

Usage
=====

Start out by setting your `STATIC_ROOT` (ex: /var/www/project/static) and your `STATIC_URL` 
(ex: /static/) settings. Those settings will be used when Djammit looks for files matching
the patterns you specify.

You tell Djammit which files to include by setting the DJAMMIT_JAVSCRIPTS setting as a dictionary
of packages with patterns.::

    DJAMMIT_JAVASCRIPTS = {
        'core': (
            'js/libs/jquery-*.js',
            'js/libs/underscore*.js',
            'js/libs/*.js',
            'js/model/**/*.js',
        ),
        'ui': (
            'js/views/**/*.js',
            'js/templates/**/*.jst',
        )
    }

Now you need to add ``{% include_javascript core ui %}`` for Djammit to load the packages.

When Debug = True the include_javascript template tag will render all of the included
javascript include tags if Debug = False the files will be compiled into a single JavaScript
file named after the package they are in.

Right now Djammit also runs Django's management command ``collectstatic`` on every request 
which will move changed files to your static root folder. If you are using django-staticfiles
with Django pre 1.3 or some other app you can specify which collect command to run by setting
the `DJAMMIT_COLLECT_COMMAND`.

As you can see in the above example the ui package includes javascript templates (\*.jst). 
The templates will be included in a file named after the package (core.js in this case) which
in production (Debug = False) will be the same file as the javascript is compiled into. The
templates can later be accessed using the JST namespace.::

    $(this.el).html(JST['name']({model: this.model}));

You can change the template files extension with the `DJAMMIT_TEMPLATE_EXTENSION` setting and
the namespace (defaults to JST) with the `DJAMMIT_TEMPLATE_NAMESPACE` setting. By default 
the template engine used is underscore.js' _.template method. You can change that to something
else using the `DJAMMIT_TEMPLATE_FUNCTION` setting.
