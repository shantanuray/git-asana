#!/usr/bin/python
# Please note that the following are necessary -
#   (a) asana_key
#   (b) config_filename
#   (c) asana_url
#
# The following can be used to test
# Check ASANA_KEY if it has been defined
# try:
#     asana_key = os.environ['ASANA_KEY']
# except KeyError:
#     print 'Asana key is not set!'
#     quit(-1)
# config_filename = '/Users/chico/DevProjects/git-asana/.git-asana-config'
# asana_url = 'https://app.asana.com/api/1.0/'

import os, json, sys, urllib2

def asana_query(asana_key, path, data=None, method=None):
    if type(path) is not str:
        path = '/'.join(path)
    url = asana_url + path
    req = urllib2.Request(url, data)
    req.add_header('Authorization', 'Basic ' + (asana_key + ':').encode('base64').rstrip())
    if method is not None:
        req.get_method = lambda: method
    try:
        return json.loads(urllib2.urlopen(req).read())
    except urllib2.HTTPError as e:
        return {'error': str(e)}

def find_id(d, name):
    return [v['id'] for v in d if v['name'] == name]

def normalize_verb(inp):
    inp = inp.lower()
    status_types = ['c', 'fixing','fixed' ,'fixes' ,'closing' ,'closed' ,'closes' ,'completed' ,'complete' ,'completes' ,'done']
    if inp in status_types:
        return 'complete'
    else:
        return {'error': 'Unknown Verb Error'}

def take_stdin(field_name, field_prompt=None):
    if field_prompt is None:
        inp = raw_input('Enter value for ' + field_name + ': ')
    else:
        inp = raw_input('Enter value for ' + field_name + '. If same as <' + field_prompt + '> press Enter, else type name: ')
        if inp == '':
            inp = field_prompt
    if inp == '':
        print 'Error in specifying value for ' + field_name
        return -1
    else:
        return inp

def config_create(project=None, workspace=None):
    project = take_stdin('project', project)
    workspace = take_stdin('workspace', workspace)
    return json.dumps({'project' : project, 'workspace' : workspace})

def workspace_id_query(workspace):
    workspaces = asana_query(asana_key, 'workspaces')
    workspace_id = find_id(workspaces['data'], workspace)
    if not workspace_id:
        print 'There is no such workspace'
        return -1
    else:
        return workspace_id[0]

def project_id_query(workspace_id, project):
    projects = asana_query(asana_key, ['workspaces', str(workspace_id), 'projects'])
    project_id = find_id(projects['data'], project)
    if not project_id:
        print 'There is no such project'
        return -1
    else:
        return project_id[0]