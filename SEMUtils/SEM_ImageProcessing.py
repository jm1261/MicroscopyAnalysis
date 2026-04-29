###############################################################################
###############################################################################
#                         SEM Image Processing Script                         #
#                             Author: Joshua Male                             #
#                              Date: 29/04/2026                               #
#                 Description: Functions to process SEM images                #
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

import logging
import GeneralUtils.FileIO as gio

from pathlib import Path

# Start logging
logger = logging.getLogger(name=Path(__file__).stem)


class SEMImageProcessor:
    """
    Class Details
    =============
    A class to process SEM image, including functions to correct for angle
    distortion, measure periods, and perform other image processing tasks.

    Methods
    -------
    __init__

    Attributes
    ----------
    root_path : pathlib.Path
        The root path for the image processing.

    ---------------------------------------------------------------------------
    Update History
    ==============

    29/04/2026
    ----------
    - Initial creation of the class.

    """

    def __init__(
            self,
            root_path: Path):
        """
        Function Details
        ----------------
        Initialize SEM Image Processor class.

        Parameters
        ----------
        root_path : pathlib.Path
            The root path for the image processing.

        Returns
        -------
        None

        -----------------------------------------------------------------------
        Update History
        ==============

        29/04/2026
        ----------
        - Initial creation of the function.

        """
        self.root_path = root_path


if __name__ == '__main__':
    root = Path(Path().absolute(), 'MicroscopyAnalysis').as_posix()
    logger.info(f'Current working directory: {root}')
    plot_dict = gio.load_json(
        file_path=Path(
            root,
            'plot_dictionary.json'
        )
    )
    logger.info(f'Loaded plot dictionary: {plot_dict}')
