import logging
import re
import aiohttp
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)

URL = "https://ebok.gkpge.pl/ebok/profil/logowanie.xhtml"

class PgeEbokApiError(Exception):
    """Exception raised for API errors."""
    pass

class PgeEbokAuthError(PgeEbokApiError):
    """Exception raised for authentication errors."""
    pass

class PgeEbokApi:
    """Class to communicate with the PGE eBOK portal."""

    def __init__(self, username, password, session: aiohttp.ClientSession):
        """Initialize the API object."""
        self._username = username
        self._password = password
        self._session = session
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }

    async def get_balance(self) -> float:
        """Fetch the current balance from the portal."""
        try:
            # 1. Fetch ViewState
            async with self._session.get(URL, headers=self._headers, timeout=15) as response:
                response.raise_for_status()
                html = await response.text()

            soup = BeautifulSoup(html, 'html.parser')
            view_state_input = soup.find("input", {"name": "javax.faces.ViewState"})

            if not view_state_input:
                raise PgeEbokApiError("Nie znaleziono ViewState na stronie logowania PGE")

            view_state = view_state_input['value']

            # 2. Login
            payload = {
                'hiddenLoginForm': 'hiddenLoginForm',
                'hiddenLoginForm:hiddenLogin': self._username,
                'hiddenLoginForm:hiddenPassword': self._password,
                'hiddenLoginForm:loginButton': '',
                'javax.faces.ViewState': view_state
            }

            async with self._session.post(URL, data=payload, headers=self._headers, timeout=15) as res:
                res.raise_for_status()
                res_html = await res.text()

            # 3. Check login success and parse balance
            soup_logged = BeautifulSoup(res_html, 'html.parser')

            # Simple check for authentication failure: if we are still on the login page or see a known error message.
            # Assuming the form element specific to logged-in user is missing.
            container = soup_logged.find("div", {"id": "formNaleznosc:idSaldoNaDzien_content"})

            if not container:
                # If we didn't find the balance container, it might mean we didn't login properly.
                raise PgeEbokAuthError("Nie znaleziono kontenera salda. Sprawdź, czy dane logowania są poprawne.")

            label = container.find("label")
            # Fallback to the container's full text if no label is found inside
            text_source = label.text if label else container.text

            # Clean the text, remove spaces and replace comma with dot
            saldo_str = text_source.strip().replace(' ', '').replace(',', '.')

            # Extract numerical value
            match = re.search(r'-?\d+(\.\d+)?', saldo_str)
            if match:
                return float(match.group())

            raise PgeEbokApiError(f"Nie udało się przekonwertować salda na liczbę: {saldo_str}")

        except aiohttp.ClientError as e:
            raise PgeEbokApiError(f"Błąd połączenia z portalem PGE: {e}") from e
        except Exception as e:
            if isinstance(e, (PgeEbokApiError, PgeEbokAuthError)):
                raise
            raise PgeEbokApiError(f"Nieoczekiwany błąd komunikacji: {e}") from e

    async def test_authentication(self) -> bool:
        """Test if the provided credentials are valid."""
        try:
            await self.get_balance()
            return True
        except PgeEbokAuthError:
            return False
        except Exception as e:
            # Re-raise non-auth errors
            raise PgeEbokApiError(f"Błąd testowania uwierzytelnienia: {e}") from e
