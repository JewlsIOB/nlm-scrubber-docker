# NLM Scrubber Wrappers

This package wraps the [NLM Scrubber](https://scrubber.nlm.nih.gov/) to make it easily accessible for a variety of programs.

This package includes three components-

1. A Docker container with NLM Scrubber already configured.
2. A `scrub.sh` script to make using the docker container easier.
3. A python library for dynamic deidentification.


## Docker

The docker image can be downloaded from [docker hub](https://hub.docker.com/r/radaisystems/nlm-scrubber) or built via `make build`.

Once run the container will deidentify anything in `/tmp/once_off/input` and output it to `/tmp/once_off/output` (these directories are *inside* the container). The input files can be limited by defining the `SCRUBBER_REGEX` environmental variables.

Mounting a local volume to `/tmp/once_off/input` and another to `/tmp/once_off/output` will allow you to deidentify and save items on your host machine.

You can mount a local volume to `/tmp/once_off/preserved.nci2.txt` or `/tmp/once_off/redacted.nci2.txt` to add addition terms to preserve or redact form the document.

You also can choose to define the environment variables `LDS_date`, `LDS_address`, or `LDS_age`. If you define them, these flags will be set in the config file, turning off the redaction of those elements.

Example call:

    docker run -it --rm --platform linux/amd64 -v  /tmp/nlp_input:/tmp/once_off/input -v /tmp/nlp_output:/tmp/once_off/output --env "KEEP_DATES=1" --env "KEEP_AGES=1" radaisystems/nlm-scrubber:latest

###FAQs
* The scrubber requires files to be ASCII encoded.  If nothing happens with a file, it could be in the wrong format.
* LDS_date: Dates in the format 2022-09-22 are considered to be alphanumeric instead of dates, so the only way to filter these out is to generate a list of all dates in this format in preserved.nci2.txt

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
