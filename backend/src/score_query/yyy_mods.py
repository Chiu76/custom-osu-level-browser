from typing import Literal
from enum import Enum
from sqlalchemy import Select, and_

from src.common.models.scores import Score


MODS_FIELDS = Literal[
    'none',
    'nofail',
    'easy',
    'touchdevice',
    'hidden',
    'hardrock',
    'suddendeath',
    'doubletime',
    'relax',
    'halftime',
    'nightcore',
    'flashlight',
    'autoplay',
    'spunout',
    'relax2',
    'perfect',
    'key4',
    'key5',
    'key6',
    'key7',
    'key8',
    'fadein',
    'random',
    'cinema',
    'target',
    'key9',
    'keycoop',
    'key1',
    'key3',
    'key2',
    'scorev2',
    'mirror',
]

MODS_FIELDS_ALTERNATIVES = Literal[
    'nm',
    'nf',
    'ez',
    'td',
    'hd',
    'hr',
    'sd',
    'dt',
    'rx',
    'ht',
    'nc',
    'fl',
    'ap',
    'so',
    'rx2',
    'pf',
    'k4',
    'k5',
    'k6',
    'k7',
    'k8',
    'fi',
    'rd',
    'cm',
    'tg',
    'k9',
    'kc',
    'k1',
    'k3',
    'k2',
    'sv2',
    'mr',
]

MODS_VALUES = {
    'none': 0,
    'nofail': 1,
    'easy': 2,
    'touchdevice': 4,
    'hidden': 8,
    'hardrock': 16,
    'suddendeath': 32,
    'doubletime': 64,
    'relax': 128,
    'halftime': 256,
    'nightcore': 576,
    'flashlight': 1024,
    'autoplay': 2048,
    'spunout': 4096,
    'Relax2': 8192,
    'perfect': 16416,
    'key4': 32768,
    'key5': 65536,
    'key6': 131072,
    'key7': 262144,
    'key8': 524288,
    'fadein': 1048576,
    'random': 2097152,
    'cinema': 4194304,
    'target': 8388608,
    'key9': 16777216,
    'keycoop': 33554432,
    'key1': 67108864,
    'key3': 134217728,
    'key2': 268435456,
    'scorev2': 536870912,
    'mirror': 1073741824,
}

MODS_VALUES_ALTERNATIVES = {
    'nm': 0,
    'nf': 1,
    'ez': 2,
    'td': 4,
    'hd': 8,
    'hr': 16,
    'sd': 32,
    'dt': 64,
    'rx': 128,
    'ht': 256,
    'nc': 576,
    'fl': 1024,
    'ap': 2048,
    'so': 4096,
    'rx2': 8192,
    'pf': 16416,
    'k4': 32768,
    'k5': 65536,
    'k6': 131072,
    'k7': 262144,
    'k8': 524288,
    'fi': 1048576,
    'rd': 2097152,
    'cm': 4194304,
    'tg': 8388608,
    'k9': 16777216,
    'kc': 33554432,
    'k1': 67108864,
    'k3': 134217728,
    'k2': 268435456,
    'sv2': 536870912,
    'mr': 1073741824,
}


def get_mod_value(mod: MODS_FIELDS | MODS_FIELDS_ALTERNATIVES) -> int:
    mod_values = MODS_VALUES | MODS_VALUES_ALTERNATIVES
    if not mod in mod_values.keys():
        raise ValueError(f'Received invalid mod value, not present in `MODS_VALUES` or `MODS_FIELDS_ALTERNATIVES` mappings: {mod}')
    return mod_values[mod]


def apply_mods(
    stmt: Select,
    mods_exact: list[MODS_FIELDS | MODS_FIELDS_ALTERNATIVES],
    mods_include: list[MODS_FIELDS | MODS_FIELDS_ALTERNATIVES],
    mods_exclude: list[MODS_FIELDS | MODS_FIELDS_ALTERNATIVES],
) -> Select:    
    if mods_exact:
        mods_exact_value = sum([get_mod_value(mod) for mod in mods_exact])
        return stmt.where(Score.mods == mods_exact_value)
    
    conditions = []
    
    if mods_include:
        for mod_include in mods_include:
            mod_include_value = get_mod_value(mod_include)
            conditions.append(Score.mods.op('&')(mod_include_value) == mod_include_value)
    
    if mods_exclude:
        for mod_exclude in mods_exclude:
            mod_exclude_value = get_mod_value(mod_exclude)
            conditions.append(Score.mods.op('&')(mod_exclude_value) == 0)

    if not conditions: 
        return stmt
    
    return stmt.where(and_(*conditions))
