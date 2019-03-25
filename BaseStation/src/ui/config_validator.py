def is_number(x):
    try:
        return float(x) is not None
    except ValueError:
        return False


def is_positive(x):
    return is_number(x) and float(x) >= 0


def is_nonzero(x):
    return is_number(x) and float(x) != 0


def is_length(x, n):
    try:
        return len(x) == int(n)
    except ValueError:
        return False


class ConfigValidator:
    validators = {
        'is_positive': is_positive,
        'is_nonzero': is_nonzero,
        'is_number': is_number,
        'is_length': is_length
    }

    validations = {
        'target_altitude': 'is_positive,is_nonzero',
        'sampling_frequency': 'is_positive',
        'origin_measurement_delay': 'is_positive',
        'gui_fps': 'is_positive',
        'baudrate': 'is_positive',
        'timeout': 'is_positive',
        'start_character': 'is_length:1'
    }
    errors = {
        'is_positive': 'Doit être un nombre positif',
        'is_number': 'Doit être un nombre',
        'is_nonzero': 'Doit être un nombre non nul',
        'is_length': 'Doit être de longueur {}'
    }

    def is_valid(self, inputs):
        for name, value in inputs.items():
            for v in self.validations.get(name, '').split(','):
                parameters = v.split(':')
                try:
                    fun = self.validators[parameters[0]]
                except KeyError:
                    continue
                try:
                    parameters = parameters[1:]
                except IndexError:
                    parameters = []
                if not fun(value, *parameters):
                    return False
        return True

    def get_errors(self, inputs):
        errors = {}
        for name, value in inputs.items():
            for v in self.validations.get(name, '').split(','):
                parameters = v.split(':')
                try:
                    fun = self.validators[parameters[0]]
                except KeyError:
                    continue
                try:
                    parameters = parameters[1:]
                except IndexError:
                    parameters = []
                if not fun(value, *parameters):
                    errors[name] = self.errors[fun.__name__].format(*parameters)
        return errors
