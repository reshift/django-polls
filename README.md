Polls app
=======

A simple poll app for Django. Include support for AJAX polls for caching purposes.

Installation
------------

- Run "pip install https://github.com/hub-nl/django-polls/zipball/master"
- Add polls urls to your url file: "(r'^polls/', include('polls.urls'))"
- Add '{% load poll_tags %}' to your templates where needed

Usage
-----

Create some polls in the admin and show them with or without the provided template tags below

Available tags
--------------

Get the latest poll (object).
    
    {% get_poll %}
    {% get_poll as [var] %}

Render the latest poll
    
    {% render_poll %}
    
Render needed javascript for a AJAX version of the latest poll

    {% render_poll_ajax %}

example:

    <script>
      {% render_poll_ajax %}
    </script>