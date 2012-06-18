import os
import json
from yafowil import loader
import yafowil.webob
from yafowil.base import factory
from yafowil.controller import Controller
import yafowil.widget.dynatree
from yafowil.tests import fxml
from webob import Request, Response

dir = os.path.dirname(__file__)

DOC_LOCAL = """\
Dynatree with Static Content
----------------------------

Define a tree of dicts with each value a tuple::

    sample_tree = {
        'animal': ('Animals', {
            'mammal': ('Mammals', {
                'elephant': ('Elephant', None),
                'ape': ('Ape', None),
                'horse': ('Horse', None),
            }),
            'bird': ('Birds', {
                'duck': ('Duck', None),
                'swan': ('Swan', None),
                'turkey': ('Turkey', None),
                'hummingbird': ('Hummingbird', None),
            }),
    })}

Then the widget can be factored so::

    factory('label:error:dynatree', props={
        'label': 'Select single value',
        'value': '',
        'source': sample_tree})

"""

DOC_DYNAMIC = """\
Dynatree with JSON
------------------

A JSON address needs to be provided i order to use this feature. Here it is
under ``http://.../yafowil.widget.dynatree.json``. Then the widget is defined
this way::

    factory('label:error:dynatree', props={
             'label': 'Select multiple',
             'value': '',
             'source': 'yafowil.widget.dynatree.json',
             'selectMode': 2})

"""

sample_tree = {
    'animal': ('Animals', {
        'mammal': ('Mammals', {
            'elephant': ('Elephant', None),
            'ape': ('Ape', None),
            'horse': ('Horse', None),
        }),
        'bird': ('Birds', {
            'duck': ('Duck', None),
            'swan': ('Swan', None),
            'turkey': ('Turkey', None),
            'hummingbird': ('Hummingbird', None),
        }),
})}


def json_response(environ, start_response):
    request = Request(environ)
    selected = request.GET['selected'].split('|')
    def dir_tree(base):
        result = []
        for value in os.listdir(base):
            if value.endswith('pyc') or value.startswith('.'):
                continue
            new_item = {} #we have to have boolItems
            new_item['key'] = os.path.join(base, value)
            new_item['title'] = value
            new_item['children'] = []
            if os.path.isdir(new_item['key']):
                new_item['children'] = dir_tree(new_item['key'])
            new_item['select'] = new_item['key'] in selected
            new_item['isFolder'] = bool(new_item['children'])
            new_item['hideCheckbox'] = False
            new_item['expand'] = new_item['key'] in selected \
                          or isSomethingSelectedInChildren(new_item['children'],
                                                           selected)
            result.append(new_item)
        return result
    data = dir_tree(dir)
    response = Response(content_type='application/json', body=json.dumps(data))
    return response(environ, start_response)


def isSomethingSelectedInChildren(children, selected):
    return bool(set([_['key'] for _ in children]).intersection(selected)) \
        or bool([_ for _ in children
            if _['children'] and isSomethingSelectedInChildren(_['children'], selected)])


def get_example():
    part1 = factory(u'fieldset', name='yafowilwidgetdynatree.local')
    part1['local'] = factory('label:error:dynatree', props={
         'label': 'Select single value',
         'value': '',
         'source': sample_tree})
    part2 = factory(u'fieldset', name='yafowilwidgetdynatree.remote')
    part2['remote'] = factory('label:error:dynatree', props={
         'label': 'Select multiple',
         'value': '',
         'source': 'yafowil.widget.dynatree.json',
         'selectMode': 2})
    routes = {'yafowil.widget.dynatree.json': json_response}
    return [{'widget': part1, 'doc': DOC_LOCAL, 'title': 'Static Tree'},
            {'widget': part2, 'routes': routes, 'doc': DOC_DYNAMIC,
             'title':'Tree via JSON'}]
