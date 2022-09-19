""" Constants """
from pathlib import Path

DEFAULT_TGT_CCSID = "*JOB"
DEFAULT_OBJLIB = "*CURLIB"
DEFAULT_CURLIB = "*CRTDFT"

BOB_PATH = Path(__file__).resolve().parent.parent

TARGET_GROUPS = ["TRG",
                    "DTA",
                    "SQL",
                    "BNDD",
                    "PF",
                    "LF",
                    "DSPF",
                    "PRTF",
                    "CMD",
                    "SQL",
                    "MODULE",
                    "SRVPGM",
                    "PGM",
                    "MENU",
                    "PNLGRP",
                    "QMQRY",
                    "WSCST",
                    "MSG"
                ]

FILE_TARGETGROUPS_MAPPING = {
    "PGM.SQLRPGLE": "PGM",
    "PGM.RPGLE": "PGM",
    "PGM.CLLE": "PGM",
    "PGM.C": "PGM",
    "CMDSRC": "CMD",
    "DSPF": "DSPF",
    "LF": "LF",
    "PF": "PF",
    "PRTF": "PRTF",
    "FILE": "PF",
    "MENUSRC": "MENU",
    "C": "MODULE",
    "RPGLE": "MODULE",
    "CLLE": "MODULE",
    "SQLC": "MODULE",
    "SQLRPGLE": "MODULE",
    "MODULE": "PGM",
    "CBL": "PGM",
    "CBLLE": "PGM",
    "RPG": "PGM",
    "ILEPGM": "PGM",
    "PNLGRPSRC": "PNLGRP",
    "SQL": "QMQRY",
    "BND": "SRVPGM",
    "ILESRVPGM": "SRVPGM",
    "BNDDIR": "BNDD",
    "DTA": "DTA",
    "DTAARA": "DTA",
    "SYSTRG": "TRG",
    "SQLPRC": "SQL",
    "TABLE": "SQL",
    "VIEW": "SQL",
    "SQLSEQ": "SQL",
    "SQLUDF": "SQL",
    "SQLTRG": "SQL",
    "MSGF": "MSG",
    "WSCSTSRC": "WSCST",
}

TARGET_TARGETGROUPS_MAPPING = {
    "CMD": "CMD",
    "FILE": "PF",
    "MENU": "MENU",
    "MODULE": "MODULE",
    "PGM": "PGM",
    "PNLGRP": "PNLGRP",
    "QMQRY": "QMQRY",
    "BNDD": "BNDD",
    "DTA": "DTA",
    "PGM": "PGM",
    "DTAARA": "SQL",
    "SRVPGM": "SRVPGM",
    "MSGF": "MSG",
    "WSCST": "WSCST",
    "TRG": "TRG",
}

FILE_TARGET_MAPPING = {
    "PGM.SQLRPGLE": "PGM",
    "PGM.RPGLE": "PGM",
    "PGM.CLLE": "PGM",
    "PGM.C": "PGM",
    "CMDSRC": "CMD",
    "DSPF": "FILE",
    "LF": "FILE",
    "PF": "FILE",
    "PRTF": "FILE",
    "MENUSRC": "MENU",
    "MENU": "MENU",
    "C": "MODULE",
    "RPGLE": "MODULE",
    "CLLE": "MODULE",
    "SQLC": "MODULE",
    "SQLRPGLE": "MODULE",
    "MODULE": "PGM",
    "CBL": "PGM",
    "CBLLE": "PGM",
    "RPG": "PGM",
    "ILEPGM": "PGM",
    "PNLGRPSRC": "PNLGRP",
    "PNLGRP": "PNLGRP",
    "SQL": "QMQRY",
    "BND": "SRVPGM",
    "ILESRVPGM": "SRVPGM",
    "BNDDIR": "BNDD",
    "DTAARA": "DTA",
    "SYSTRG": "PGM",
    "SQLPRC": "PGM",
    "TABLE": "FILE",
    "VIEW": "FILE",
    "SQLSEQ": "DTAARA",
    "SQLUDF": "SRVPGM",
    "SQLTRG": "PGM",
    "MSGF": "MSGF",
    "WSCSTSRC": "WSCST",
}
# This is the maximum number of dot seperated parts in the file extensions defined above.
FILE_MAX_EXT_LENGTH = max(
    map(lambda ext: len(ext.split('.')), FILE_TARGET_MAPPING.keys()))
