import logging
import re
from datetime import timedelta

import requests
from bs4 import BeautifulSoup
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "pge_ebok"
URL = "https://ebok.gkpge.pl/ebok/profil/logowanie.xhtml"

SCAN_INTERVAL = timedelta(hours=6)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Konfiguracja platformy sensora PGE."""
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    add_entities([PgeEbokSensor(username, password)], True)

class PgeEbokSensor(SensorEntity):
    """Klasa reprezentująca sensor salda PGE eBOK."""

    def __init__(self, username, password):
        """Inicjalizacja sensora."""
        self._username = username
        self._password = password
        self._state = None
        self._attr_name = "PGE eBOK Saldo"
        self._attr_native_unit_of_measurement = "PLN"
        self._attr_device_class = "monetary"
        self._attr_icon = "mdi:flash"
        self._attr_unique_id = f"pge_ebok_{username}"

    @property
    def native_value(self):
        """Zwraca obecny stan sensora."""
        return self._state

    def update(self):
        """Pobiera najnowsze dane ze strony internetowej (wywoływane co SCAN_INTERVAL)."""
        session = requests.Session()
        try:
            # 1. Pobranie ViewState
            response = session.get(URL, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            view_state_input = soup.find("input", {"name": "javax.faces.ViewState"})

            if not view_state_input:
                _LOGGER.error("Nie znaleziono ViewState na stronie logowania PGE")
                return

            view_state = view_state_input['value']

            # 2. Logowanie
            payload = {
                'hiddenLoginForm': 'hiddenLoginForm',
                'hiddenLoginForm:hiddenLogin': self._username,
                'hiddenLoginForm:hiddenPassword': self._password,
                'hiddenLoginForm:loginButton': '',
                'javax.faces.ViewState': view_state
            }

            res = session.post(URL, data=payload, timeout=15)

            # 3. Parsowanie salda
            soup_logged = BeautifulSoup(res.text, 'html.parser')
            container = soup_logged.find("div", {"id": "formNaleznosc:idSaldoNaDzien_content"})

            if container:
                label = container.find("label")
                if label:
                    # Wyciągamy czysty tekst, usuwamy spacje i zamieniamy przecinek na kropkę
                    saldo_str = label.text.strip().replace(' ', '').replace(',', '.')

                    # Ekstrakcja samej wartości numerycznej (np. z "-123.45 zł")
                    match = re.search(r'-?\d+(\.\d+)?', saldo_str)
                    if match:
                        self._state = float(match.group())
                    else:
                        _LOGGER.warning("Nie udało się przekonwertować salda na liczbę: %s", saldo_str)
                        self._state = None
                else:
                    _LOGGER.error("Nie znaleziono etykiety z saldem w kontenerze.")
            else:
                _LOGGER.error("Nie znaleziono kontenera salda. Sprawdź, czy dane logowania są poprawne.")

        except requests.exceptions.RequestException as e:
            _LOGGER.error("Błąd połączenia z portalem PGE: %s", e)
        except Exception as e:
            _LOGGER.error("Nieoczekiwany błąd podczas aktualizacji sensora PGE: %s", e)
