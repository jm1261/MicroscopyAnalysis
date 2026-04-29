###############################################################################
###############################################################################
#                               File I/O Script                               #
#                             Author: Joshua Male                             #
#                              Date: 29/04/2026                               #
#           Description: File I/O operations for SEM image analysis           #
#                         Project: Microscopy Analysis                        #
#                                                                             #
#                        Script designed for Python 3                         #
#                           © Copyright Joshua Male                           #
#                                                                             #
#                            Software Release: 1.0                            #
#                            License: MIT License                             #
###############################################################################
###############################################################################

# Imports
#  import InitializeGeneralUtils  # noqa

import os
import json
import logging

from pathlib import Path

# Set up logging
logger = logging.getLogger(name=Path(__file__).stem)


def load_json(file_path: os.PathLike) -> dict:
    """
    Function Details
    ================
    Loads .json file types.

    Use json python library to load a .json file.

    Parameters
    ----------
    file_path : string
        Path to file.

    Returns
    -------
    json file : dictionary
        .json dictionary file.

    Notes
    -----
    json files are typically dictionaries, as such the function is intended for
    use with dictionaries stored in .json file types.

    ---------------------------------------------------------------------------
    Update History
    ==============

    06/08/2024
    ----------
    Copied from previous work, documentation updated. JM.

    """
    with open(file_path, 'r') as file:
        return json.load(file)


def convert(o):
    """
    Function Details
    ================
    Check data type.

    Check type of data string.

    Parameters
    ----------
    o : string
        String to check.

    Returns
    -------
    TypeError : Boolean
        TypeError if string is not suitable.

    ---------------------------------------------------------------------------
    Update History
    ==============

    06/08/2024
    ----------
    Copied from previous work, documentation updated. JM.

    """
    if isinstance(o, np.generic):
        return o.item()
    raise TypeError(f'Cannot serialize object of {type(o)}')


def save_json_dicts(out_path: os.PathLike,
                    dictionary: dict) -> None:
    """
    Function Details
    ================
    Save .json file types.

    Use json python library to save a dictionary to a .json file.

    Parameters
    ----------
    out_path : string
        Path to file.
    dictionary : dictionary
        Dictionary to save.

    Returns
    -------
    None

    Notes
    -----
    json files are typically dictionaries, as such the function is intended for
    use with dictionaries stored in .json file types.

    ---------------------------------------------------------------------------
    Update History
    ==============

    06/08/2024
    ----------
    Copied from previous work, documentation updated. JM.

    """
    with open(out_path, 'w') as outfile:
        json.dump(
            dictionary,
            outfile,
            indent=2,
            default=convert)
        outfile.write('\n')
