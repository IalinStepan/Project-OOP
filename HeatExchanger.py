class HeatExchanger:
    # Удельная теплоёмкость воды
    SPECIFIC_HEAT_WATER = 4200
    # Счётчик для уникальных идентификаторов
    _id_counter = 0

    def __init__(self, model, area, max_temp, max_pressure, medium):
        self.__class__._id_counter += 1
        self.__id = self.__class__._id_counter

        self.model = model
        self.area = area
        self.max_temp = max_temp
        self.max_pressure = max_pressure
        self.medium = medium

        self.__last_heat_flow = 0.0
        self.__last_delta_t = 0.0

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
    def area(self):
        return self.__area

    @area.setter
    def area(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Площадь теплообмена должна быть положительным числом")
        self.__area = float(value)

    @property
    def max_temp(self):
        return self.__max_temp

    @max_temp.setter
    def max_temp(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Максимальная температура должна быть положительным числом")
        self.__max_temp = float(value)

    @property
    def max_pressure(self):
        return self.__max_pressure

    @max_pressure.setter
    def max_pressure(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Максимальное давление должно быть положительным числом")
        self.__max_pressure = float(value)

    @property
    def medium(self):
        return self.__medium

    @medium.setter
    def medium(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Среда должна быть непустой строкой")
        self.__medium = value.strip().lower()

    def calculate_heat_flow(self, flow_rate, delta_t):
        """Рассчитывает тепловой поток и запоминает последние параметры."""
        if self.medium == "вода":
            cp = self.SPECIFIC_HEAT_WATER
        else:
            cp = 4000

        heat_flow = flow_rate * cp * delta_t
        self.__last_heat_flow = heat_flow
        self.__last_delta_t = delta_t
        return heat_flow

    @property
    def heat_flow(self):
        return self.__last_heat_flow

    @property
    def delta_t(self):
        return self.__last_delta_t

    @property
    def power_per_area(self):
        if self.area > 0 and self.heat_flow > 0:
            return self.heat_flow / self.area
        return 0.0

    @property
    def theoretical_max_power(self):
        return self.area * 2000

    def __eq__(self, other):
        if not isinstance(other, HeatExchanger):
            return False
        return self.id == other.id

    def __str__(self):
        return (f"HeatExchanger(id={self.id}, model={self.model}, area={self.area} m², "
                f"max_temp={self.max_temp}°C, max_pressure={self.max_pressure} bar, "
                f"medium={self.medium})")

    def __repr__(self):
        return f"HeatExchanger(model={self.model!r}, area={self.area})"