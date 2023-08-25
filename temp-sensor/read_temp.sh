#!/bin/bash
FNAME=${HOME}/raspisump/csv/`date +%Y-%m-%d`-temp.csv
${HOME}/sumpy/temp-sensor/ds18b20_read.py >> ${FNAME}
