# Django Client Statistics and Errors Logger

Automatic tracking of javascript errors and client accesses for Django based on sorensen's Django Client Errors.
Sends error and access data information back to the server to be persisted in the database, uses jQuery if available to send all information,
falling back to a GET request to send limited information.


## Installation

```bash
pip install -e GIT+git://github.com/RossiAndrea/django-statistics-and-errors.git#egg=django-statistics-and-errors
````

Alternatively, you can download the project and put the `statistics_errors` directory into 
your project directory.

Add the following app to your project's `INSTALLED_APPS` in the `settings.py` file:

````
'statistics_errors',
````

Add the following middleware to your project's `MIDDLEWARE_CLASSES` in the `settings.py` file:

````
'statistics_errors.middleware.StatisticsErrorMiddleware',
````

Since this module contains a model of its own, you must add it to the database schema:

```bash
python manage.py syncdb
````

Or, if you are using `south` to manage your project, you can run the following command,
however, this is best to use only if you have included the source code inside of your project.
Otherwise, it will attempt to add the migration to the egg directory.

```bash
python manage.py schemamigration statistics_errors
````

After the database synchronization you have to collect static files into STATIC_ROOT.
Personally I prefer symlinking file into STATIC_ROOT directory, so I don't have to run 
again the command each time I modify a single static file.
If you prefer copying the file, simply ommit the ***-l*** parameter in the following command.
```bash
python manage.py collectstatic -l
````

### Note:

Tying into middleware allows each panel to be instantiated on request and
rendering to happen on response.

The order of MIDDLEWARE_CLASSES is important: the Statistics and Error middleware
must come after any other middleware that encodes the response's content
(such as GZipMiddleware).

If you are using the `django_debug_toolbar`, the `client_error` middleware must
come after it.

The javascript will only be added if the mimetype of the
response is either `text/html` or `application/xhtml+xml` and contains the selected
html tag, the `</head>` tag by default.

Note: Be aware of middleware ordering and other middleware that may
intercept requests and return responses.  Putting the debug toolbar
middleware *after* the Flatpage middleware, for example, means the
toolbar will not show up on flatpages.

### Beware:

The middleware provides its own url parsing rules. Do not add inclusion to the app's 
url configuration to your own ROOT_URLCONF or very bad things gonna happen, unless 
**CLIENT_ERRORS_TAG** is explicity set to False in settings!
Among others: infinite loops on url parsing for each rule defined after the inclusion of
'statistics_errors.urls' and, if you configured django for sending errors to your email
while DEBUG=False, a lot of spam.


## Usage

When an error occurs, the app will save the following information:

* `created` current timestamp
* `message` javascript error text
* `url` where the error occurred
* `loc` line of code
* `os` user's operating system
* `browser` user's browser
* `version` user's browser version

If jQuery is found on the page, the app will send the following information as 
serialized JSON (not sent otherwise due to URL size constraints)

* `plugins` list of browser enabled plugins
* `device` user's device information
* `locale` user's country and language


## Example

To access the errors for a given user you could do something like this:

```python
from models import User

user = User.objects.get(pk=1)
errors = user.usererror_set.all()
````

If you want to access the `plugins`, `device`, or `locale` fields, you will likely
want to deserialize them first for better use.

```python
from django.utils import simplejson
from statistics_errors.models import UserError

error = UserError.objects.get(pk=1)
locale = simplejson.loads(error.locale)
device = simplejson.loads(error.device)
plugins = simplejson.loads(error.plugins)
````


## Output

* `created` 2012-06-16 11:05:56
* `created_by_id` 1   
* `message` Uncaught ReferenceError: foo is not defined    
* `url` http://localhost:8000/app.js
* `loc` 174 
* `os` Mac 
* `browser` Chrome
* `version` 19.0.1084.54
* `plugins` {"flash":true,"silverlight":false,"java":true,"quicktime":true}
* `device` {"screen":{"width":1280,"height":1024},"viewport":{"width":1308,"height":386},"is_tablet":false,"is_phone":false,"is_mobile":false}
* `locale` {"country":"us","lang":"en"}


## Configuration

* `statistics_errors_USER` the user model to connect the errors to (optional, default `django.contrib.auth.models.User`)
* `statistics_errors_AUTO` automatic URL injection (optional, default `True`)
* `statistics_errors_MEDIA_ROOT` directory to serve the JS media from (optional)
* `statistics_errors_TAG` chosen tag to prepend the javascript to (optional, default `</head>`)
* `statistics_errors_ENABLED` enable the module (optional, default `not DEBUG`)


## License

(The MIT License)

Copyright (c) 2013 Andrea Rossi <direlemming+github@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
