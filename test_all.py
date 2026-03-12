import pytest
from HeatExchanger import HeatExchanger
from FlowMeter import FlowMeter


def test_heat_exchanger_creation():
    he = HeatExchanger("МойТеплообменник", 10.5, 100, 16, "вода")
    
    assert he.model == "МойТеплообменник"
    assert he.area == 10.5
    assert he.max_temp == 100
    assert he.max_pressure == 16
    assert he.medium == "вода"
    assert he.id == 1


def test_heat_exchanger_id_schetchik():
    he1 = HeatExchanger("A", 1, 100, 10, "вода")
    he2 = HeatExchanger("B", 2, 100, 10, "вода")
    he3 = HeatExchanger("C", 3, 100, 10, "вода")
    
    assert he1.id == 2
    assert he2.id == 3
    assert he3.id == 4


def test_heat_exchanger_calculate_water():
    he = HeatExchanger("Тест", 10, 100, 16, "вода")
    
    result = he.calculate_heat_flow(2, 30)
    
    assert result == 252000
    assert he.heat_flow == 252000
    assert he.delta_t == 30


def test_heat_exchanger_calculate_oil():
    he = HeatExchanger("Тест", 10, 100, 16, "масло")
    
    result = he.calculate_heat_flow(2, 30)
    
    assert result == 240000


def test_heat_exchanger_calculate_air():
    he = HeatExchanger("Тест", 10, 100, 16, "воздух")
    
    result = he.calculate_heat_flow(2, 30)
    
    assert result == 240000


def test_heat_exchanger_power_per_area():
    he = HeatExchanger("Тест", 10, 100, 16, "вода")
    he.calculate_heat_flow(2, 30)
    
    assert he.power_per_area == 25200


def test_heat_exchanger_power_per_area_zero():
    he = HeatExchanger("Тест", 10, 100, 16, "вода")
    
    assert he.power_per_area == 0.0


def test_heat_exchanger_max_power():
    he = HeatExchanger("Тест", 10, 100, 16, "вода")
    
    assert he.theoretical_max_power == 20000


def test_heat_exchanger_model_error():
    with pytest.raises(ValueError, match="Модель должна быть непустой строкой"):
        HeatExchanger("", 10, 100, 16, "вода")


def test_heat_exchanger_model_error_spaces():
    with pytest.raises(ValueError, match="Модель должна быть непустой строкой"):
        HeatExchanger("   ", 10, 100, 16, "вода")


def test_heat_exchanger_area_error_negative():
    with pytest.raises(ValueError, match="Площадь теплообмена должна быть положительным числом"):
        HeatExchanger("Тест", -5, 100, 16, "вода")


def test_heat_exchanger_area_error_zero():
    with pytest.raises(ValueError, match="Площадь теплообмена должна быть положительным числом"):
        HeatExchanger("Тест", 0, 100, 16, "вода")


def test_heat_exchanger_temp_error():
    with pytest.raises(ValueError, match="Максимальная температура должна быть положительным числом"):
        HeatExchanger("Тест", 10, -100, 16, "вода")


def test_heat_exchanger_pressure_error():
    with pytest.raises(ValueError, match="Максимальное давление должно быть положительным числом"):
        HeatExchanger("Тест", 10, 100, -16, "вода")


def test_heat_exchanger_medium_error():
    with pytest.raises(ValueError, match="Среда должна быть непустой строкой"):
        HeatExchanger("Тест", 10, 100, 16, "")


def test_heat_exchanger_equality():
    he1 = HeatExchanger("A", 1, 100, 10, "вода")
    he2 = HeatExchanger("B", 2, 100, 10, "вода")
    
    assert he1 != he2
    assert he1 != "строка"
    assert he2 != 123


def test_heat_exchanger_str():
    he = HeatExchanger("Тестовый", 15.5, 120, 20, "вода")
    text = str(he)
    
    assert "Тестовый" in text
    assert "15.5" in text
    assert "120" in text
    assert "20" in text
    assert "вода" in text


def test_heat_exchanger_repr():
    he = HeatExchanger("Тестовый", 15.5, 120, 20, "вода")
    text = repr(he)
    
    assert "HeatExchanger" in text
    assert "Тестовый" in text
    assert "15.5" in text



