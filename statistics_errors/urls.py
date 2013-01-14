from django.conf.urls.defaults import patterns, url

# Prepend this prefix to the urls designated to errors data
# collection. 
_ERROR_PREFIX = '__error__'

# Prepend this prefix to the urls designated to access data
# collection. 
_STATISTIC_PREFIX = '__statistic__'

urlpatterns = patterns('statistics_errors.views',
    url(
        regex = r'^%s/client/$' % _ERROR_PREFIX,
        view  = 'error',
        name  = 'client_error'
    ),

    url(
        regex = r'^%s/client/$' % _STATISTIC_PREFIX,
        view  = 'statistic',
        name  = 'client_statistic'
    )
)
