"""Customizer component. Bring extra customize features to home-assistant."""

import asyncio
import logging
import os

from homeassistant.components.frontend import register_panel
import homeassistant.helpers.config_validation as cv
from homeassistant.config import load_yaml_config_file, DATA_CUSTOMIZE

from homeassistant.core import callback

from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.const import CONF_ENTITY_ID

import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

DOMAIN = 'customizer'
DEPENDENCIES = ['frontend']

CONF_PANEL = 'panel'
CONF_HIDE_CUSTOMUI_ATTRIBUTES = 'hide_customui_attributes'
CONF_HIDE_ATTRIBUTES = 'hide_attributes'

CONF_ATTRIBUTE = 'attribute'
CONF_VALUE = 'value'

SERVICE_SET_ATTRIBUTE = 'set_attribute'
SERVICE_SET_ATTRIBUTE_SCHEMA = vol.Schema({
    vol.Required(CONF_ENTITY_ID): cv.entity_id,
    vol.Required(CONF_ATTRIBUTE): cv.string,
    vol.Optional(CONF_VALUE): cv.match_all,
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_PANEL): cv.boolean,
        vol.Optional(CONF_HIDE_CUSTOMUI_ATTRIBUTES, default=True): cv.boolean,
        vol.Optional(CONF_HIDE_ATTRIBUTES):
            vol.All(cv.ensure_list, [cv.string]),
    })
}, extra=vol.ALLOW_EXTRA)


@asyncio.coroutine
def async_setup(hass, config):
    """Set up customizer."""
    if config[DOMAIN].get(CONF_PANEL):
        register_panel(
            hass,
            "custom-ui",
            hass.config.path('panels/ha-panel-custom-ui.html'),
            sidebar_title="Custom UI",
            sidebar_icon="mdi:domain"
        )

    component = EntityComponent(_LOGGER, DOMAIN, hass)
    yield from component.async_add_entity(CustomizerEntity(config[DOMAIN]))

    descriptions = yield from hass.async_add_job(
        load_yaml_config_file, os.path.join(
            os.path.dirname(__file__), 'services.yaml'))

    @callback
    def set_attribute(call):
        """Set attribute override."""
        data = call.data
        entity_id = data[CONF_ENTITY_ID]
        attribute = data[CONF_ATTRIBUTE]
        value = data.get(CONF_VALUE)
        overrides = hass.data[DATA_CUSTOMIZE].get(entity_id)
        state = hass.states.get(entity_id)
        state_attributes = dict(state.attributes)
        if value is None:
            if attribute in overrides:
                overrides.pop(attribute)
            if attribute in state_attributes:
                state_attributes.pop(attribute)
        else:
            overrides[attribute] = value
            state_attributes[attribute] = value
        hass.states.async_set(entity_id, state.state, state_attributes)

    hass.services.async_register(DOMAIN, SERVICE_SET_ATTRIBUTE,
                                 set_attribute,
                                 descriptions[SERVICE_SET_ATTRIBUTE],
                                 SERVICE_SET_ATTRIBUTE_SCHEMA)

    return True


class CustomizerEntity(Entity):
    """Customizer entity class."""

    def __init__(self, config):
        """Constructor that parses the config."""
        self.hide_customui_attributes = config.get(
            CONF_HIDE_CUSTOMUI_ATTRIBUTES)
        self.hide_attributes = config.get(CONF_HIDE_ATTRIBUTES)

    @property
    def hidden(self):
        """Don't show the entity."""
        return True

    @property
    def name(self):
        """Singleton name."""
        return DOMAIN

    @property
    def state_attributes(self):
        """Return the state attributes."""
        result = {}
        if self.hide_customui_attributes:
            result[CONF_HIDE_CUSTOMUI_ATTRIBUTES] = True
        if self.hide_attributes:
            result[CONF_HIDE_ATTRIBUTES] = self.hide_attributes
        return result
