"""

File:
    is_temper/temps.py
    
Project:
    is-temper
    
Created:
    8/24/22 - 17:43 hrs
    
Author:
    Taylor-Jayde Blackstone <t.blackstone@inspyre.tech>
    
Description:
    Contains code related to the gathering of CPU temperatures.
    
"""

#  Copyright (c) 2022. Inspyre Softworks (https://softworks.inspyre.tech)

import datetime as dt

import matplotlib.pyplot as plt
from inspyre_toolbox.humanize import Numerical
# import matplotlib.animation as animation
from psutil import sensors_temperatures

VALID_UNITS = [
    'c',
    'celsius',
    'f',
    'fahrenheit',
    'k',
    'kelvin'
]


def get_temps():
    """
    The get_temps function returns a list of named tuples, each containing the
    name and current temperature (in degrees Celsius) for each CPU on the system.

    Returns:
        :class:`dict`:
            The temperatures for all cores

    """
    return sensors_temperatures()['coretemp']


def get_timestamp():
    """
    The get_timestamp function returns the current time in a string format that is useful for
    creating timed plots. The function returns the current time as a string in the format:
    "HH:MM:SS.SSSSS"

    Returns:
        :class:`str`:
            The current time in the format: "HH:MM:SS.SSSSS"

    """
    return str(dt.datetime.now().time())


def celsius_to_fahrenheit(celsius):
    """
    Convert a temperature from celsius

    Arguments:
        celsius (float):
            The temperature in degrees Celsius

    Returns:
        :class:`float`:
            The temperature in degrees Fahrenheit

    """
    return round(float((celsius * 9 / 5) + 32), 2)


def celsius_to_kelvin(celsius):
    """
    Convert a temperature from celsius to kelvin.

    Arguments:
        celsius (float):
            The temperature in degrees Celsius

    Returns:
        :class:`float`:
            The temperature in degrees Kelvin
    """
    return round(float(celsius + 273.15), 2)


def get_core_number():
    """
    The get_core_number function returns the number of cores on a machine.

    Returns:
        :class:`int`:
            The number of cores on the machine.

    """
    sensor_data = get_temps()
    return len(sensor_data) - 1


def check_unit(unit):
    """
    The check_unit function checks that the value for 'unit' is one of:
        * 'c', or 'celsius' to get temperature readings in celsius.
        * 'f' or 'fahrenheit' to get temperature readings in fahrenheit.
        * 'k' or 'kelvin' to get temperature readings in kelvin.


    Args:
        unit: Check that the unit is one of the valid units

    Returns:
        :class:`bool`:
            A boolean value indicating whether the provided unit is a valid one.

    Raises:
        ValueError:
            If the unit is not one of the valid units.

    """
    if unit.lower() not in VALID_UNITS:
        raise ValueError(f"The value for 'unit' must be one of: {', '.join(VALID_UNITS)}")

    return True


