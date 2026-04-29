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
import InitializeSEMUtils  # noqa

import json
import logging
import numpy as np

from PIL import Image
from pathlib import Path

# Start logging
logger = logging.getLogger(name=Path(__file__).stem)


def remove_unwanted(all_lines: list,
                    unwanted_character: str) -> list:
    """
    Function Details
    ================
    Remove unwanted characters from lines, removes hidden newline characters.

    Parameters
    ----------
    all_lines : list
        A list of lines read from the SEM log file.
    unwanted_character : str
        The character to be removed from the lines.

    Returns
    -------
    list
        A list of lines with the unwanted characters and newline characters
        removed.

    ---------------------------------------------------------------------------
    Update History
    ==============

    29/04/2026
    ----------
    - Initial creation of the function.

    """
    lines = [
        (
            line.translate(
                {ord(unwanted_character): None}
            )
        )[0: -1]
        for line in all_lines
    ]
    logger.info(f'Removed unwanted character {unwanted_character} from lines.')
    return lines


def lines_to_parameters(lines: list) -> dict:
    """
    Function Details
    ================
    Pull important parameters into a dictionary.

    Parameters
    ----------
    lines: list
        Array of lines from txt file, stripped of '$' and \n characters.

    Returns
    -------
    parameters: dict
        A dictionary containing the parameter labels as keys and their
        corresponding values as lists.

    ---------------------------------------------------------------------------
    Update History
    ==============

    29/04/2026
    ----------
    - Initial creation of the function.

    """
    parameters = dict()
    for line in lines:
        parameter_label, *parameter_values = line.strip().split(' ')
        parameters[parameter_label] = parameter_values
    logger.info(
        f'Converted lines to parameters dictionary with {len(parameters)} '
        f'entries.'
    )
    return parameters


def desired_JEOL_parameters(all_parameters: dict,
                            pull_text: bool=False) -> dict:
    """
    Function Details
    ================
    Pull important parameters into a dictionary. Add more parameters by adding
    names and keys to the dictionary in this function.

    Parameters
    ----------
    all_parameters: dict
        A dictionary of all parameters from the txt file.
    pull_text: bool, optional
        Whether to include the on-image text parameters in the output
        dictionary. Default is False.

    Returns
    -------
    desired_parameters: dict
        Dictionary of all desired parameters from the txt file.

    ---------------------------------------------------------------------------
    Update History
    ==============

    29/04/2026
    ----------
    - Initial creation of the function.

    """
    desired_parameters = {
        'acceleration_voltage': float(all_parameters['CM_ACCEL_VOLT'][0]),
        'emission_current': float(all_parameters['SM_EMI_CURRENT'][0]),
        'brightness': int(all_parameters['CM_BRIGHTNESS'][0]),
        'contrast': int(all_parameters['CM_CONTRAST'][0]),
        'magnification': int(all_parameters['CM_MAG'][0]),
        'working_distance': float(all_parameters['SM_WD'][0]),
        'calibration_pixels': int(all_parameters['SM_MICRON_BAR'][0]),
        'stage_position_x': float(all_parameters['CM_STAGE_POS'][0]),
        'stage_position_y': float(all_parameters['CM_STAGE_POS'][1]),
        'stage_position_z': float(all_parameters['CM_STAGE_POS'][2]),
        'stage_position_r': float(all_parameters['CM_STAGE_POS'][3]),
        'stage_position_t': float(all_parameters['CM_STAGE_POS'][4]),
        'working_distance_correct': int(all_parameters['SM_WD_CORRECT'][0]),
        'scan_rotation': float(all_parameters['SM_SCAN_ROTATION'][0])}

    units_suffix = 2
    calibration_distance = all_parameters['SM_MICRON_MARKER'][0]
    desired_parameters['calibration_distance'] = int(
        calibration_distance[: -units_suffix])
    desired_parameters['distance_unit'] = calibration_distance[-units_suffix:]

    width, height = (0, 1)
    desired_parameters['image_width'] = int(
        all_parameters['CM_FULL_SIZE'][width])
    desired_parameters['image_height'] = int(
        all_parameters['CM_FULL_SIZE'][height])

    if pull_text:
        for key, value in all_parameters.items():
            if key.startswith('AN_TEXT%'):
                try:
                    measurement_string = value[4].strip('"')
                    if any(
                        unit in measurement_string for unit in [
                            'nm', 'µm', 'um'
                        ]
                    ):
                        desired_parameters[
                            f'text_label_{key.split("%")[-1]}'
                        ] = measurement_string
                        logger.info(
                            f'Extracted text parameter {key}: '
                            f'{measurement_string}'
                        )
                except (IndexError, TypeError):
                    logger.warning(
                        f'Could not extract text from parameter: {key}'
                    )

    logger.info(f'Extracted desired parameters: {desired_parameters}')
    return desired_parameters


def read_SEM_log(file_path: Path) -> dict:
    """
    Function Details
    ================
    Load JEOL-SEM txt file as a dictionary of key parameters.

    Parameters
    ----------
    file_path : Path
        The path to the SEM log file.

    Returns
    -------
    parameters: dict
        A dictionary containing the desired parameters extracted from the SEM
        log file.

    ---------------------------------------------------------------------------
    Update History
    ==============

    29/04/2026
    ----------
    - Initial creation of the function.

    """
    with open(file_path) as infile:
        all_lines = infile.readlines()
        logger.info(f"Read {len(all_lines)} lines from {file_path.name}")
    stripped_lines = remove_unwanted(
        all_lines=all_lines,
        unwanted_character='$'
    )
    JEOL_parameters = lines_to_parameters(lines=stripped_lines)
    parameters = desired_JEOL_parameters(
        all_parameters=JEOL_parameters,
        pull_text=True
    )
    return parameters


if __name__ == "__main__":
    storage_path = Path('K://Josh/SEM/ARGUS/EtchStability')
    target_file = 'AI18a_260415_001.txt'
    file_path = Path(storage_path, target_file)
    parameters = read_SEM_log(file_path)
    logger.info(f"Extracted parameters from {target_file}: {parameters}")
