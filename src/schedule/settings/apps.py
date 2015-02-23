import os

from .core import *

#
# django-grappelli
#
INSTALLED_APPS = ('grappelli',) + INSTALLED_APPS

#
# django-debug-toolbar settings
#

INSTALLED_APPS += ('debug_toolbar', 'template_timings_panel')

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

#
# django-bower
#

INSTALLED_APPS += ('djangobower',)

STATICFILES_FINDERS += ('djangobower.finders.BowerFinder',)

BOWER_INSTALLED_APPS = (
    'bootstrap#3.3.2',
)

BOWER_COMPONENTS_ROOT = VAR_DIR
