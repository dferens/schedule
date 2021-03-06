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
    'jquery#>1.9.1',
    'react#0.13.1',
    'react-router#0.13.2',
    'lodash#3.6.0',
    'moment#2.9.0'
)

BOWER_COMPONENTS_ROOT = VAR_DIR

#
# django-pipeline
#

INSTALLED_APPS += ('pipeline',)

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

STATICFILES_FINDERS += ('pipeline.finders.PipelineFinder',)

PIPELINE_COMPILERS = (
    'pipeline.compilers.es6.ES6Compiler',
    'pipeline.compilers.sass.SASSCompiler'
)

PIPELINE_6TO5_BINARY = 'babel --experimental'

PIPELINE_JS = {
    'react': {
        'source_filenames': (
            'react/react.js',
            'react-router/build/global/ReactRouter.js',
        ),
        'output_filename': 'js/react-bundle.js'
    },
    'schedule': {
        'source_filenames': (
            'jquery/dist/jquery.js',
            'lodash/lodash.js',
            'moment/moment.js',
            'moment/locale/uk.js',
            'core/schedule/*.es6',
        ),
        'output_filename': 'js/schedule.js'
    }
}

PIPELINE_CSS = {
    'schedule': {
        'source_filenames': (
            'core/schedule/*.sass',
        )
    }
}
