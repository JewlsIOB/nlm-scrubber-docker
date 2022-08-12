#!/usr/bin/env bash
# Options based on documentation: https://data.lhncbc.nlm.nih.gov/public/scrubber/files/user_manual/windows/user_manual_v.19.0411W.pdf

if [ -z ${SCRUBBER_REGEX+x} ]; then
  SCRUBBER_REGEX='.*'
fi
# If these variables are defined, turn on the appropriate flags
if [[ ! -z ${KEEP_DATES+z} ]]; then
  echo "LDS_date = display_all_dates" >> /tmp/once_off/config
fi
# TODO awaiting response from NLM on the correct syntax for addresses
if [[ ! -z ${KEEP_ADDRESSES+z} ]]; then
  echo "LDS_address = display_cities_and_towns" >> /tmp/once_off/config
fi
if [[ ! -z ${KEEP_AGES+z} ]]; then
  echo "LDS_age = display_all_ages" >> /tmp/once_off/config
fi

ROOT1="/tmp/once_off"
PRESERVED_FILE="${ROOT1}/preserved.nci2.txt"
REDACTED_FILE="${ROOT1}/redacted.nci2.txt"

# Basic options to run
echo "ROOT1 = ${ROOT1}" >> /tmp/once_off/config
echo "ClinicalReports_dir = ROOT1/input" >> /tmp/once_off/config
echo "ClinicalReports_files = ${SCRUBBER_REGEX}" >> /tmp/once_off/config
echo "nPHI_outdir = ROOT1/output" >> /tmp/once_off/config
echo "Preserved_phrases = ${PRESERVED_FILE}" >> /tmp/once_off/config
echo "Redacted_phrases = ${REDACTED_FILE}" >> /tmp/once_off/config

# Ensure preserved and redacted phrase files exist. It's fine if these files are empty
touch ${PRESERVED_FILE}
touch ${REDACTED_FILE}

# Ensure we know the options we are running with
echo "*****Config file:*********"
cat /tmp/once_off/config

if [ ! -f /opt/nlm_scrubber.exe ]; then
    /opt/nlm_scrubber /tmp/once_off/config
else
    wine /opt/nlm_scrubber.exe /tmp/once_off/config
fi
