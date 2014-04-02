'''
DESDMDASHBOARD

'''

import subprocess

class ShellCommand(object):

    def __init__(self, command):
        self.command = command
        self.output = None

    def execute_command(self):
        if type(self.command) == list:
            self.output = subprocess.check_output(self.command)
        elif type(self.command) == str:
            args = self.command.rsplit(' ')
            self.output = subprocess.check_output(args)
        raise ShellCommandError('Command cannot be executed.')

    def return_list_of_dicts(self, first_line_is_header=True):
        lines = self.output.rsplit('\n')
        header = lines[0].rsplit(' ')
        output = [ {header[]} ]


class ShellCommandError(Exception):
    pass
