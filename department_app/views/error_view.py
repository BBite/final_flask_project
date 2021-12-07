"""
Error views, this module defines the following functions:

- `custom_404`: function that displays error page in case 404 error
"""

from flask import render_template

from department_app import app


@app.errorhandler(404)
def custom_404(error):
    """
    Renders 'empty.html' template

    :return: rendered 'empty.html' template
    """

    # pylint: disable=unused-argument

    app.logger.debug('Error 404 was handled')
    app.logger.debug('empty.html was rendered')
    return render_template('empty.html',
                           error={'code': 404, 'msg': 'This page could not be found.'})
