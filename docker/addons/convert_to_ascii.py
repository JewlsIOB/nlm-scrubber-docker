import glob
import os
import sys

def convert_to_ascii(source_dir, temp_dir, intermediate_dir, ext=".txt"):
    """Converts files from UTF-8 to ASCII format so as to support the NLM Scrubber (https://lhncbc.nlm.nih.gov/scrubber/)

    Args:
        source_dir (string): source directory where your files with HIPAA data exist
        temp_dir (string): temporary directory where you want your files that were find/replaced placed
        intermediate_dir (string): intermediate directory where you want your ascii converted files placed

        ext (string): extension of the files you are working with. Defaults to ".txt". (Needs to be some text format).
    """

    docs = {}
    for file_path in glob.glob(source_dir + "*" + ext):
        file_name = os.path.basename(file_path)

        # 1. Read whole file to a string and write replaced syntax
        temp_file_path = temp_dir + file_name
        temp_file = open(temp_file_path, 'w')
        with open(file_path, 'r') as file :
            filedata = file.read()

            #
            # Preserve certain utf-8 characters
            #
            # Temperatures
            filedata = filedata.replace('°C', 'C')
            filedata = filedata.replace('°F', 'F')
            filedata = filedata.replace('° C', 'C')
            filedata = filedata.replace('° F', 'F')
            filedata = filedata.replace('øC', 'C')
            filedata = filedata.replace('øF', 'F')
            filedata = filedata.replace(' °', ' deg. ')
            filedata = filedata.replace(' °', ' deg. ')
            filedata = filedata.replace('°', ' deg. ')
            # Other common medical terms that aren't in ascii
            filedata = filedata.replace('µ', 'm')
            filedata = filedata.replace('²', '^2')

            temp_file.write(filedata)

        # close out temp file
        temp_file.close()

        # 2. Convert the file to ascii from utf-8.
        # Based on https://stackabuse.com/convert-bytes-to-string-in-python/
        intermediate_file_path = intermediate_dir + file_name
        intermediate_file = open(intermediate_file_path, 'wb')
        with open(temp_file_path, "rb+") as file:
            existing = file.read()
            intermediate_file.write(existing.decode('UTF-8').encode('ascii', 'ignore'))
        intermediate_file.close()

        # No need to keep extra files around
        os.remove(temp_file_path)

# Run this function with Dockerfile defaults
convert_to_ascii("/tmp/once_off/input/", "/tmp/once_off/temp/", "/tmp/once_off/intermediate/", sys.argv[1])
