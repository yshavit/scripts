#!python3

import json
import re
import shutil
import sys
#import xml.dom.minidom as xml
import xml.etree.ElementTree as ET
from datetime import datetime

def log(msg):
    print(msg, file=sys.stderr)


def read_vscode(path):
    with open(path) as f:
        vscode_str = f.read()
    # vscode allows (1) comments in json, and (2) extra commas: "[foo, bar,]". Strip those away.
    vscode_str = re.sub('\n\\s*//.*', '', vscode_str)
    vscode_str = re.sub(',\\s+]', ']', vscode_str)
    return json.loads(vscode_str)

def launch_configs(vscode_obj):
    for config in vscode_obj.get('configurations', []):
        if config.get('type') == 'node':
            yield config

def upsert_config(project_et, launch_config):
    port = launch_config.get('port')
    config_name = launch_config.get('name')
    if not port or not config_name:
        return
    port = str(port)

    run_manager = project_et.find("./component[@name='RunManager']")
    if not run_manager:
        run_manager = ET.Element('component', attrib={'name': 'RunManager'})
        run_manager.append(ET.Element('list'))
        project_et.getroot().append(run_manager)

    for project_run_config in run_manager.iter('configuration'):
        if config_name == project_run_config.get('name') and project_run_config.get('type') == 'ChromiumRemoteDebugType':
            orig_attrs = dict(project_run_config.attrib)

            any_updated = False

            def do_update(key, value):
                any_updated = True
                if value is None:
                    if key in project_run_config:
                        log(f"  Updated \"{config_name}\" to remove {key} (was {project_run_config.get(key)})")
                        del project_run_config[key]
                else:
                    log(f"  Updated \"{config_name}\" to use {key} {value} (was {project_run_config.get(key)})")
                    project_run_config[key] = value

            if project_run_config.get('port') != port:
                do_update('port', port)
            config_address = launch_config.get('address')
            if config_address != project_run_config.get('host'):
                if config_address in ['localhost', '127.0.0.1']:
                    do_update('host', None)
                else:
                    do_update('host', config_address)
            if not any_updated:
                log(f"  {config_name} was up to date")
            return # found and updated; no need to insert

    # If we got here, there was nothing to update; upsert instead.
    # add "<configuration ...> <method /> </configuration>"
    log(f"  Added config {config_name}")
    config_elem = ET.Element('configuration', attrib={
        'name':  config_name,
        'type': 'ChromiumRemoteDebugType',
        'factoryName': 'Chromium Remote',
        'port': port
    })
    config_elem.append(ET.Element('method', attrib={'v': '2'}))
    run_manager.append(config_elem)
    # add <item> to sub-element <list>
    run_manager_list = run_manager.find('list')
    if run_manager_list:
        run_manager_list.append(ET.Element('item', attrib={'itemvalue': config_name}))

def upsert_configs(project_et, vscode_obj):
    for one_config in launch_configs(vscode_obj):
        upsert_config(project_et, one_config)

def upsert_from_files(project_root, vscode_json_path):
    project_file_path = f'{project_root}/.idea/workspace.xml'
    shutil.copy(project_file_path, f'{project_root}/.idea/workspace-bak-{timestamp()}.xml')
    log(f'Syncing {vscode_json_path} to {project_file_path}')

    project_et = ET.parse(project_file_path)
    vscode_obj = read_vscode(vscode_json_path)
    upsert_configs(project_et, vscode_obj)
    project_et.write(project_file_path, encoding='utf-8', xml_declaration=True)

def timestamp():
    full_ts = datetime.now().isoformat()
    without_fractional_seconds = re.sub('\\..*', '', full_ts)
    return without_fractional_seconds.replace(':', '').replace('-', '')

if __name__ == '__main__':
    project_root = sys.argv[1]
    vscode_json_path = sys.argv[2]
    upsert_from_files(project_root, vscode_json_path)


