#!/bin/bash
FNAME=${HOME}/raspi-sump/csv/`date +%Y-%m-%d`-temp.csv
${HOME}/sumpy/temp-sensor/ds18b20_read.py >> ${FNAME}
