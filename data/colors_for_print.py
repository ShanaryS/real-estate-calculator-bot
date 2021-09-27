"""Add colors to print output where necessary"""

from enum import Enum, unique


@unique
class PrintColors(Enum):
    """Used for adding color to print output"""
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


BAD = PrintColors.FAIL.value
OK = PrintColors.WARNING.value
GOOD = PrintColors.OKCYAN.value
GREAT = PrintColors.OKGREEN.value
END = PrintColors.ENDC.value
