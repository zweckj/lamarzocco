"""Constants for the La Marzocco integration."""

from lmcloud.const import MODEL_LMU

DOMAIN = "lamarzocco"

"""Set polling interval at 20s."""
POLLING_INTERVAL = 30

""" Delay to wait before refreshing state"""
UPDATE_DELAY = 3

"""Configuration parameters"""
CONF_SERIAL_NUMBER = "serial_number"
CONF_CLIENT_ID = "client_id"
CONF_CLIENT_SECRET = "client_secret"
CONF_KEY = "key"
CONF_MACHINE_NAME = "machine_name"
CONF_MODEL_NAME = "model_name"
CONF_USE_WEBSOCKET = "use_websocket"
CONF_DEFAULT_CLIENT_ID = "7_1xwei9rtkuckso44ks4o8s0c0oc4swowo00wgw0ogsok84kosg"
CONF_DEFAULT_CLIENT_SECRET = "2mgjqpikbfuok8g4s44oo4gsw0ks44okk4kc4kkkko0c8soc8s"

DEFAULT_PORT_CLOUD = 8081

DEFAULT_NAME = "Espresso Machine"

SCHEMA = "schema"
MODELS_SUPPORTED = "supported"
FUNC = "func"

HOST = "host"

'''Migrated from lmdirect'''
ENABLED = "Enabled"

MODEL_GS3_AV = "GS3 AV"
MODEL_GS3_MP = "GS3 MP"
MODEL_LM = "Linea Mini"

MODEL_NAME = "model_name"

DATE_RECEIVED = "date_received"
POWER = "power"

TEMP_COFFEE = "coffee_temp"
TEMP_STEAM = "steam_temp"
TSET_COFFEE = "coffee_set_temp"
TSET_STEAM = "steam_set_temp"

DOSE = "dose"

DOSE_HOT_WATER = "dose_hot_water"

ENABLE_PREBREWING = "enable_prebrewing"
ENABLE_PREINFUSION = "enable_preinfusion"

PREBREWING = "prebrewing"
PREINFUSION = "preinfusion"
TON = "ton"
TOFF = "toff"

DRINKS = "drinks"

CONTINUOUS = "continuous"
TOTAL_COFFEE = "total_coffee"
HOT_WATER = "hot_water"
TOTAL_COFFEE_ACTIVATIONS = "total_coffee_activations"
DRINKS_HOT_WATER = "drinks_hot_water"
TOTAL_FLUSHING = "total_flushing"
MACHINE_NAME = "machine_name"
SERIAL_NUMBER = "serial_number"
FRONT_PANEL_DISPLAY = "front_panel_display"


STEAM_BOILER_ENABLE = "steam_boiler_enable"
HEATING_STATE = "heating_state"

WATER_RESERVOIR_CONTACT = "water_reservoir_contact"
BREW_ACTIVE = "brew_active"

COFFEE_HEATING_ELEMENT_HOURS = "coffee_heating_element_hours"
STEAM_HEATING_ELEMENT_HOURS = "steam_heating_element_hours"


UPDATE_AVAILABLE = "update_available"

ON = "on"
OFF = "off"
MIN = "min"
AUTO = "auto"
TIME = "time"

GLOBAL = "global"
MON = "mon"
TUE = "tue"
WED = "wed"
THU = "thu"
FRI = "fri"
SAT = "sat"
SUN = "sun"

DAYS = [MON, TUE, WED, THU, FRI, SAT, SUN]

"""Data Types"""
TYPE_MAIN = 1
TYPE_PREBREW = 2
TYPE_AUTO_ON_OFF = 3
TYPE_COFFEE_TEMP = 4
TYPE_STEAM_TEMP = 5
TYPE_DRINK_STATS = 6
TYPE_WATER_RESERVOIR_CONTACT = 7
TYPE_PREINFUSION = 8
TYPE_START_BACKFLUSH = 9
TYPE_STEAM_BOILER_ENABLE = 10
TYPE_BREW_ACTIVE = 11

SUPPORTED = "supported"
MODELS = [MODEL_GS3_AV, MODEL_GS3_MP, MODEL_LM, MODEL_LMU]

SET_PREBREW_TIMES = "set_prebrew_times"
SET_PREINFUSION_TIME = "set_preinfusion_time"
SET_DOSE = "set_dose"
SET_DOSE_HOT_WATER = "set_dose_hot_water"
SET_AUTO_ON_OFF_ENABLE = "set_auto_on_off_enable"
SET_AUTO_ON_OFF_TIMES = "set_auto_on_off_times"

""" end migrated lmdirect """

