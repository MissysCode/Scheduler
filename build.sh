#!/usr/bin/env bash

set -euxo pipefail

# KEEP IN SYNC WITH THE ACTUAL RUN COMMAND  <---------------------------------+
rsync --dry-run --delete -av static prinsessa:/var/www/html/scheduler/ #      |
rsync --dry-run --exclude __pycache__ --exclude venv --exclude .git --delete -av . prinsessa:~/backend-scheduler-missyscode.com
#                                                                             |
# Then, confirm that user wants to actually run the rsync                     |
#                                                                             |
read -p "Do you want to run the actual rsync? (y/n): " confirm    #  +--------+
#                                                                 #  |
if [[ $confirm == "y" ]]; then                                    #  |
                                                                  #  |
    # KEEP IN SYNC WITH THE DRY RUN COMMAND  <-----------------------+
    rsync --delete -av static prinsessa:/var/www/html/scheduler/
    rsync --exclude venv --exclude .git --delete -av . prinsessa:~/backend-scheduler-missyscode.com

    echo "Rsync completed successfully."
else
    echo "Rsync aborted."
fi
