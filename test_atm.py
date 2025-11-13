from atm import ATMMachine, ATMService


def test_init_atm_service():
    atm_svc = ATMService()
    assert atm_svc.initial_state ==