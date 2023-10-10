import os
import pyedflib
import datetime
from xml.etree import ElementTree

import logger
import config
from flow_events import write_flow_events
from flow_events import write_classification_arousal
from sleep_profile import write_sleep_profile
from sleep_profile import write_sleep_profile_snore


# Runs convert operation for every subdirectory for parent_dir
def multi_convert(parent_dir: str):
    if not parent_dir.endswith(os.path.sep):
        parent_dir = parent_dir + os.path.sep

    for item in os.listdir(parent_dir):
        if os.path.isdir(os.path.join(parent_dir, item)):
            input_dir = os.path.join(parent_dir, item)
            output_dir = os.path.join(parent_dir, 'converted', item)

            if not os.path.exists(os.path.join(parent_dir, 'converted')):
                os.mkdir(os.path.join(parent_dir, 'converted'))

            convert(input_dir, output_dir)


# Runs convert operation for one directory
def convert(input_dir: str, output_dir: str):
    if output_dir == '':
        output_dir = os.path.join(input_dir, 'converted')

    try:
        logger.info(f'Converting directory: {input_dir}')
        do_convert(input_dir, output_dir)
        logger.info(f'Successfully converted directory {input_dir}')
    except Exception as ex:
        logger.error(f'Convert operation failed: {ex}')


def do_convert(input_dir: str, output_dir: str):
    edf_path = find_edf_file(input_dir)
    xml_path = os.path.join(input_dir, 'sleep_profile.xml')
    if not os.path.isfile(xml_path):
        raise Exception('sleep_profile.xml file is not found')

    start_time = read_edf_start_time(edf_path)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    tree = ElementTree.parse(xml_path)
    xml_root = tree.getroot()
    config.load()

    with open(os.path.join(output_dir, 'Flow Events.txt'), 'w', encoding="utf-8") as file:
        write_flow_events(file, xml_root, start_time)

    with open(os.path.join(output_dir, 'Sleep profile.txt'), 'w', encoding='utf-8') as file:
        write_sleep_profile(file, xml_root, start_time)

    with open(os.path.join(output_dir, 'Sleep profile SNORE.txt'), 'w', encoding='utf-8') as file:
        write_sleep_profile_snore(file, xml_root, start_time)

    with open(os.path.join(output_dir, 'Classification Arousals.txt'), 'w', encoding='utf-8') as file:
        write_classification_arousal(file, xml_root, start_time)

    pyedflib.highlevel.rename_channels(edf_path, config.edf_channel_map, os.path.join(output_dir, "converted.edf"))


def find_edf_file(input_dir: str) -> str:
    if not input_dir.endswith(os.path.sep):
        input_dir = input_dir + os.path.sep

    for file in os.listdir(input_dir):
        if file.endswith('.edf'):
            return os.path.join(input_dir, file)

    raise Exception('EDF file is not found')


def read_edf_start_time(edf_path: str) -> datetime.datetime:
    file = pyedflib.EdfReader(edf_path)
    start_time = datetime.datetime(
        year=file.startdate_year, month=file.startdate_month, day=file.startdate_day, hour=file.starttime_hour,
        minute=file.starttime_minute, second=file.starttime_second, microsecond=file.starttime_subsecond * 10)
    file.close()
    return start_time
