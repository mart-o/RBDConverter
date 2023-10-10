import datetime
from xml.etree import ElementTree
from typing import TextIO
import format
import config
import logger


def write_sleep_profile(file: TextIO,
                        xml_root: ElementTree.Element,
                        start_time: datetime.datetime):
    write_header(file, start_time, "N4,N3,N2,N1,REM,Wake,Movement")
    write_content(file, xml_root, start_time, config.sleep_stage_map)


def write_sleep_profile_snore(file: TextIO,
                              xml_root: ElementTree.Element,
                              start_time: datetime.datetime):
    write_header(file, start_time, "N4,N3,N2,N1,SNORE,Wake,Movement")
    write_content(file, xml_root, start_time, config.snore_map)


def write_header(file: TextIO, start_time: datetime.datetime, event_list: str):
    file.writelines('Signal ID: SchlafProfil\\profil\n')
    file.writelines('Start Time: ' + format.datetime_to_str(start_time) + '\n')
    file.writelines('Unit:\n')
    file.writelines('Signal Type: Discret\n')
    file.writelines('Events list: ' + event_list + '\n')
    file.writelines('Rate: 30 s\n\n')


def write_content(file: TextIO,
                  xml_root: ElementTree.Element,
                  start_time: datetime.datetime,
                  sleep_stage_map: dict[str, str]):

    epoch_length = read_epoch_length(xml_root)
    time_step = datetime.timedelta(seconds=epoch_length)

    sleep_stages = None
    for item in xml_root:
        if item.tag == 'SleepStages':
            sleep_stages = item
            break

    if sleep_stages is None:
        raise Exception("Unable to find <SleepStages> tag in sleep_profile.xml")

    current_time = start_time
    for stage in sleep_stages:
        if stage.text in sleep_stage_map:
            write = format.time_to_str(current_time) + '; ' + sleep_stage_map[stage.text] + '\n'
            file.writelines(write)
        else:
            logger.warning("Unexpected SleepStage: " + stage.text + ". Skipping")
        current_time += time_step


def read_epoch_length(xml_root: ElementTree.Element) -> float:
    default_epoch_length = 30
    for item in xml_root:
        if item.tag == 'EpochLength':
            try:
                return float(item.text)
            except ValueError:
                logger.warning("<EpochLength> value is not a valid number. Using default value (30)")
                return default_epoch_length
    logger.warning("WARNING: unable to find <EpochLength>. Using default value (30)")
    return default_epoch_length


