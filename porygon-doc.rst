==============================
Porygon : Pyglet Game Skeleton
==============================

:Author: Richard Thomas
:Contact: porygon@supereffective.org
:Date: 2009-04-19

This is a framework for writing games in Pyglet_. It sports a number of features
to aid the development process which are documented here. Bear in mind, though,
that this is only a framework. It is expected that any or all of this may be
replaced during the course of development; the intention is therefore only to
help developers set off on the right foot.

.. _Pyglet: http://www.pyglet.org/


History
=======

The layout is based on Skellington_. This is because it is actually based on
the work I did for `Robot Underground`_ which in turn was built up from
Skellington during PyWeek 6.

*Version 0.3*

  - py2app distribution uses hdiutil to package a DMG.
  - Distribution mechanisms are internally documented.

*Version 0.2*

  - Improved dsitribution.
  - Reorganised execution structure.
  - Added mode.Renderer class.
  - Various textual changes.

*Version 0.1*

  - Initial release for PyWeek 7.

.. _Skellington: http://media.pyweek.org/static/rules.html#your-final-submission
.. _Robot Underground: http://www.supereffective.org/pages/Robot-Underground


Modes, Handlers and Renderers
=============================

Games pretty much are event handling, so somewhere to process events is one of
the larger and more complex parts of game development. This is what the
``mode.Mode`` class is for. A mode is an interface object and the ``Mode``
class is the simplest interface object there is: one that never does anything.

Handlers are instances of modes and it is handlers that will be thrown around
the Pyglet event stacks. Modes should respond to window events but do not need
to worry about their position in the event stack. They should also respond to
a number of callbacks from the controller.

For convenience, modes can be identified by a name; new modes are automatically
added to a directory, and the class attribute ``name`` becomes the name by
which it is identified. Thenceforth, controller methods that specify a mode
specify it by name.

The finally players in the world of modes are the renderers. Its good practice
to separate the code that operates an interface from the code that displays it,
so this is the purpose of the ``mode.Renderer`` class. ``Renderer`` objects
are attached to a handler and have a ``handler`` attribute to access it, beyond
that they respond to window events just like a mode does. Likely all they want
to do is respond to the ``on_draw`` event.


Controller
==========

The ``main`` module contains the ``Controller`` class. An instance of this class
does three things:

1) It starts the game, including configuring all libraries that need to be
   configured, setting up auxilliary objects like media managers and resource
   loaders and setting up any model state that needs to be in place from the
   start.

2) It manages the changing of modes and handlers, restructuring the event
   stacks as it does so.

3) It calls the `tick and update`_ methods on the handler and other objects.

Connect and Disconnect
----------------------

The controller issues ``connect`` and ``disconnect`` callbacks to handlers when
they (respectively) have just been pushed onto and are about to be popped off
the event stack. The ``connect`` callback is particularly important because it
is how the handler finds out where the controller is, and therefore equally
important objects like the window.

By default, the ``connect`` and ``disconnect`` callbacks will create instance
attributes on the handler for the controller (``control``) and the window
(``window``).

If the handler has any additional objects that should be on the event stack it
should push them on during ``connect`` and pop them off during ``disconnect``.

Tick and Update
---------------

Event handling isn't quite everything, at least certainly not for realtime
games. That's where the tick and update methods come in. Every handler has them
and can do whatever it likes with them. The ``Controller`` calls them
periodically along with various other things which it keeps in sync.

The only difference between ``tick`` and ``update`` is that ``update`` receives
the ``dt`` argument indicating exactly how much time has passed since it was
last called. There are two sorts of game here: ones that happen in absolute
real-time and therefore need the ``dt`` to keep up, and ones that try to run in
real-time but are actually measuring time in internal ticks. (Obviously, there
are pure turn-based games too, but it matters far less which of these methods is
used to update their logic.)


Development Features
====================

Launching
---------

Running the game is managed by the ``run_game.py`` script at the top level.
Running this script will show you exactly what happens when one of the
distributions is run. The default course is to switch to the game directory,
perform some slight configuration and loade ``main.py``.

However there is also the ``test_game.py`` script, intended to be used during
development (up to final testing), which emulates ``run_game.py`` perfectly
except that it uses a debug argument to set the ``DEBUG`` value in the
``constants`` module to ``True``. Any code that is intended purely as a
development aid can then be sectioned off like so::

    from constants import *
    if DEBUG:
        print "We are in debug mode."

Packaging
---------

The ``setup.py`` script can package the game to a tarball, a .exe or a .app.
There are many constants defined at the top of the script which need to be
configured for your game. See the inline comments for help on their meaning.

Building a distribution is done in one of these ways::

    # Build a source distribution
    python setup.py sdist
    # Build a Windows distribution
    python setup.py py2exe
    # Build an OS X distribution
    python setup.py py2app

Versioning
----------

The version of a release is stored in the ``constants`` module under
``VERSION``. However, there are a couple of useful versioning features specific
to Subversion. If you aren't using Subversion then these won't work but you may
be able to implement them all the same.

There is a file ``VERSION.txt`` which contains two values separated by a colon.
The first is the version string out of the ``constants`` module and the second
is either the Subversion revision number or some special value (see below). The
file is written when the game is packaged for distribution and allows the game
to log versioning information.

The special values and their meanings are:

``testing``
  The game is being run from ``test_game.py``.
``exported``
  There is no version control information.
``unknown``
  Subversion was not installed.

Another feature only available with Subversion is that ``setup.py`` will prompt
you if it thinks you are trying to make a distribution with local modifications.

Error Log
---------

If ``run_game.py`` encounters an error then it writes it to error.log in the
game directory. This is useful for people who just double click on the Python
file to test their game.

Profiling
---------

The ``-p`` or ``--profile`` command line argument is set up to run a profiler
on the game. For more details on profiling, refer to the ``profile`` module in
the `Python docs`_.


.. _Python docs: http://docs.python.org/
