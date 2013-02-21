#!/usr/bin/env python


"""
Longshoreman corrals containers.

"""
import json
import os
import subprocess

def _get_default_container_dir(env):
    """ tries $LSM_CONTAINER_DIR, fall back to $HOME/.lsm/containers/ """
    fallback = os.path.join(env.get('HOME'), '.lsm/containers/')
    return env.get('LSM_CONTAINER_DIR', fallback)

DEFAULT_CONTAINERS_DIR = _get_default_container_dir(os.environ)

COMMON_CONFIG_KEYS = (
    'user',
    'primary_group',
    'secondary_groups',
    'env',
    'kill_timeout',
)
CONTAINER_CONFIG_KEYS = (
    'ports',
)
PROCESS_CONFIG_KEYS = (
    'cwd',
)


class LongShoreMan(object):
    def __init__(self, containers_dir=None):
        if containers_dir is None:
            self.containers_dir = DEFAULT_CONTAINERS_DIR
        else:
            self.containers_dir = containers_dir
        self.processes = {}  # PID -> (stdin, stdout, stderr)
    def create_container(self, container_id, config):
        if not conatiner_id.isalnum():
            raise ValueError('container_id can only be alpha-numeric')
        
        
        # config = {base_env, ports, source_template, etc})
        # mkdirs
        # write config file
        subprocess.call_check(['mkenv', container_id])

    def create_process(command, env)

        # open container config file
        # look for runtime file
        # how to clean-up when all processes have exited?

    def list_processes(self):
        return self.processes.keys()
    def list_containers(self):
        return os.listdir(self.containers_dir)
    def get_container_info(self, container_id):
        config = os.path.join(self._get_container_dir(container_id), 'container.json')
        return json.load(config)
    #def get_container_contents(self, container_id):
    def get_process_info(self, process_id):
        pass
    def remove_container(self, container_id):
        pass
    def remove_process(self, process_id):
        pass
    def write_to_process(self, process_id, message):
        pass
    def _get_container_dir(self, container_id):
        return os.path.join(self.containers_dir, container_id)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
