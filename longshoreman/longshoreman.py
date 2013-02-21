#!/usr/bin/env python


"""
Longshoreman corrals containers.

"""
import json
import os

import gevent_subprocess as subprocess

from .utils import get_free_port

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
        self._validate_potential_container_id(container_id)
        # create base container
        # allocate ports
        for p in config.get('ports', []):
            config['ports'][p] = get_free_port(self._get_allocated_ports())
        # write config file
        json.dump(open(self._get_container_config_filepath(), 'w'))
        subprocess.call_check(['mkenv', container_id])

    def create_process(self, container_id, command, config)

        self._validate_existing_container_id(container_id)
        # open container config file
        # look for runtime file
        # how to clean-up when all processes have exited?

    def list_processes(self):
        return self.processes.keys()
    def list_containers(self):
        return os.listdir(self.containers_dir)
    def _get_container_config_filepath(self, container_id):
        container_dir = self._get_container_dir(container_id)
        return os.path.join(container_dir, 'container.json')
    def get_container_config(self, container_id):
        self._validate_existing_container_id(container_id)
        config = self._get_container_config_filepath()
        return json.load(open(config))
    def get_container_info(self, container_id):
        self._validate_existing_container_id(container_id)
        raise NotImplementedError
    #def get_container_contents(self, container_id):
    def get_process_info(self, process_id):
        pass
    def remove_container(self, container_id):
        self._validate_existing_container_id(container_id)
    def remove_process(self, process_id):
        pass
    def write_to_process(self, process_id, message):
        pass
    def _get_container_dir(self, container_id):
        return os.path.join(self.containers_dir, container_id)
    def _validate_container_id(self, container_id):
        # check that the name is valid
        if not conatiner_id.isalnum():
            raise ValueError('container_id can only be alpha-numeric')

    def _validate_potential_container_id(self, container_id):
        # check that the name is valid, and that no such container exists
        self._validate_container_id(container_id)
        if container_id in self.list_containers():
            raise ValueError(
                'A container with ID %s already exists' % container_id)

    def _validate_existing_container_id(self, container_id):
        # check that the name is valid, and that the container exists
        self._validate_container_id(container_id)
        if container_id not in self.list_containers():
            raise ValueError(
                'No container with ID %s exists' % container_id)
    def _get_allocated_ports(self):
        ports = []
        for c in self.list_containers():
            config = self.get_container_config(c)
            ports.extend(info.get('ports', {}).values())
        return ports

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
