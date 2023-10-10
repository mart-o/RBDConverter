import datetime
from typing import TextIO
from xml.etree import ElementTree

import config
from format import time_to_str
from format import datetime_to_str


def write_flow_events(file: TextIO, xml_root: ElementTree.Element, start_time: datetime.datetime):
    write_header(file, start_time, 'FlowD\\flow')

    scored_events = None
    for item in xml_root:
        if item.tag == 'ScoredEvents':
            scored_events = item
            break

    if scored_events is None:
        print("ERROR: Unable to find <ScoredEvents> tag in sleep_profile.xml")
        return

    for event in scored_events:
        if event.tag != "ScoredEvent":
            continue
        write_flow_event(file, event, start_time, config.flow_event_map)


def write_classification_arousal(file: TextIO, xml_root: ElementTree, start_time: datetime.datetime):
    write_header(file, start_time, 'KorrelationMA\\MAK')


def write_header(file: TextIO, start_time: datetime.datetime, signal_id: str):
    file.writelines('Signal ID: ' + signal_id + '\n')
    file.writelines('Start Time: ' + datetime_to_str(start_time) + '\n')
    file.writelines('Unit: s\n')
    file.writelines('Signal Type: Impuls\n\n')


def write_flow_event(
        file: TextIO,
        event: ElementTree.Element,
        start_time: datetime.datetime,
        flow_event_map: dict[str, str]):
    start = None
    duration = None
    name = None
    event_name = None

    for item in event:
        if item.tag == 'Start':
            start = start_time + datetime.timedelta(seconds=float(item.text))
        elif item.tag == 'Duration':
            duration = datetime.timedelta(seconds=float(item.text))
        elif item.tag == 'Name':
            name = item.text
        elif item.tag == 'EventName':
            event_name = item.text

    if start is None or duration is None or name is None or event_name is None:
        print("WARNING: invalid <ScoredEvent>, skipping")
        return

    sleep_stage = flow_event_map.get(event_name)
    if sleep_stage is None:
        sleep_stage = flow_event_map.get(name)
        if sleep_stage is None:
            return

    file.writelines(
        "{0}-{1}; {2:d};{3}\n".format(
            time_to_str(start),
            time_to_str(start + duration),
            round(duration.seconds, 0),
            sleep_stage))
