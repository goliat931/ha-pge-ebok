import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN
from .pge_api import PgeEbokApi, PgeEbokApiError, PgeEbokAuthError

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)

class PgeEbokConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PGE eBOK."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_USERNAME])
            self._abort_if_unique_id_configured()

            session = async_get_clientsession(self.hass)
            api = PgeEbokApi(user_input[CONF_USERNAME], user_input[CONF_PASSWORD], session)

            try:
                valid = await api.test_authentication()
                if not valid:
                    errors["base"] = "invalid_auth"
            except PgeEbokAuthError:
                errors["base"] = "invalid_auth"
            except PgeEbokApiError:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

            if not errors:
                return self.async_create_entry(
                    title=f"PGE eBOK ({user_input[CONF_USERNAME]})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )
