###############################################################################
###############################################################################
#                            Initialization Script                            #
#                             Author: Joshua Male                             #
#                              Date: 29/04/2026                               #
#    Description: Initializes the utilities package for SEM image analysis    #
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
import sys
import logging
import logging.config

from pathlib import Path
from datetime import datetime

# Date
date = datetime.now().date()

# Adjust path for functions
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Initialize logging software
log_path = Path(project_root, 'Logging').as_posix()
logging.config.fileConfig(
    fname=Path(log_path, 'logging.conf'),
    defaults={'logdir': log_path, 'log_date': date}
)
logger = logging.getLogger(name=Path(__file__).stem)

# Check logger working
logger.info('SEMUtils initialized successfully.')
