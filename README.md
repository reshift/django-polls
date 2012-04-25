Polls app
=======

Available tags
--------------
Render the latest poll
    
    {% render_poll %}
    
Render needed javascript for a AJAX version of the latest poll

    {% render_poll_ajax %}

example:

    <script>
      {% render_poll_ajax %}
    </script>