def test_flow_meter_creation():
    fm = FlowMeter("Расходомер-1", "ультразвуковой", 50, (0.5, 10), 0.02)
    
    assert fm.model == "Расходомер-1"
    assert fm.type == "ультразвуковой"
    assert fm.diameter == 50
    assert fm.flow_range == (0.5, 10)
    assert fm.error == 0.02
    assert fm.last_flow == 0.0


def test_flow_meter_get_flow():
    fm = FlowMeter("Тест", "механический", 25, (1, 5), 0.1)
    
    flow = fm.get_flow()
    
    assert 0.9 <= flow <= 5.5
    assert fm.last_flow == flow


def test_flow_meter_error_percent():
    fm = FlowMeter("Тест", "механический", 25, (1, 5), 0.15)
    
    assert fm.error_percent == 15.0


def test_flow_meter_flow_range_lmin():
    fm = FlowMeter("Тест", "механический", 25, (1, 5), 0.1)
    lmin_min, lmin_max = fm.flow_range_lmin
    
    assert lmin_min == 60
    assert lmin_max == 300


def test_flow_meter_max_error():
    fm = FlowMeter("Тест", "механический", 25, (1, 5), 0.1)
    fm.get_flow()
    
    assert fm.max_error == fm.last_flow * 0.1


def test_flow_meter_model_error():
    with pytest.raises(ValueError):
        FlowMeter("", "механический", 25, (1, 5), 0.1)


def test_flow_meter_type_error():
    with pytest.raises(ValueError):
        FlowMeter("Тест", "", 25, (1, 5), 0.1)


def test_flow_meter_diameter_error():
    with pytest.raises(ValueError):
        FlowMeter("Тест", "механический", -25, (1, 5), 0.1)


def test_flow_meter_range_error_min_max():
    with pytest.raises(ValueError):
        FlowMeter("Тест", "механический", 25, (10, 1), 0.1)


def test_flow_meter_range_error_negative():
    with pytest.raises(ValueError):
        FlowMeter("Тест", "механический", 25, (-1, 5), 0.1)


def test_flow_meter_error_range():
    with pytest.raises(ValueError):
        FlowMeter("Тест", "механический", 25, (1, 5), 1.5)


def test_flow_meter_error_negative():
    with pytest.raises(ValueError):
        FlowMeter("Тест", "механический", 25, (1, 5), -0.1)


def test_flow_meter_str():
    fm = FlowMeter("МойFM", "электромагнитный", 80, (2, 20), 0.05)
    text = str(fm)
    
    assert "МойFM" in text
    assert "электромагнитный" in text
    assert "80" in text
    assert "2" in text
    assert "20" in text
    assert "5.0%" in text or "5.0 %" in text


def test_flow_meter_repr():
    fm = FlowMeter("МойFM", "электромагнитный", 80, (2, 20), 0.05)
    text = repr(fm)
    
    assert "FlowMeter" in text
    assert "МойFM" in text
    assert "электромагнитный" in text



def test_heat_exchanger_with_flow_meter():
    he = HeatExchanger("Заводской", 20, 150, 25, "вода")
    fm = FlowMeter("ЗаводскойFM", "турбинный", 100, (5, 50), 0.03)
    
    flow = fm.get_flow()
    heat = he.calculate_heat_flow(flow, 40)
    
    assert 4 <= flow <= 52
    assert heat > 0
    assert he.heat_flow == heat
    assert fm.last_flow == flow
    assert he.power_per_area == heat / 20


def test_multiple_heat_exchangers():
    he1 = HeatExchanger("HE1", 10, 100, 10, "вода")
    he2 = HeatExchanger("HE2", 20, 150, 16, "масло")
    he3 = HeatExchanger("HE3", 30, 200, 25, "воздух")
    
    assert he1.id < he2.id < he3.id
    assert he1.model == "HE1"
    assert he2.medium == "масло"
    assert he3.max_pressure == 25


def test_multiple_flow_meters():
    fm1 = FlowMeter("FM1", "type1", 25, (0.1, 2), 0.01)
    fm2 = FlowMeter("FM2", "type2", 50, (1, 10), 0.02)
    fm3 = FlowMeter("FM3", "type3", 100, (5, 50), 0.05)
    
    assert fm1.id < fm2.id < fm3.id
    assert fm1.error == 0.01
    assert fm2.diameter == 50
    assert fm3.flow_range == (5, 50)