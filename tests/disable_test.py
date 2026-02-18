"""
tests.disable_test.py
=====================
"""

# pylint: disable=too-many-lines
import pytest

from docsig.messages import E

from . import FixtureInitFile, FixtureMain

ES = (
    E[402].ref,
    E[202].ref,
    E[203].ref,
    E[502].ref,
    E[502].ref,
    E[201].ref,
    E[303].ref,
)
SYMBOLIC = [
    (E[402].ref, E[402].symbolic),
    (E[202].ref, E[202].symbolic),
    (E[203].ref, E[203].symbolic),
    (E[502].ref, E[502].symbolic),
    (E[503].ref, E[503].symbolic),
    (E[201].ref, E[201].symbolic),
]
DISABLE_FILE_1 = '''
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """
'''
DISABLE_FILE_2 = '''
# docsig: disable
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """
'''
DISABLE_FILE_3 = '''
def function_1(param1, param2, param3) -> None:  # docsig: disable
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """
'''
DISABLE_FILE_4 = '''
# docsig: disable=SIG402
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """

'''
DISABLE_FILE_5 = '''
# docsig: disable=SIG402,SIG202
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """

'''
DISABLE_FILE_6 = '''

def function_1(param1, param2, param3) -> None:  # docsig: disable=SIG402
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """

'''
DISABLE_FILE_7 = '''
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(  # docsig: disable=SIG402,SIG202,SIG201,SIG303
    param1, param2, param3
) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """

'''
ENABLE_FILE_1 = '''
# docsig: disable
# docsig: enable
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """

'''
ENABLE_FILE_2 = '''

# docsig: disable
def function_1(param1, param2, param3) -> None:  # docsig: enable
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """

'''
ENABLE_FILE_3 = '''
# docsig: disable
# docsig: enable=SIG402
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """

'''
ENABLE_FILE_4 = '''

# docsig: disable
# docsig: enable=SIG402,SIG202
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """

'''
ENABLE_FILE_5 = '''

# docsig: disable
def function_1(param1, param2, param3) -> None:  # docsig: enable=SIG402
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """

'''
ENABLE_FILE_6 = '''

# docsig: disable
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(  # docsig: enable=SIG402,SIG202,SIG201,SIG303
    param1, param2, param3
) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """

'''
INLINE_DISABLE_TEMPLATE = '''
def function_1(param1, param2, param3) -> None:  # docsig: disable={rules}
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:  # docsig: disable={rules}
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:  # docsig: disable={rules}
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:  # docsig: disable={rules}
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:  # docsig: disable={rules}
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:  # docsig: disable={rules}
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:  # docsig: disable={rules}
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """
'''
MODULE_LEVEL_DISABLE_TEMPLATE = '''
# docsig: disable={rules}
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """
'''
INLINE_ENABLE_TEMPLATE = '''
# docsig: disable
def function_1(param1, param2, param3) -> None:  # docsig: enable={rules}
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:  # docsig: enable={rules}
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:  # docsig: enable={rules}
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:  # docsig: enable={rules}
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:  # docsig: enable={rules}
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:  # docsig: enable={rules}
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:  # docsig: enable={rules}
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """
'''
MODULE_LEVEL_ENABLE_TEMPLATE = '''
# docsig: disable
# docsig: enable={rules}
def function_1(param1, param2, param3) -> None:
    """Docstring summary.

    :param param2: Description of param2.
    :param param3: Description of param3.
    :param param1: Description of param1.
    """

def function_2(param1, param2) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_3(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    """

def function_4(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    :return: Return description.
    """

def function_5(param1, param2, param3) -> int:
    """Docstring summary.

    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_6(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param param3: Description of param3.
    """

def function_7(param1, param2, param3) -> None:
    """Docstring summary.

    :param param1: Description of param1.
    :param param1: Description of param1.
    :param param2: Description of param2.
    :param: Description of param.
    """
'''


def test_no_disables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test the series of functions with no `disable` comments.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_1)
    main(".")
    std = capsys.readouterr()
    assert all(E.from_ref(i).ref in std.out for i in ES)


