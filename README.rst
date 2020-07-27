Tinydoor
========
A robust way to score the experience of your customers, one video at a time.

.. image:: https://media.giphy.com/media/UVXpGlDTa4OSqyC1f4/giphy.gif
.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style
.. image:: https://travis-ci.com/escofresco/tinydoor.svg?branch=master
     :target: https://travis-ci.com/escofresco/tinydoor
.. image:: https://codecov.io/gh/escofresco/tinydoor/branch/master/graph/badge.svg
     :target: https://codecov.io/gh/escofresco/tinydoor

:License: MIT

Overview
=========

Why Tinydoor?
--------------

Tinydoor helps retailers track customer satisfaction using computer vision and deep learning.

Brick and mortar business owners need to be able to listen to customers, with the least amount of bias as possible.
Tinydoor allows business owners to be able to: 

- maintain their existing surveillance camera infrastructure
- track the emotions of ALL their visitors, not just those who happen to answer customer surveys
- and communicate easily to their partners how the customer experience is evolving emotionally

Tinydoor can be applied to any industry that still relies upon providing physical experiences - from airports to hotels and hospitals, why not see what Tinydoor will do for you?


How does Tinydoor work?
------------------------
See the Demo: https://youtu.be/apUk86MRG2E

Tinydoor users will be able to hop on the site, https://tinydoor.co, and upload surveillance videos for free.

Then the web app will process those videos, using deep learning provided by AWS Rekognition to detect any and all facial expressions.

Based on how positive the facial expressions in the video file are in general, the web app then outputs a "Customer Satisfaction" score of 0-1 for that video.
1 means that the people in the video are having a great time, while a score of 0 means the model thinks they are absolutely miserable. 

What is Tinydoor's Mission?
------------------------------

We need to have a larger conversation about the use of computer vision technology by businesses as well as governments.
Tinydoor does not reveal the identities of the customers found in the videops it searches, but rather returns a lump sum score for the general sentiment of the group. 

We intend to shed a light upon one possible scenario of the future, in which AI can bring value to a company while respecting customer privacy.

Technical Details
==================


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy tinydoor

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html



Celery
^^^^^^

This app comes with Celery.

To run a celery worker:

.. code-block:: bash

    cd tinydoor
    celery -A config.celery_app worker -l info

Please note: For Celery's import magic to work, it is important *where* the celery commands are run. If you are in the same folder with *manage.py*, you should be right.





Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. If you choose to use `MailHog`_ when generating the project a local SMTP server with a web interface will be available.

#. `Download the latest MailHog release`_ for your OS.

#. Rename the build to ``MailHog``.

#. Copy the file to the project root.

#. Make it executable: ::

    $ chmod +x MailHog

#. Spin up another terminal window and start it there: ::

    ./MailHog

#. Check out `<http://127.0.0.1:8025/>`_ to see how it goes.

Now you have your own mail server running locally, ready to receive whatever you send it.

.. _`Download the latest MailHog release`: https://github.com/mailhog/MailHog/releases

.. _mailhog: https://github.com/mailhog/MailHog



Sentry
^^^^^^

Sentry is an error logging aggregator service. You can sign up for a free account at  https://sentry.io/signup/?code=cookiecutter  or download and host it yourself.
The system is setup with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.


Deployment
----------

The following details how to deploy this application.


Heroku
^^^^^^

See detailed `cookiecutter-django Heroku documentation`_.

.. _`cookiecutter-django Heroku documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html




Custom Bootstrap Compilation
^^^^^^

The generated CSS is set up with automatic Bootstrap recompilation with variables of your choice.
Bootstrap v4 is installed using npm and customised by tweaking your variables in ``static/sass/custom_bootstrap_vars``.

You can find a list of available variables `in the bootstrap source`_, or get explanations on them in the `Bootstrap docs`_.



Bootstrap's javascript as well as its dependencies is concatenated into a single file: ``static/js/vendors.js``.


.. _in the bootstrap source: https://github.com/twbs/bootstrap/blob/v4-dev/scss/_variables.scss
.. _Bootstrap docs: https://getbootstrap.com/docs/4.1/getting-started/theming/
