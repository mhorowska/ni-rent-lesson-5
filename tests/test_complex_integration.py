from src.manager import Manager
from src.models import Parameters

def test_get_apartment_costs():
    parameters = Parameters(
        apartments_json_path="data/apartments.json",
        tenants_json_path="data/tenants.json",
        transfers_json_path="data/transfers.json",
        bills_json_path="data/bills.json",
    )
    manager = Manager(parameters)
    assert manager.get_apartment_costs("apart-polanka", 2025, 1) == 910.0
    assert manager.get_apartment_costs("apart-polanka", 2025, 2) == 0.0
    assert manager.get_apartment_costs("nieistniejace-mieszkanie", 2025, 1) is None