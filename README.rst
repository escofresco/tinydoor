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

Please see the Demo_ video.
    .. _Demo: https://youtu.be/7txyTNZqXO4

Tinydoor users will be able to hop on the website_, and upload surveillance videos for free.
    .. _website: https://tinydoor.co

Then the web app will process those videos, using deep learning provided by AWS Rekognition to detect any and all facial expressions.

Based on how positive the facial expressions in the video file are in general, the web app then outputs a "Customer Satisfaction" score of 0-1 for that video.
1 means that the people in the video are having a great time, while a score of 0 means the model thinks they are absolutely miserable. 

What is Tinydoor's Mission?
------------------------------


We need to have a larger conversation about the use of computer vision technology by businesses as well as governments.
Tinydoor does not reveal the identities of the customers found in the videops it searches, but rather returns a lump sum score for the general sentiment of the group. 

We intend to shed a light upon one possible scenario of the future, in which AI can bring value to a company while respecting customer privacy.

To read more into Tinydoor's journey so far, please see this article_ published on Medium on June 29th, 2020.
    .. _article: https://medium.com/dev-genius/computer-vision-the-cure-for-the-retail-industry-ba666421f182?source=friends_link&sk=c82350b6585e69e9c6272d016532ea02


Technical Details
==================


Running the App Locally
------------------------

1. Fork the repo on GitHub, and download your fork onto your local machine. On the new GitHub UI, the fork button is found to the right of where the repo name is shown, and looks like this:
    .. image:: https://i.postimg.cc/Y9s3DWDQ/Screen-Shot-2020-07-27-at-11-34-04-AM.png
2. Be sure to install Postgres.app_ (if you're on macOS). If you're a Windows user, we appreciate you but unfortunately have very little experience developing on your OS. Please check out this 20 minute video_ instead.
    .. _Postgres.app: https://postgresapp.com/
    .. _video: https://youtu.be/BLH3s5eTL4Y
3. Download the latest version Redis for your OS. Details can be found here_.
    .. _here: https://redis.io/download
4. Create a new virtual environment, name it "env" or something else listed under "Project template" on:
    .. code-block:: bash

        .gitignore

    There are several kinds of virtual environments. If you use virutalenv, then you can start and activate your virtual environment using the commands below, respectively:
    ::

        $ python -m venv <name-for-your-virtual-environment>
        $ source <name-for-your-virtual-environment>/bin/activate
    
5. Install the dependencies. From the top level of the repo, run this commad:

::

    $ python -m pip install -r requirements/local.txt

6. Create a new file to hold your environment variables. Name it:
    .. code-block:: bash

        .env

7. You will need the following keys on this file. Don't worry, we will add the values to these variables in upcoming steps:
    .. code-block:: bash

        DJANGO_AWS_ACCESS_KEY_ID
        DJANGO_AWS_SECRET_ACCESS_KEY
        DJANGO_AWS_REKOGNITION_REGION_NAME
        DJANGO_AWS_CLIENT_UPLOADS_BUCKET_NAME
        DJANGO_AWS_REKOGNITION_ROLE_ARN
        DJANGO_AWS_STORAGE_BUCKET_NAME
        DJANGO_AWS_S3_REGION_NAME

8. Please follow the tutorial_ from AWS, it will show you how to set up the AWS services needed to run this project on your own AWS account. As you complete this tutorial, fill in the values for your environment variables above, so that your AWS account info is safe.
    .. _tutorial: https://docs.aws.amazon.com/rekognition/latest/dg/api-video-roles.html

9. Now it's time to run the app!
    - Make sure that Postgres.app is running. You can verify by either clicking on the icon in the menu bar at the top of your screen. The green checkmark tells you it is running, like in this image below:

    .. image:: https://i.postimg.cc/7LDwbCV1/Screen-Shot-2020-07-27-at-11-41-05-AM.png
    
    - Alternatively, you can also open up the app using Spotlight Search.

    .. image:: https://i.postimg.cc/wTX6zc5x/Screen-Shot-2020-07-27-at-11-43-51-AM.png
    
    - Spin up a new Terminal window, and run the Django server.The command is below, and if you are only working on the front-end of the site it is all you will need.

    ::

    $ ./manage.py runserver

    - If you will be doing full-stack development on the app, then you will also need to run the Redis server. Open up another Terminal window, activate your virtual environment, and run this command:
    
    ::

    $ redis-server

    - In addition to Redis, you will also need to be running Celery. Spin up a third Terminal window now, activate your virtual environment once more, and use this:
    
    ::

    $ celery -A config.celery_app worker -l info 

10. Now you are all set. For more commands to help do things such as create a super user account, to run tests, see the section below!



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

If you do not choose to use MailHog, you will still be able to see the emails being sent. They will be printed on whichever Terminal window is running the Django server.
To be clear, this Terminal window is where you ran this command:

.. code-block:: bash

    ./manage.py runserver

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The generated CSS is set up with automatic Bootstrap recompilation with variables of your choice.
Bootstrap v4 is installed using npm and customised by tweaking your variables in ``static/sass/custom_bootstrap_vars``.

You can find a list of available variables `in the bootstrap source`_, or get explanations on them in the `Bootstrap docs`_.



Bootstrap's javascript as well as its dependencies is concatenated into a single file: ``static/js/vendors.js``.


.. _in the bootstrap source: https://github.com/twbs/bootstrap/blob/v4-dev/scss/_variables.scss
.. _Bootstrap docs: https://getbootstrap.com/docs/4.1/getting-started/theming/
