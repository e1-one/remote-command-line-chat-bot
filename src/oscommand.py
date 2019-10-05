import logging
import os
import subprocess


def execute_command_as_subprocess(command):
    if os.sys.platform == 'win32':
        return execute_on_windows(command)
    else:
        raise Exception(f'Unsupported platform: {os.sys.platform}')


def check_dir(new_dir):
    try:
        os.chdir(new_dir)
        return True
    except FileNotFoundError:
        return False


def execute_on_windows(command):
    print(f'command received: {command}')
    process = subprocess.Popen([command[0], command[1:]], stdout=subprocess.PIPE, shell=True)
    (out, err) = process.communicate()
    logging.info("process output: " + str(out))
    print(str(out))
    if err:
        logging.error("process error: " + str(err))
        return str(err)
    return str(out)[2:][0:-1]  # deleting two characters from the beginning and one char from the end

