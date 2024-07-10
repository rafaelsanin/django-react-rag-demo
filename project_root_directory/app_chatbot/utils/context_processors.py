import json
import os
from django.conf import settings


def react_build_files(request):
    manifest_path = os.path.join(settings.REACT_APP_DIR, 'asset-manifest.json')
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        main_js = os.path.join(settings.REACT_APP_DIR,
                               str(manifest['files']['main.js']))
        main_css = os.path.join(settings.REACT_APP_DIR,
                                manifest['files'].get('main.css', ''))
    except (IOError, KeyError, json.JSONDecodeError):
        main_js = os.path.join(settings.REACT_APP_DIR, 'static/js/main.js')
        main_css = os.path.join(settings.REACT_APP_DIR, 'static/js/main.css')
    return {
        'main_js': main_js,
        'main_css': main_css,
    }
