"""Intents for the Custody Schedule integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent, config_validation as cv
from homeassistant.util import slugify

from .const import DOMAIN, CONF_CHILD_NAME, CONF_CHILD_NAME_DISPLAY

INTENT_WHO_HAS_CHILD = "CustodyWhoHasChild"

async def async_setup_intents(hass: HomeAssistant) -> None:
    """Set up the custody intents."""
    intent.async_register(hass, CustodyWhoHasChildHandler())

class CustodyWhoHasChildHandler(intent.IntentHandler):
    """Handler for CustodyWhoHasChild intent."""

    intent_type = INTENT_WHO_HAS_CHILD
    slot_schema = {vol.Required("child_name"): cv.string}

    async def async_handle(self, intent_obj: intent.Intent) -> intent.IntentResponse:
        """Handle the intent."""
        slots = self.async_validate_slots(intent_obj.slots)
        child_name_query = slots["child_name"]["value"].lower().strip()
        
        hass = intent_obj.hass
        best_match_coordinator = None
        match_display_name = None

        # Iterate over all registered entries for our domain
        for entry_id, entry_data in hass.data.get(DOMAIN, {}).items():
            # Check if this is a valid entry data (contains coordinator)
            if not isinstance(entry_data, dict) or "coordinator" not in entry_data:
                continue
            
            entry = hass.config_entries.async_get_entry(entry_id)
            if not entry:
                continue
                
            display_name = (entry.data.get(CONF_CHILD_NAME_DISPLAY) or "").lower()
            slug_name = (entry.data.get(CONF_CHILD_NAME) or "").lower()
            
            # Simple fuzzy matching: check if query is in the name or the name is in the query
            if child_name_query in display_name or child_name_query in slug_name or display_name in child_name_query:
                best_match_coordinator = entry_data["coordinator"]
                match_display_name = entry.data.get(CONF_CHILD_NAME_DISPLAY, entry.data.get(CONF_CHILD_NAME))
                break
        
        response = intent_obj.create_response()
        
        if not best_match_coordinator:
            response.async_set_speech(f"Désolé, je ne trouve pas d'enfant nommé {child_name_query} dans votre configuration Custody.")
            return response
            
        data = best_match_coordinator.data
        if not data:
            response.async_set_speech(f"Je n'ai pas encore pu calculer la position de {match_display_name}.")
            return response
            
        if data.is_present:
            text = f"{match_display_name} est actuellement avec vous."
        else:
            text = f"{match_display_name} est actuellement chez l'autre parent."
            
        response.async_set_speech(text)
        return response
