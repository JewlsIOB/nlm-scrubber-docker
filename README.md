# Overview

This package provides docker (and other) wrappers to the [National Library of Medicine HIPAA scrubber](https://scrubber.nlm.nih.gov/).
The NLM Scrubber currently does not work on Macs, so the docker version adds the ability to run the NLM scrubber on a Mac.

The Docker image has some additional benefits over the other components here:

1. It adds additional options to support v.19 of the NLM Scrubber.
   This includes allowing for preserving dates, ages over 89, (addresses coming soon), and specifying
   a preserved terms or redacted terms file.

2. It expands upon the NLM Scrubber functionality to allow preservation of SQL-formatted dates (e.g. 2022-09-22).

# NLM Scrubber Wrappers

This package includes three components-

1. A Docker container with NLM Scrubber already configured.
2. A `scrub.sh` script to make using the docker container easier.
3. A python library for dynamic deidentification.


## Docker

The docker image can be downloaded from [docker hub](https://hub.docker.com/r/jewlsiob/nlm-scrubber) or built via `make build`.

Once run the container will deidentify anything in `/tmp/once_off/input` and output it to `/tmp/once_off/output` (these directories are *inside* the container). The input files can be limited by defining the `SCRUBBER_REGEX` environmental variables.

Mounting a local volume to `/tmp/once_off/input` and another to `/tmp/once_off/output` will allow you to deidentify and save items on your host machine.

You can mount a local volume to `/tmp/once_off/preserved.nci2.txt` or `/tmp/once_off/redacted.nci2.txt` to add addition terms to preserve or redact form the document.

You also can choose to define the environment variables `KEEP_DATES`, `KEEP_ADDRESSES`, or `KEEP_AGES` (for ages over 89). If you define them, these flags will be set in the config file, turning off the redaction of those elements.

`KEEP_SQL_DATES` preserves sql-formatted dates as well -- e.g. 2022-09-22.

Example call:

    docker run -it --rm --platform linux/amd64 -v  /tmp/nlp_input:/tmp/once_off/input -v /tmp/nlp_output:/tmp/once_off/output --env "KEEP_DATES=1" --env "KEEP_AGES=1" jewlsiob/nlm-scrubber:latest

### FAQs
* The scrubber requires files to be ASCII encoded.  If nothing happens with a file, it could be in the wrong format.
* KEEP_DATES: Dates in the format 2022-09-22 are considered to be alphanumeric instead of dates, so add the KEEP_SQL_DATES flag to retain these.

## scrub.sh

This script wraps around the docker container, automatically mounting the supplied directories into the container so their contents can be deidentified.

To deidentify any json files from `testing/input` into the directory `testing/output` you'd run this command-

```
./scrub.sh testing/input/ testing/output/ .\*.json
```

Note that the NLM Scrubber does leave metadata at the bottom of each file- this would have to be removed before parsing the json.


## pyscrubber

This library does not use the docker container and depends on the nlm-scrubber being installed in `/opt/nlm_scrubber`.

To work with the `nlm_scrubber` application this library dynamically generates a config, writes all of the supplied strings to disk, and then reads the outputted data back before erasing all of the files it wrote.

There is a significant delay when the application is being loaded- as such it is far more efficient to batch data than to run it through individually.

## Credits

This package builds upon and extends upon the great work of [radaisystems/nlm-scrubber-docker](https://github.com/radaisystems/nlm-scrubber-docker)!