#  Copyright (c) 2022. Inspyre Softworks (https://softworks.inspyre.tech)

import logging
import pathlib
from argparse import ArgumentParser
from threading import Thread
from time import sleep

from csv_logger import CsvLogger
from matplotlib import pyplot as plt

arguments = None

filename = 'logs/log.csv'
delimiter = ','
level = logging.INFO
custom_additional_levels = [
    'CPUTemperature',
    'Event'
]

fmt = f'%(asctime)s{delimiter}%(levelname)s{delimiter}%(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
max_size = 2097152
max_files = 5
header = ['date', 'level', 'time', 'temp']

csvlogger = CsvLogger(filename=filename,
                      delimiter=delimiter,
                      level=level,
                      add_level_names=custom_additional_levels,
                      add_level_nums=None,
                      fmt=fmt,
                      datefmt=datefmt,
                      max_size=max_size,
                      max_files=max_files,
                      header=header)

monitoring = False


def to_fahrenheit(celsius):
    """
    Convert celsius to fahrenheit.

    Args:
        celsius (float):
            The temperature in celsius.

    Returns:
        The temperature in fahrenheit.

    """
    return celsius * 9 / 5 + 32


def get_CPU_temp(fahrenheit=False):
    """
    Get the CPU temperature.

    Args:
        fahrenheit (bool):
            Whether to return the temperature in fahrenheit.

    Returns:
        The temperature in celsius or fahrenheit.

    """
    cpu_temp = pathlib.Path('/sys/class/thermal/thermal_zone0/temp').read_text()

    if fahrenheit:
        return to_fahrenheit(float(cpu_temp))
    return to_fahrenheit(float(cpu_temp)) / 1000


def monitor(interval=3, fahrenheit=False):
    """
    Monitor the CPU temperature.

    Args:
        interval (int):
            The interval in seconds to monitor the temperature.

        fahrenheit (bool):
            Whether to monitor the temperature in fahrenheit.

    """

    global monitoring
    monitoring = True

    csvlogger.Event('Monitoring CPU temperature.')
    while monitoring:
        csvlogger.CPUTemperature(get_CPU_temp(fahrenheit=fahrenheit))

        sleep(interval)

    csvlogger.Event('Stopped monitoring CPU temperature.')


class Arguments(object):
    def __init__(self):
        self.parser = ArgumentParser(
            prog='CPUTempMonitor',
            description='Monitor the CPU temperature.',
        )

        self.parser.add_argument(
            '-i',
            '--interval',
            type=int,
            required=False,
            action='store',
            help='The interval in seconds to monitor the temperature.',
            default=3
        )

        self.parser.add_argument(
            '-f',
            '--fahrenheit',
            action='store_true',
            help='Whether to monitor the temperature in fahrenheit.',
            default=False
        )

        self.parser.add_argument(
            '--filesize',
            type=int,
            required=False,
            action='store',
            help='The maximum size of the log file in bytes.',
            default=2097152
        )

        self.parser.add_argument(
            '--files',
            type=int,
            required=False,
            action='store',
            help='The maximum number of log files to keep.',
            default=5
        )

        self.parser.add_argument(
            '--logfile',
            type=str,
            required=False,
            action='store',
            help='The log file to write to.',
            default='logs/log.csv'
        )

    def parse(self):
        return self.parser.parse_args()


if __name__ == '__main__':
    arguments = Arguments()
    args = arguments.parse()

    monitoring = True
    monitor_thread = Thread(target=monitor, args=[args.interval], daemon=True)
    monitor_thread.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        csvlogger.Event('Received KeyboardInterrupt.')
        csvlogger.error('Received KeyboardInterrupt. Stopping.')
        monitoring = False

    csvlogger.Event('Stopping monitoring.')
    print('\nDone.')
    all_logs = csvlogger.get_logs(evaluate=False)
    for log in all_logs:
        print(log)

    plt.plot(all_logs['time'], all_logs['temp'])
    plt.show()
    plt.close()
