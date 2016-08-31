# Creates config file for webserver based on create_conf.yaml and data downloaded based on that file.

from __future__ import print_function
import sys
import requests
import yaml
from collections import OrderedDict


class UnsortableList(list):
    def sort(self, *args, **kwargs):
        pass


class UnsortableOrderedDict(OrderedDict):
    def items(self, *args, **kwargs):
        return UnsortableList(OrderedDict.items(self, *args, **kwargs))

# Hack to make yaml print out somewhat in order
yaml.add_representer(UnsortableOrderedDict, yaml.representer.SafeRepresenter.represent_dict)

FIX_SCRIPT = 'bigBedToBed'
YAML_CONFIG_FILE = 'create_conf.yaml'

# load global configuration from YAML_CONFIG_FILE
yaml_config = {}
with open(YAML_CONFIG_FILE) as infile:
    yaml_config = yaml.safe_load(infile)
DATA_SOURCE_URL = yaml_config['DATA_SOURCE_URL']
CONFIG_FILENAME = yaml_config['CONFIG_FILENAME']
BINDING_MAX_OFFSET = yaml_config['BINDING_MAX_OFFSET']
GENOMES_FILENAME = yaml_config['GENOMES_FILENAME']
GENOME_SPECIFIC_DATA = yaml_config['GENOME_SPECIFIC_DATA']
SORT_MAX_GUESS_DEFAULT = yaml_config['SORT_MAX_GUESS_DEFAULT']
SORT_MAX_GUESS = yaml_config['SORT_MAX_GUESS']
CORE_SETTINGS_DEFAULT = yaml_config['CORE_SETTINGS_DEFAULT']
CORE_SETTINGS = yaml_config['CORE_SETTINGS']


def create_config_file(trackhub_data, output_filename):
    genome_data = []
    genome_to_track = trackhub_data.get_genomes()
    for genome in sorted(genome_to_track.keys()):
        genome_specific = GENOME_SPECIFIC_DATA.get(genome, {})
        track_filename = genome_to_track[genome]
        track_data = []
        prediction_lists = []
        for track, url in trackhub_data.get_track_data(track_filename):
            sort_max_guess = SORT_MAX_GUESS.get(track, SORT_MAX_GUESS_DEFAULT)
            core_settings = CORE_SETTINGS.get(track, CORE_SETTINGS_DEFAULT)
            prediction_data = {
                'name': track,
                'url': url,
                'fix_script': FIX_SCRIPT,
                'sort_max_guess': sort_max_guess,
                'core_offset': core_settings[0],
                'core_length': core_settings[1],
            }
            prediction_lists.append(prediction_data)
        genome_data.append({
            'genome': '' + genome,
            'genome_file': "goldenPath/{}/bigZips/{}.2bit".format(genome, genome),
            'trackhub_url': genome_specific['trackhub_url'],
            'ftp_files': genome_specific['ftp_files'],
            'gene_lists': genome_specific['gene_lists'],
            'prediction_lists': prediction_lists,
        })

    config_data = {
        'binding_max_offset': BINDING_MAX_OFFSET,
        'download_dir': '/tmp/pred_data',
        'genome_data': genome_data,
    }
    with open(output_filename, 'w') as outfile:
        yaml.safe_dump(config_data, outfile, default_flow_style=False)
    print("Wrote config file to {}".format(output_filename))


def get_genomes(remote_data):
    genome = ''
    genome_to_track = {}
    lines = remote_data.get_lines_for_path(GENOMES_FILENAME)
    for name, value in get_key_value_list(lines):
        if name == 'genome':
            genome = value
        if name == 'trackDb':
            genome_to_track[genome] = '{}/{}'.format(remote_data.data_source_url, value)
    return genome_to_track


def get_key_value_list(lines):
    result = []
    for line in lines:
        line = line.strip()
        if line:
            parts = line.split(" ", 1)
            name = parts[0]
            value = parts[1]
            result.append((name, value))
    return result


class TrackHubData(object):
    def __init__(self, data_source_url):
        self.remote_data = RemoteData(data_source_url)

    def get_genomes(self):
        genome = ''
        genome_to_track = {}
        lines = self.remote_data.get_lines_for_path(GENOMES_FILENAME)
        for name, value in get_key_value_list(lines):
            if name == 'genome':
                genome = value
            if name == 'trackDb':
                genome_to_track[genome] = value
        return genome_to_track

    def get_track_data(self, track_filename):
        result = []
        track = ''
        lines = self.remote_data.get_lines_for_path(track_filename)
        for name, value in get_key_value_list(lines):
            if name == 'track':
                track = value
            if name == 'bigDataUrl':
                url = self.remote_data.create_url(value)
                result.append((track, url))
        return result


class RemoteData(object):
    def __init__(self, data_source_url):
        self.data_source_url = data_source_url

    def get_text_for_path(self, path):
        url = self.create_url(path)
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def get_lines_for_path(self, path):
        return self.get_text_for_path(path).split('\n')

    def create_url(self, suffix):
        return '{}/{}'.format(self.data_source_url, suffix)


if __name__ == '__main__':
    create_config_file(TrackHubData(DATA_SOURCE_URL), CONFIG_FILENAME)
