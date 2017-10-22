It's simple UWSGI framework.
Usage example: 'uwsgi --http :9090 --wsgi-file example.py'
Your website will be available at http://localhost:9090/ in this case.

To create your UWSGI app use this:
application = UwsgiApp()

Use '@application.add_handler([regexp])' for adding your url handlers.

Also you can use this simple functions for conversion your text into html:
- plain_text_to_html(text)
- text_to_html_link(link, text)
- text_to_html_paragraph(text)

You can find simple usage examples in 'examlpe.py'
