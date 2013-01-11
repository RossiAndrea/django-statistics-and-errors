from django.conf.urls.defaults import patterns, url

# Prepend this prefix to the urls designated to errors data
# collection. 
_ERROR_PREFIX = '__error__'

urlpatterns = patterns('statistics_errors.views',
    url(
        regex = r'^%s/client/$' % _ERROR_PREFIX,
        view  = 'error',
        name  = 'client_error'
    )
)
