'''
DESDMDashboard data collection utility database functions

'''

import subprocess


def shell_command(cmd):
    p = subprocess.Popen(cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.rsplit('\n'), err.rsplit('\n')


def du_dir_Mb(path):
    out, err = shell_command('du -s -m ' + path)
    if any(err):
        raise CommandLineError(err)
    return out[0].rsplit('\t')[0]


class CommandLineError(Exception):
    pass
