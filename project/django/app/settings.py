from os import path as os_path
PROJECT_PATH = os_path.abspath(os_path.split(__file__)[0])

LOGGED_IN_TIME_DELTA = 4
FROM_EMAIL = 'bit-less@gmail.com'


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = '/Users/rpedigoni/Sites/bioinfo/app/temp.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'
SITE_ID = 1
USE_I18N = True
USE_I10N = True
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'KEY'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'global_context.context',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)


ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os_path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    # django contribs
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
	'django.contrib.databrowse',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.messages',
    
    # 3rd party
    'django_extensions',
    'pagination',
    'south',
    
    # project apps
    'enrollments',
	'accounts',
    'appsite',
    'courses',
    'institutions',
	'util',
	'plugins',
	
	# bioinfo plugins
	'plugins.genome_annotation',
	'plugins.calendar',
)

AUTH_PROFILE_MODULE = 'accounts.UserProfile'

MEDIA_URL = '/ebioinfo/media/'
STATIC_URL = '/ebioinfo/static/'
ADMIN_MEDIA_PREFIX = '/ebioinfo/static/admin/'
try:
	from local_settings import *
except ImportError:
	print u'Warning: local_settings not found'


MEDIA_ROOT = os_path.join(PROJECT_PATH, 'media')
STATIC_ROOT = os_path.join(PROJECT_PATH, 'static')


# Additional locations of static files
STATICFILES_DIRS = (
    os_path.join(PROJECT_PATH, '../static'),
)
