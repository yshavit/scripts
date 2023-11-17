import argparse
import io
import json
import os
import subprocess
import sys
from contextlib import contextmanager

SCRIPT_NAME = os.path.basename(sys.argv[0])

class Configs:
    CONFIG_DIR_HOME = os.path.expanduser('~/.config/yshavit-scripts')

    def __init__(self, script_name):
        self.dir_path = os.path.join(Configs.CONFIG_DIR_HOME, script_name)
        os.makedirs(self.dir_path, exist_ok=True)

    def open_read(self, file_name, default_value=None):
        file_path = self.file_path(file_name)
        if not os.path.exists(file_path):
            if default_value is None:
                raise Exception(f'no such file: {file_path}')
            return io.StringIO(default_value)
        return open(file_path)

    def open_write(self, file_name):
        return open(self.file_path(file_name), 'w')

    def read_json(self, file_name, default_value=None):
        # open_read requires default_value to be a string, and we'll read it as json; so take the value and jsonify it.
        # That's not efficient, but whatever.
        if default_value is not None:
            default_value = json.dumps(default_value)
        with self.open_read(file_name, default_value=default_value) as f:
            return json.load(f)

    def write_json(self, file_name, obj):
        with self.open_write(file_name) as f:
            json.dump(obj, f, indent=2)

    def file_path(self, file_name):
        return os.path.join(self.dir_path, file_name)

class DispatchingArgParser:
    def __init__(self, description):
        self.parser = argparse.ArgumentParser(prog=SCRIPT_NAME, description=description)
        self.subparsers = self.parser.add_subparsers(required=True)

    def __enter__(self):
        return self

    @contextmanager
    def subcommand(self, func, *args, **kwargs):
        cmd_subparser = self.subparsers.add_parser(*args, **kwargs)
        yield cmd_subparser
        if func:
            cmd_subparser.set_defaults(_func=func)

    def __exit__(self, type, value, traceback):
        if traceback:
            print(traceback, file=sys.stderr)
            raise Exception(value)
        args = self.parser.parse_args()
        args_vars = vars(args)
        args_func = args_vars.pop('_func')
        args_func(**args_vars)


def simple_exec(cmd, *cmd_args, **kwargs) -> str:
    cmd_list = cmd if isinstance(cmd, list) else [str(cmd)]
    cmd_desc = ' '.join(cmd_list)
    cmd_list += cmd_args
    completed = subprocess.run(cmd_list, capture_output=True, **kwargs)
    if completed.returncode != 0:
        msg = f'exit code {completed.returncode} when running {cmd_desc}'
        if completed.stderr:
            lines = completed.stderr.decode('utf-8').strip('\n\r').split('\n')
            lines = [f'│ {l}' for l in lines]
            msg += ':\n' + ('\n'.join(lines))
        raise Exception(msg)
    return completed.stdout.decode('utf-8').strip('\n\r')

