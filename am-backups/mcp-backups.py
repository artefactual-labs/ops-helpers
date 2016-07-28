#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# assuming running on the default python3 provided in trusty (python 3.4)
# (python 3.5 introduces some improvements to the subprocess module
#  but unfortunately not able to use here yet)

import datetime
import logging
import os
import subprocess
import shlex
import sys

backup_root = "/srv/am-db-backups"


def main():

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

    try:
        # Create backup_root dir if it doesn't exist
        if not os.path.exists(backup_root):
            os.makedirs(backup_root)

        # get current date and time string and create a dir with it
        now = datetime.datetime.now()
        date_str = now.strftime("%Y%m%d-%H%M%S")
        backup_path = os.path.join(backup_root, date_str)
        if not os.path.exists(backup_path):
            os.makedirs(backup_path)

        logging.info("Creating backups in {}".format(backup_path))

        # dump MCP database
        command_string = "mysqldump MCP | gzip -c > {}/MCP.sql.gz".format(backup_path)
        #subprocess.check_call(shlex.split(command_string), shell=True)   # won't return stderr/out
        # do not use shlex.split() when using shell=True
        p = subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            logging.error("Error in command: {}".format(command_string))
            logging.error("returncode: {}".format(p.returncode))
            logging.error("stdout: {}".format(stdout))
            logging.error("stderr: {}".format(stderr))
            return -1

        # make dump of individual MCP tables
        command_string = "mysql -N -B -e 'show tables from MCP'"
        mcp_tables = subprocess.check_output(shlex.split(command_string))
        for table in mcp_tables.splitlines():
            table_str = table.decode("utf-8")
            command_string = "mysqldump MCP {0} | gzip -c > {1}/MCP-{0}.sql.gz".format(table_str, backup_path)
            p = subprocess.Popen(command_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = p.communicate()
            if p.returncode != 0:
                logging.error("Error in command: {}".format(command_string))
                logging.error("returncode: {}".format(p.returncode))
                logging.error("stdout: {}".format(stdout))
                logging.error("stderr: {}".format(stderr))
                return -1

    except subprocess.CalledProcessError as e:
        logging.error("Error in command: {}".format(e.cmd))
        logging.error("returncode: {}".format(e.returncode))
        #logging.error("stdout: {}".format(e.stdout)) # not supported until python 3.5 :-(
        #logging.error("stderr: {}".format(e.stderr)) # not supported until python 3.5 :-(
    except:
        logging.error("Unexpected error: {}".format(sys.exc_info()[0]))
        raise

if __name__ == '__main__':
    sys.exit(main())