@pytest.mark.parametrize("code,symbolic", SYMBOLIC)
def test_commandline_disables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    code: str,
    symbolic: str,
) -> None:
    """Test the series of functions with `disable` commandline arg.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param code: Rule to disable.
    :param symbolic: Rule symbolic code to comment.
    """
    init_file(DISABLE_FILE_1)
    main(".", "--disable", code, test_flake8=False)
    std = capsys.readouterr()
    assert E.from_ref(code).ref not in std.out
    assert all(
        E.from_ref(i[0]).ref in std.out for i in SYMBOLIC if i[0] != code
    )
    init_file(DISABLE_FILE_1)
    main(".", "--disable", symbolic, test_flake8=False)
    std = capsys.readouterr()
    assert symbolic not in std.out
    assert all(i[1] in std.out for i in SYMBOLIC if i[1] != symbolic)


def test_unknown_commandline_disables(main: FixtureMain) -> None:
    """Test invalid `disable` option provided.

    :param main: Mock ``main`` function.
    """
    assert (
        main(".", "--disable", "unknown", test_flake8=False)
        == "unknown option to disable 'unknown'"
    )


def test_module_disables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test disabling entire module with `disable` comment.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_2)
    main(".")
    std = capsys.readouterr()
    assert not any(i in std.out for i in ES)


def test_single_function_disable(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test disabling single function with `disable` comment.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_3)
    main(".")
    std = capsys.readouterr()
    assert "function_1" not in std.out
    assert all(f"function_{i}" in std.out for i in range(2, 8))


def test_module_single_error_disables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test disabling entire module with specific `disable` comment.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_4)
    main(".")
    std = capsys.readouterr()
    assert E.from_ref(ES[0]).ref not in std.out
    assert all(E.from_ref(i).ref in std.out for i in ES if i != ES[0])


def test_module_comma_separated_error_disables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test disabling module with comment of several specific errors.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_5)
    main(".")
    std = capsys.readouterr()
    excluded = ES[0], ES[1]
    assert not any(E.from_ref(i).ref in std.out for i in excluded)
    assert all(E.from_ref(i).ref in std.out for i in ES if i not in excluded)


def test_single_function_single_error_disable(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test disabling single function with specific `disable` comment.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_6)
    main(".")
    std = capsys.readouterr()
    assert "function_1" not in std.out
    assert all(f"function_{i}" in std.out for i in range(2, 8))


