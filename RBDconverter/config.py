import configparser

edf_channel_map: dict[str, str] = {}
flow_event_map: dict[str, str] = {}
sleep_stage_map: dict[str, str] = {}
snore_map: dict[str, str] = {}


def load():
    global sleep_stage_map, edf_channel_map, flow_event_map, snore_map

    config = configparser.ConfigParser()
    config.optionxform = lambda key: key
    config.read('config.ini', encoding='utf8')

    edf_channel_map = read_map(config['edf_channel_map'])
    flow_event_map = read_map(config['flow_event_map'])
    sleep_stage_map = read_map(config['sleep_stage_map'])
    snore_map = read_map(config['snore_map'])


def read_map(config_section) -> dict[str, str]:
    result = {}
    for key in config_section:
        result[key] = config_section[key]
    return result
