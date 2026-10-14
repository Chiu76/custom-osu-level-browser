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
    'pf',
    'sv2',
]

MODS_VALUES = {
    'none': 0,
    
    'nofail': 1,
    'nf': 1,
    
    'easy': 2,
    'ez': 2,
    
    'touchdevice': 4,
    'td': 4,
    
    'hidden': 8,
    'hd': 8,
    
    'hardrock': 16,
    'hr': 16,
    
    'suddendeath': 32,
    'sd': 32,
    
    'doubletime': 64,
    'dt': 64,
    
    'relax': 128,
    'rx': 128,
    
    'halftime': 256,
    'ht': 256,
    
    'nightcore': 576,
    'nc': 576,
    
    'flashlight': 1024,
    'fl': 1024,
    
    'autoplay': 2048,
    'ap': 2048,
    
    'spunout': 4096,
    'so': 4096,
    
    'Relax2': 8192,
    
    'perfect': 16416,
    'pf': 16416,
    
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
    'sv2': 536870912,
    
    'mirror': 1073741824,
}


def get_mod_value(mod: MODS_FIELDS | MODS_FIELDS_ALTERNATIVES) -> int:
    if not mod in MODS_VALUES.keys():
        raise ValueError(f'Received invalid mod value, not present in `MODS_VALUES` mapping: {mod}')
    return MODS_VALUES[mod]


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
