from typing import List, Type, TypedDict


class __TenseBlock(TypedDict):
    tense: str
    forms: List[str]


TENSE_BLOCKS = List[__TenseBlock]


class __TenseBlockV2__(TypedDict):
    tense: str
    forms: List[str]
    translations: List[str]


class __TenseBlocksV2__(TypedDict):
    result: List[__TenseBlockV2__]


TENSE_BLOCKS_V2 = Type[__TenseBlocksV2__]
