# Home-assistant customizer comonent
Custom component for [home-assistant](https://home-assistant.io)

Adds customization features and optionally registers CustomUI panel.

## Installing
Put `customizer` dir in `<ha_config_dir>/custom_components/`

## Using
`configuration.yaml` options:

attribute | default | description
-- | -- | --
panel | false | Whether to register [CustomUI configuration panel](https://github.com/andrey-git/home-assistant-custom-ui).
hide_customui_attributes | true | Hide attributes used in CustomUI from more-info popups. 
hide_attributes | [ ] (empty list) | List of attributes to hide from more-info popups. (Requires CustomUI)

Example:
```yaml
customizer:
  panel: true
  hide_customui_attributes: false
  hide_attributes:
    - node_id
    - value_index
```

## Services

The component exposes a `set_attribute` service. It sets (or clears) persistent attribute of an entity overriding any value set in code. (Like specifying it in `homeassistant -> customize` YAML section.


Note that calling `homeassistant.reload_core_config` service will reset overrides to their yaml state.

Service fields:

name | description | example
-- | -- | --
entity_id | Entity ID to set the attribute on | light.patio
attribute | Name of the attribute to set | friendly_name
value | (Optional) Value to set. Leave unspecified in order to clear set value. Note that when clearing attribute it will be empty (and not set-by-code) until next entity update | My light'