def test_single_function_comma_separated_error_disable(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test disabling function with comment of several specific errors.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(DISABLE_FILE_7)
    main(".")
    std = capsys.readouterr()
    assert "function_6" not in std.out
    assert all(f"function_{i}" in std.out for i in range(1, 8) if i != 6)


def test_module_enables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test individual checks.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(ENABLE_FILE_1)
    main(".")
    std = capsys.readouterr()
    assert all(E.from_ref(i).ref in std.out for i in ES)


def test_single_function_enable(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test enabling entire module with enable comment.

    Prior to `enable` add the `disable` directive.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(ENABLE_FILE_2)
    main(".")
    std = capsys.readouterr()
    assert "function_1" in std.out
    assert not any(f"function_{i}" in std.out for i in range(2, 8))


def test_module_single_error_enables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test enabling entire module with enable comment.

    Prior to `enable` add the `disable` directive.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(ENABLE_FILE_3)
    main(".")
    std = capsys.readouterr()
    assert E.from_ref(ES[0]).ref in std.out
    assert not any(E.from_ref(i).ref in std.out for i in ES if i != ES[0])


def test_module_comma_separated_error_enables(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test enabling entire module with specific enable comment.

    Prior to `enable` add the `disable` directive.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(ENABLE_FILE_4)
    main(".")
    std = capsys.readouterr()
    included = ES[0], ES[1]
    assert all(E.from_ref(i).ref in std.out for i in included)
    assert not any(
        E.from_ref(i).ref in std.out for i in ES if i not in included
    )


def test_single_function_single_error_enable(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test enabling single function with specific enable comment.

    Prior to `enable` add the `disable` directive.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(ENABLE_FILE_5)
    main(".")
    std = capsys.readouterr()
    assert "function_1" in std.out
    assert not any(f"function_{i}" in std.out for i in range(2, 8))


def test_single_function_comma_separated_error_enable(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
) -> None:
    """Test enabling function with comment of several specific errors.

    Prior to `enable` add the `disable` directive.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    """
    init_file(ENABLE_FILE_6)
    main(".")
    std = capsys.readouterr()
    assert "function_6" in std.out
    assert not any(f"function_{i}" in std.out for i in range(1, 8) if i != 6)


@pytest.mark.parametrize("code,symbolic", SYMBOLIC)
def test_individual_inline_disable_checks(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    code: str,
    symbolic: str,
) -> None:
    """Test individual inline `disable` checks.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param code: Rule code to comment.
    :param symbolic: Rule symbolic code to comment.
    """
    enabled_rules = [i[0] for i in SYMBOLIC if i[0] != code]
    init_file(INLINE_DISABLE_TEMPLATE.format(rules=code))
    main(".")
    std = capsys.readouterr()
    assert E.from_ref(code).ref not in std.out
    assert all(E.from_ref(i).ref in std.out for i in enabled_rules)
    enabled_rules = [i[1] for i in SYMBOLIC if i[1] != symbolic]
    init_file(INLINE_DISABLE_TEMPLATE.format(rules=symbolic))
    main(".")
    std = capsys.readouterr()
    assert symbolic not in std.out
    assert all(E.from_ref(i).ref in std.out for i in enabled_rules)


@pytest.mark.parametrize(
    "rules",
    [
        f"{ES[0]},{ES[1]}",
        f"{ES[0]},{ES[1]},{ES[2]}",
        f"{ES[0]},{ES[1]},{ES[2]},{ES[3]}",
        f"{ES[0]},{ES[1]},{ES[2]},{ES[3]},{ES[4]}",
        f"{ES[0]},{ES[1]},{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[1]},{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[5]},{ES[6]}",
    ],
)
def test_comma_separated_inline_disable_checks(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    rules: str,
) -> None:
    """Test multiple inline `disable` checks.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param rules: Rules to comment.
    """
    all_rules = list(ES)
    comma_separated_rules = rules.split(",")
    enabled_rules = [i for i in all_rules if i not in comma_separated_rules]
    init_file(INLINE_DISABLE_TEMPLATE.format(rules=rules))
    main(".")
    std = capsys.readouterr()
    assert not any(E.from_ref(i).ref in std.out for i in comma_separated_rules)
    assert all(E.from_ref(i).ref in std.out for i in enabled_rules)


@pytest.mark.parametrize("code,symbolic", SYMBOLIC)
def test_individual_module_disable_checks(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    code: str,
    symbolic: str,
) -> None:
    """Test individual module `disable` checks.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param code: Rule code to comment.
    :param symbolic: Rule symbolic code to comment.
    """
    enabled_rules = [i[0] for i in SYMBOLIC if i[0] != code]
    init_file(MODULE_LEVEL_DISABLE_TEMPLATE.format(rules=code))
    main(".")
    std = capsys.readouterr()
    assert E.from_ref(code).ref not in std.out
    assert all(E.from_ref(i).ref in std.out for i in enabled_rules)
    enabled_rules = [i[1] for i in SYMBOLIC if i[1] != symbolic]
    init_file(MODULE_LEVEL_DISABLE_TEMPLATE.format(rules=symbolic))
    main(".")
    std = capsys.readouterr()
    assert code not in std.out
    assert all(i in std.out for i in enabled_rules)


@pytest.mark.parametrize(
    "rules",
    [
        f"{ES[0]},{ES[1]}",
        f"{ES[0]},{ES[1]},{ES[2]}",
        f"{ES[0]},{ES[1]},{ES[2]},{ES[3]}",
        f"{ES[0]},{ES[1]},{ES[2]},{ES[3]},{ES[4]}",
        f"{ES[0]},{ES[1]},{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[1]},{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[5]},{ES[6]}",
    ],
)
def test_comma_separated_module_disable_checks(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    rules: str,
) -> None:
    """Test multiple module `disable` checks.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param rules: Rules to comment.
    """
    all_rules = list(ES)
    comma_separated_rules = rules.split(",")
    enabled_rules = [i for i in all_rules if i not in comma_separated_rules]
    init_file(MODULE_LEVEL_DISABLE_TEMPLATE.format(rules=rules))
    main(".")
    std = capsys.readouterr()
    assert not any(E.from_ref(i).ref in std.out for i in comma_separated_rules)
    assert all(E.from_ref(i).ref in std.out for i in enabled_rules)


@pytest.mark.parametrize("code,symbolic", SYMBOLIC)
def test_individual_inline_enable_checks(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    code: str,
    symbolic: str,
) -> None:
    """Test individual inline enable checks.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param code: Rule code to comment.
    :param symbolic: Rule symbolic code to comment.
    """
    disabled_rules = [i[0] for i in SYMBOLIC if i[0] != code]
    init_file(INLINE_ENABLE_TEMPLATE.format(rules=code))
    main(".")
    std = capsys.readouterr()
    assert E.from_ref(code).ref in std.out
    assert not any(E.from_ref(i).ref in std.out for i in disabled_rules)
    disabled_rules = [i[1] for i in SYMBOLIC if i[1] != symbolic]
    init_file(INLINE_ENABLE_TEMPLATE.format(rules=symbolic))
    main(".")
    std = capsys.readouterr()
    assert symbolic in std.out
    assert not any(E.from_ref(i).ref in std.out for i in disabled_rules)


@pytest.mark.parametrize(
    "rules",
    [
        f"{ES[0]},{ES[1]}",
        f"{ES[0]},{ES[1]},{ES[2]}",
        f"{ES[0]},{ES[1]},{ES[2]},{ES[3]}",
        f"{ES[0]},{ES[1]},{ES[2]},{ES[3]},{ES[4]}",
        f"{ES[0]},{ES[1]},{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[1]},{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[5]},{ES[6]}",
    ],
)
def test_comma_separated_inline_enable_checks(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    rules: str,
) -> None:
    """Test multiple inline enable checks.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param rules: Rules to comment.
    """
    all_rules = list(ES)
    comma_separated_rules = rules.split(",")
    disabled_rules = [i for i in all_rules if i not in comma_separated_rules]
    init_file(INLINE_ENABLE_TEMPLATE.format(rules=rules))
    main(".")
    std = capsys.readouterr()
    assert all(E.from_ref(i).ref in std.out for i in comma_separated_rules)
    assert not any(E.from_ref(i).ref in std.out for i in disabled_rules)


@pytest.mark.parametrize("code,symbolic", SYMBOLIC)
def test_individual_module_enable_checks(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    code: str,
    symbolic: str,
) -> None:
    """Test individual module `enable` checks.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param code: Rule code to comment.
    :param symbolic: Rule symbolic code to comment.
    """
    disabled_rules = [i[0] for i in SYMBOLIC if i[0] != code]
    init_file(MODULE_LEVEL_ENABLE_TEMPLATE.format(rules=code))
    main(".")
    std = capsys.readouterr()
    assert E.from_ref(code).ref in std.out
    assert not any(E.from_ref(i).ref in std.out for i in disabled_rules)
    disabled_rules = [i[1] for i in SYMBOLIC if i[1] != symbolic]
    init_file(MODULE_LEVEL_ENABLE_TEMPLATE.format(rules=symbolic))
    main(".")
    std = capsys.readouterr()
    assert symbolic in std.out
    assert not any(E.from_ref(i).ref in std.out for i in disabled_rules)


@pytest.mark.parametrize(
    "rules",
    [
        f"{ES[0]},{ES[1]}",
        f"{ES[0]},{ES[1]},{ES[2]}",
        f"{ES[0]},{ES[1]},{ES[2]},{ES[3]}",
        f"{ES[0]},{ES[1]},{ES[2]},{ES[3]},{ES[4]}",
        f"{ES[0]},{ES[1]},{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[1]},{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[2]},{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[3]},{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[4]},{ES[5]},{ES[6]}",
        f"{ES[5]},{ES[6]}",
    ],
)
def test_comma_separated_module_enable_checks(
    capsys: pytest.CaptureFixture,
    init_file: FixtureInitFile,
    main: FixtureMain,
    rules: str,
) -> None:
    """Test multiple module enable checks.

    :param capsys: Capture sys out.
    :param init_file: Initialize a test file.
    :param main: Mock ``main`` function.
    :param rules: Rules to comment.
    """
    all_rules = list(ES)
    comma_separated_rules = rules.split(",")
    disabled_rules = [
        E.from_ref(i).ref for i in all_rules if i not in comma_separated_rules
    ]
    init_file(MODULE_LEVEL_ENABLE_TEMPLATE.format(rules=rules))
    main(".")
    std = capsys.readouterr()
    assert all(E.from_ref(i).ref in std.out for i in comma_separated_rules)
    assert not any(i in std.out for i in disabled_rules)
