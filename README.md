# Clinical Text De-identification

This package provides a docker wrapper to v.19 of the [National Library of Medicine HIPAA scrubber](https://scrubber.nlm.nih.gov/).
It allows you to remove in bulk identifying information from medical documentation in various text/csv formats.

The Docker image adds some additional functionality on top of the NLM Scrubber:

1. The NLM Scrubber currently does not work on Macs. The docker version adds the ability to run the NLM scrubber on a Mac.

2. It adds a pre-scrubbing step to convert files to ASCII text format, as v.19 of the NLM Scrubber is not compatible with UTF-8.

3. It expands upon the NLM Scrubber functionality to allow preservation of SQL-formatted dates (e.g. 2022-09-22).

## Requirements

1. Docker installation.  Download from https://www.docker.com/
2. About 1GB of hard drive space to download the Docker image from [docker hub](https://hub.docker.com/r/jewlsiob/nlm-scrubber)
3. Please ensure you adhere to your organization's specific HIPAA regulations.

## Running the Scrubber

### Details
1. Download the docker image from [docker hub](https://hub.docker.com/r/jewlsiob/nlm-scrubber)
2. Make a directory where docker can output the scrubbed data. You must *bind* this directory to the
   docker internal output directory. e.g.

       -v  /Users/jewlsiob/my_project/nlp_output:/tmp/once_off/output
3. You must *bind* the directory where your clinical text documents live to the internal docker directory. e.g.

       -v  /Users/jewlsiob/my_project/nlp_input:/tmp/once_off/input
4. You may specify the following environment variables when running the docker image:

   1. `--env "KEEP_DATES=1"`. Preserves dates in the files.

   2. `--env "KEEP_SQL_DATES=1"`. Preserves SQL-formatted dates in the files (e.g. 2022-09-22).

   3. `--env "KEEP_AGES=1"`. Preserves the age of patients over 89 years old.

   4. `--env "KEEP_ADDRESSES=1"`. Preserves city and state portion of addresses.

   5. `--env "SCRUBBER_REGEX=*.csv"`. Allows you to narrow down what file types are processed by the NLM scrubber.

   6. `--env "CONVERT_TO_ASCII=1"`. Tells docker to convert the files in the input directory from UTF-8 to ascii.

5. You may create a file with custom terms you wish to preserve when scrubbing the data.
   In order for docker to use this file,
   you must "mount the local volume" (i.e. this text file) to `/tmp/once_off/preserved.nci2.txt`. e.g.

       -v /Users/jewlsiob/my_project/preserved.txt:/tmp/once_off/preserved.nci2.txt
6. You may create a file with custom terms you wish to exclude when scrubbing the data.
   In order for docker to use this file,
   you must "mount the local volume" (i.e. this text file) to `/tmp/once_off/redacted.nci2.txt`. e.g.

       -v /Users/jewlsiob/my_project/my_redacted_v2.txt:/tmp/once_off/redacted.nci2.txt

### Examples

    docker run -it --rm --platform linux/amd64 -v /tmp/nlp_input:/tmp/once_off/input -v /tmp/nlp_output:/tmp/once_off/output --env "CONVERT_TO_ASCII=1" --env "KEEP_DATES=1" --env "KEEP_SQL_DATES=1" jewlsiob/nlm-scrubber:latest

-or-

    docker run -it --rm --platform linux/amd64 -v  /Users/jewlsiob/my_project/nlp_input:/tmp/once_off/input -v  /Users/jewlsiob/my_project/nlp_output:/tmp/once_off/output --env "SCRUBBER_REGEX=*.csv" jewlsiob/nlm-scrubber:latest

### Output

The NLM Scrubber outputs files with an additional suffix of *.LDS.* if the file preserved dates, older ages or addresses.
Otherwise, the suffix is *.nphi.*. Some additional processing information is added to the bottom of each file.

## Troubleshooting
1. *Missing files*. If you are getting no files in the output folder, there is likely an error in the format of the file.
     1. The scrubber requires files to be ASCII encoded. Use the `CONVERT_TO_ASCII=1` environment variable
        to convert files to ascii format.
     2. Sometimes saving in Excel or other processing leaves unreadable bytes (e.g. an extra 0x9d).
        If this occurs, try exporting the file to txt.
2. *Slowness*. This is complicated work! If you have a very large file, Docker can take 30+ minutes to run.
   Try running a smaller file first to ensure everything is working properly.
3. `KEEP_DATES`. Dates in the format 2022-09-22 are considered to be alphanumeric instead of dates, so add the KEEP_SQL_DATES flag to retain these.
4. `CONVERT_TO_ASCII`. If the ascii conversion isn't doing quite what you want, you can instead do this conversion locally.
   For ideas, take a look at the code we use for the conversion:
   [convert_to_ascii.py](https://github.com/JewlsIOB/nlm-scrubber-docker/tree/master/docker/addons/convert_to_ascii.py)
5. *Advanced*. You can attach to the terminal of an actively running docker instance to troubleshoot.
   If you have docker desktop, simply click on "containers" and the little terminal icon there.
   Running something like `cat /tmp/once_off/redacted.nci2.txt` will show you if your redacted file is properly mounted.
   You can also actively change a config file if you do it quickly while the NLM Scrubber is still loading.

## Editing the code

You can build the docker container locally via `make build`.
Please note that this command will not work on a Mac since the NLM Scrubber does not work on a Mac.

## Acknowledgements

1. Kayaalp, M., Sagan, P., Browne, A.C., McDonald, C.J. (2016). Guidelines for Annotating Personal Identifiers in the
   Clinical Text Repository of the National Institutes of Health (version 6/28/2016). Lister Hill National Center for
   Biomedical Communications, U.S. National Library of Medicine, National Institutes of Health, Bethesda, Maryland.
2. This package builds upon and extends upon the great work of
   [radaisystems/nlm-scrubber-docker](https://github.com/radaisystems/nlm-scrubber-docker)