"""List of attributes for each entity based on model."""
ATTR_MAP_MAIN_GS3_AV = [
    DATE_RECEIVED,
    MACHINE_NAME,
    MODEL_NAME,
    UPDATE_AVAILABLE,
    HEATING_STATE,
    (DOSE, "k1"),
    (DOSE, "k2"),
    (DOSE, "k3"),
    (DOSE, "k4"),
    (DOSE, "k5"),
    DOSE_HOT_WATER,
    # FRONT_PANEL_DISPLAY,
]

ATTR_MAP_MAIN_GS3_MP = [
    DATE_RECEIVED,
    MACHINE_NAME,
    MODEL_NAME,
    UPDATE_AVAILABLE,
    HEATING_STATE,
    # FRONT_PANEL_DISPLAY,
]

ATTR_MAP_MAIN_LM = [
    DATE_RECEIVED,
    MACHINE_NAME,
    MODEL_NAME,
    UPDATE_AVAILABLE,
    HEATING_STATE,
]

ATTR_MAP_STEAM_BOILER_ENABLE = [
    DATE_RECEIVED,
]

ATTR_MAP_PREBREW_GS3_AV = [
    DATE_RECEIVED,
    (PREBREWING, TON, "k1"),
    (PREBREWING, TON, "k2"),
    (PREBREWING, TON, "k3"),
    (PREBREWING, TON, "k4"),
    (PREBREWING, TOFF, "k1"),
    (PREBREWING, TOFF, "k2"),
    (PREBREWING, TOFF, "k3"),
    (PREBREWING, TOFF, "k4"),
]

ATTR_MAP_PREINFUSION_GS3_AV = [
    DATE_RECEIVED,
    (PREINFUSION, "k1"),
    (PREINFUSION, "k2"),
    (PREINFUSION, "k3"),
    (PREINFUSION, "k4"),
]

ATTR_MAP_PREINFUSION_LM = [
    DATE_RECEIVED,
    (PREINFUSION, "k1"),
]

ATTR_MAP_PREBREW_LM = [
    DATE_RECEIVED,
    (PREBREWING, TON, "k1"),
    (PREBREWING, TOFF, "k1"),
]

ATTR_MAP_COFFEE = [
    DATE_RECEIVED,
    # COFFEE_HEATING_ELEMENT_HOURS,
]

ATTR_MAP_STEAM = [
    DATE_RECEIVED,
    # STEAM_HEATING_ELEMENT_HOURS,
]

ATTR_MAP_AUTO_ON_OFF = [
    DATE_RECEIVED,
    (SUN, AUTO),
    (SUN, ON, TIME),
    (SUN, OFF, TIME),
    (MON, AUTO),
    (MON, ON, TIME),
    (MON, OFF, TIME),
    (TUE, AUTO),
    (TUE, ON, TIME),
    (TUE, OFF, TIME),
    (WED, AUTO),
    (WED, ON, TIME),
    (WED, OFF, TIME),
    (THU, AUTO),
    (THU, ON, TIME),
    (THU, OFF, TIME),
    (FRI, AUTO),
    (FRI, ON, TIME),
    (FRI, OFF, TIME),
    (SAT, AUTO),
    (SAT, ON, TIME),
    (SAT, OFF, TIME),
]

ATTR_MAP_DRINK_STATS_GS3_AV = [
    DATE_RECEIVED,
    (DRINKS, "k1"),
    (DRINKS, "k2"),
    (DRINKS, "k3"),
    (DRINKS, "k4"),
    CONTINUOUS,
    TOTAL_FLUSHING,
    # DRINKS_HOT_WATER,
    # HOT_WATER,
    TOTAL_COFFEE,
    # TOTAL_COFFEE_ACTIVATIONS,
]

ATTR_MAP_DRINK_STATS_GS3_MP_LM = [
    DATE_RECEIVED,
    (DRINKS, "k1"),
    # CONTINUOUS,
    TOTAL_FLUSHING,
    # DRINKS_HOT_WATER,
    # HOT_WATER,
    TOTAL_COFFEE,
    # TOTAL_COFFEE_ACTIVATIONS,
]

ATTR_MAP_WATER_RESERVOIR = [
    WATER_RESERVOIR_CONTACT
]

ATTR_MAP_BREW_ACTIVE = [
    BREW_ACTIVE
]

ENTITY_TAG = "tag"
ENTITY_TEMP_TAG = "temp_tag"
ENTITY_TSET_TAG = "tset_tag"
ENTITY_TSTATE_TAG = "tstate_tag"
ENTITY_NAME = "name"
ENTITY_MAP = "map"
ENTITY_TYPE = "type"
ENTITY_ICON = "icon"
ENTITY_FUNC = "func"
ENTITY_CLASS = "class"
ENTITY_UNITS = "units"

PLATFORM = "platform"
PLATFORM_SENSOR = "sensor"
PLATFORM_SWITCH = "switch"

MODE_HEAT = "heat"
MODE_OFF = "off"

OPERATION_MODES = [MODE_HEAT, MODE_OFF]