class CPU(object):
    valid_units = VALID_UNITS

    def __init__(self, unit: str = 'c', use_numerical=False):
        """
        The __init__ function initializes the class. It is called automatically when an instance of the class is
        created.

        Args:
            self:
                Reference the object itself

            unit (optional, string, default='c'):
                Set the unit of temperature to either celsius or fahrenheit

            use_numerical=False:
                Display the core name instead of the numerical value

        Returns:
            :class:`CPU`:
                The object itself

        """
        if check_unit(unit):
            self.temperatures = sensors_temperatures()['coretemp']

        self.__unit = unit

        if isinstance(use_numerical, bool):
            self.__use_numerical = use_numerical
        else:
            raise ValueError(
                'Argument "use_numerical" expected a value of type "bool" but received an argument of type '
                f'{type(use_numerical)}')

        self.__cores = []

    @property
    def number_of_cores(self, as_integer=False):
        """
        The number_of_cores function returns the number of CPU cores on a computer.

        If you do not pass 'True' to the 'as_integer' argument you will get a string in the
        following format: '<NUM> CPU cores'

        Args:
            as_integer (optional, boolean, default=False):
                Return the number of cores as an integer instead of a string.

        Returns:
            The number of cpu cores on the machine

        """
        core_number = get_core_number()

        return core_number if as_integer else Numerical(core_number, noun='CPU core').count_noun()

    @property
    def cores(self):
        """
        The cores function returns the number of cores in a computer.
           It takes no arguments.

        Args:
            self: Refer to the object itself

        Returns:
            The number of cores the computer has

        """
        return self.__cores

    @property
    def unit(self):
        """
        Returns the unit of measurement as provided at initialization time.

        Returns:
            :class:`string`:
                The unit of measurement
        """
        return self.__unit

    @unit.setter
    def unit(self, new_unit):
        """
        The unit function sets the unit of measure for a given object.

        The function takes one argument, which is the new unit to be set.

        If the new unit is not valid (i.e., it isn't in our list of acceptable units),
        the function will raise an error.

        Args:
            self:
                Refer to the object itself

            new_unit (string):
                Set the new unit for the object
        """
        nu = new_unit.lower()

        if check_unit(nu):
            self.__unit = nu.lower()

    @unit.deleter
    def unit(self):
        """
        The unit function sets the unit to Celsius when `del` is invoked on it.

        Args:
            self:
                Represent the instance of the object itself
        """
        self.__unit = 'c'

    @property
    def overall_temp(self):
        """
        The overall_temp function returns the current temperature of the CPU (as a whole) in celsius, fahrenheit,
        or kelvin.

        The function accepts a single argument: :param:`unit` (:obj:`string`), which is either 'c', 'celsius', 'k',
        'kelvin', 'f', or 'fahrenheit' (defaults to celsius (or 'c') if no :param:`unit` is provided).  The function
        returns a :class:`float` value.

        Args:
            self:
                Access variables that belong to the class

        Returns:
            :class:`float`:
                The temperature in the unit that was passed to it
        """
        temp = sensors_temperatures()['coretemp'][0].current
        switch = {
            'c': temp,
            'celsius': temp,
            'f': celsius_to_fahrenheit(temp),
            'fahrenheit': celsius_to_fahrenheit(temp),
            'k': celsius_to_kelvin(temp),
            'kelvin': celsius_to_kelvin(temp)
        }
        return switch.get(self.unit, 'Invalid temperature unit provided')

    def build_cores(self):
        """
        The build_cores function is a helper function that builds the list of cores for :class:`CPU`.

        :func:`build_cores` is called by :func:`__init__` and returns a list of :class:`CPU.Core` objects that are used
        to track each core's state. :func:`build_cores`  is only called once per :obj:`CPU` object, so it does not need
        to be efficient.

        Args:
            self:
                Reference the class itself.

        Returns:
            :class:`list`:
                List of :class:`CPU.Core` objects that are used to track each core's state.

        """
        if not self.__cores:

            for i in range(get_core_number()):
                self.__cores.append(self.Core(self.unit, i + 1))

        return self.__cores

    class Core(object):
        """
        The Core object is used to track the state of a single core.
        """

        def __init__(self, unit, core_number):
            """
            The __init__ function is called when an instance of the class is created.

            It initializes the attributes of the class and can be used to set up variables that are needed by all
            instances.

            Args:
                self:
                    Refer to the instance of the class

                unit (string):
                    The temperature unit you'd like your readings back in.

                core_number (int):
                    Set the number of cores that are used to run the program

            Returns:
                :class:`CPU.Core`:
                    Instance of the class.

            """
            if check_unit(unit):
                self.__unit = unit

            if core_number <= 0 or core_number >= (get_core_number() + 1):
                raise ValueError(f"The 'core_number' argument can not exceed {get_core_number()} and can't be below 0!")
            else:
                self.__core_number = core_number

            self.__history = {}

        @property
        def history(self):
            """

            Get the history of the temperature readings for this core.

            Returns:
                :class:`dict`:
                    A dictionary containing the history of the temperature readings for this core.

            """
            return self.__history

        @property
        def temperature(self):
            """
            The temperature function returns the current temperature of a given core.

            Args:
                self:
                    Refer to the object itself

            Returns:
                :class:`float`:
                    The current temperature of the core in the unit specified by the user

            """
            temp = get_temps()[self.__core_number].current

            switch = {
                'c': temp,
                'celsius': temp,
                'f': celsius_to_fahrenheit(temp),
                'fahrenheit': celsius_to_fahrenheit(temp),
                'k': celsius_to_kelvin(temp),
                'kelvin': celsius_to_kelvin(temp)
            }

            return switch.get(self.__unit, 'Invalid temperature unit provided!')

        def __repr__(self):
            return f'Core {self.__core_number}: {self.temperature}'


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []

#
# # This function is called periodically from FuncAnimation
# def animate(i, xs, ys):
#     # Read temperature (Celsius) from TMP102
#     temp_c = round(tmp102.read_temp(), 2)
#
#     # Add x and y to lists
#     xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
#     ys.append(temp_c)
#
#     # Limit x and y lists to 20 items
#     xs = xs[-20:]
#     ys = ys[-20:]
#
#     # Draw x and y lists
#     ax.clear()
#     ax.plot(xs, ys)
#
#     # Format plot
#     plt.xticks(rotation=45, ha='right')
#     plt.subplots_adjust(bottom=0.30)
#     plt.title('TMP102 Temperature over Time')
#     plt.ylabel('Temperature (deg C)')

# Set up plot to call animate() function periodically
# ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
# plt.show()
