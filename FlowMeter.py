import random

class FlowMeter:
    _id_counter = 0
    WATER_DENSITY = 1000

    def __init__(self, model, meter_type, diameter, flow_range, error):
        self.__class__._id_counter += 1
        self.__id = self.__class__._id_counter

        self.model = model
        self.type = meter_type
        self.diameter = diameter
        self.flow_range = flow_range
        self.error = error

        self.__last_flow = 0.0 

    @property
    def id(self):
        return self.__id

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Модель должна быть непустой строкой")
        self.__model = value.strip()

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Тип расходомера должен быть непустой строкой")
        self.__type = value.strip()

    @property
    def diameter(self):
        return self.__diameter

    @diameter.setter
    def diameter(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Диаметр должен быть положительным числом")
        self.__diameter = float(value)

    @property
    def flow_range(self):
        return self.__flow_range

    @flow_range.setter
    def flow_range(self, value):
        if not isinstance(value, (tuple, list)) or len(value) != 2:
            raise ValueError("Диапазон расхода должен быть кортежем/списком из двух чисел")
        min_f, max_f = value
        if not (isinstance(min_f, (int, float)) and isinstance(max_f, (int, float))):
            raise ValueError("Границы диапазона должны быть числами")
        if min_f >= max_f:
            raise ValueError("Минимальный расход должен быть меньше максимального")
        if min_f < 0:
            raise ValueError("Расход не может быть отрицательным")
        self.__flow_range = (float(min_f), float(max_f))

    @property
    def error(self):
        return self.__error

    @error.setter
    def error(self, value):
        if not isinstance(value, (int, float)) or not (0 <= value <= 1):
            raise ValueError("Погрешность должна быть числом от 0 до 1")
        self.__error = float(value)

    def get_flow(self):
        true_flow = random.uniform(self.flow_range[0], self.flow_range[1])
        error_factor = 1 + random.uniform(-self.error, self.error)
        measured_flow = true_flow * error_factor
        self.__last_flow = measured_flow
        return measured_flow

    @property
    def last_flow(self):
        return self.__last_flow

    @property
    def max_error(self):
        return self.last_flow * self.error

    @property
    def error_percent(self):
        return self.error * 100

    @property
    def flow_range_lmin(self):
        return (self.flow_range[0] * 60, self.flow_range[1] * 60)

    def __eq__(self, other):
        if not isinstance(other, FlowMeter):
            return False
        return self.id == other.id

    def __str__(self):
        return (f"FlowMeter(id={self.id}, model={self.model}, type={self.type}, "
                f"diameter={self.diameter} mm, range={self.flow_range} kg/s, "
                f"error={self.error*100:.1f}%)")

    def __repr__(self):
        return f"FlowMeter(model={self.model!r}, type={self.type!r})"