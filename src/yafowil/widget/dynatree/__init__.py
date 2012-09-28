import os
from yafowil.base import factory


resourcedir = os.path.join(os.path.dirname(__file__), 'resources')
js = [{
    'group': 'dynatree',
    'resource': 'jquery.dynatree/jquery.dynatree.min.js',
    'order': 20,
}, {
    'group': 'yafowil.widget.dynatree',
    'resource': 'widget.js',
    'order': 21,
}]
default_css = [{
    'group': 'dynatree',
    'resource': 'jquery.dynatree/skin/ui.dynatree.css',
    'order': 20,
}, {
    'group': 'yafowil.widget.dynatree',
    'resource': 'widget.css',
    'order': 21,
}]
bootstrap_css = [{
    'group': 'dynatree',
    'resource': 'jquery.dynatree/skin-bootstrap/ui.dynatree.css',
    'order': 20,
}, {
    'group': 'yafowil.widget.dynatree',
    'resource': 'widget.css',
    'order': 21,
}]


def register():
    import widget
    factory.register_theme('default', 'yafowil.widget.dynatree',
                           resourcedir, js=js, css=default_css)
    factory.register_theme('bootstrap', 'yafowil.widget.dynatree',
                           resourcedir, js=js, css=bootstrap_css)