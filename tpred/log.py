# -*- coding: utf-8 -*-

import os
import sys
import json
import logging
import logging.handlers
import logging.config


class ContextFilter(logging.Filter):

    """Filter that will add 'extra' fields to a log message"""

    def __init__(self, name="", extras=None):
        super(ContextFilter, self).__init__(name=name)
        self.extras = extras or {}

    def unset(self, key):
        """Clear a key"""
        self.extras.pop(key)

    def filter(self, record):
        """Required to be a logging.Filter"""
        record.__dict__.update(self.extras)
        return True


logContext = ContextFilter()

config_file = os.getenv('LOGGING_CONFIG_FILE')

# Use file config over all else if available
if config_file is not None and os.path.exists(config_file):
    if config_file.endswith(".json"):
        logging.config.dictConfig(json.load(open(config_file, "r")))
    else:
        logging.config.fileConfig(config_file)
    log = None
# otherwise, use our default logging configuration from environment settings
else:
    log_to_console = os.getenv('LOG_TO_CONSOLE', 'False') == 'True'
    log_dir = os.getenv('LOGGING_DIR', 'logs')

    try:
        os.mkdir(log_dir)
    except:
        pass

    current_process = str(os.path.basename(sys.argv[0]) + '.log')
    current_process = current_process.replace('.py', '')
    log_file = os.getenv('LOGGING_FILENAME')

    if log_file is None:
        if 'gunicorn' in current_process or 'uwsgi' in current_process:
            log_file = os.path.join(log_dir, 'cratejoy.log')
        else:
            log_file = os.path.join(log_dir, current_process)
    else:
        log_file = os.path.join(log_dir, log_file)

    _stash = logging.handlers.RotatingFileHandler(filename="{}.json".format(log_file),
                                                  maxBytes=104857600,
                                                  backupCount=2)
    _stash.addFilter(logContext)
    _stash.setLevel(os.getenv('LOGGING_LEVEL', logging.DEBUG))

    _fh = logging.handlers.RotatingFileHandler(filename=log_file,
                                               maxBytes=104857600,
                                               backupCount=2)
    _fh.setLevel(os.getenv('LOGGING_LEVEL', logging.DEBUG))

    _formatter = logging.Formatter(
        fmt=os.getenv('LOGGING_FORMAT',
                      '%(asctime)s [%(process)d] [%(levelname)s] '
                      '%(module)s: %(message)s')
    )

    if log_to_console is True:
        _handler = logging.StreamHandler()
        _handler.setLevel(os.getenv('LOGGING_LEVEL', logging.DEBUG))
        _handler.setFormatter(_formatter)

    _fh.setFormatter(_formatter)

    for name in [u"cratejoy", u"flask", u"flask_oauthlib", u"oauthlib",
                 u"mailchimp", u"html5lib", u"pyftpdlib", u"restapi",
                 u"sift_client", u"shipstation"]:
        # , u"suds.wsdl", u"suds.transport.http", u"suds.metrics",
        # u"suds.xsd.schema", u"suds.xsd.sxbase", u"suds.xsd.query",
        # u"suds.wsdl"]:
        log = logging.getLogger(name)
        log.setLevel(os.getenv('LOGGING_LEVEL', logging.DEBUG))
        if log_to_console is True:
            log.addHandler(_handler)
        log.addHandler(_fh)
        #log.addHandler(_stash)
        log.propagate = False
