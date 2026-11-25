from src.manager import Manager
from src.models import Parameters
from src.models import Bill
from src.models import ApartmentSettlement
import pytest

def test_apartment_costs_invalid_month():
    manager = Manager(Parameters())
    with pytest.raises(ValueError):
        manager.get_apartment_costs("apart-polanka", 2025, 13)
    with pytest.raises(ValueError):
        manager.get_apartment_costs("apart-polanka", 2025, 0)

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

def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0
    
    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 3532.0



def test_create_apartment_settlement():
    manager = Manager(Parameters())

    settlement_jan = manager.create_apartment_settlement("apart-polanka", 2025, 1)
    assert settlement_jan is not None
    assert isinstance(settlement_jan, ApartmentSettlement)
    assert settlement_jan.apartment == "apart-polanka"
    assert settlement_jan.year == 2025
    assert settlement_jan.month == 1
    assert settlement_jan.total_rent_pln == 0.0
    assert settlement_jan.total_bills_pln == 910.0
    assert settlement_jan.total_due_pln == -910.0

    settlement_feb = manager.create_apartment_settlement("apart-polanka", 2025, 2)
    assert settlement_feb is not None
    assert settlement_feb.total_bills_pln == 0.0
    assert settlement_feb.total_due_pln == 0.0

    settlement_missing = manager.create_apartment_settlement("nie-istnieje", 2025, 1)
    assert settlement_missing is None