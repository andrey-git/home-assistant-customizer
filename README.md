# Home-assistant customizer comonent
Custom component for [home-assistant](https://home-assistant.io)

* Optionally loads CustomUI files. [HA 0.53+]
* Optionally registers CustomUI panel.
* Specify a list of attributes to hide from `more-info` window.
* [HA 0.50 - 0.52] Hide CustomUI - related attributes in `more-info` window. From HA 0.53 they are hidden automatically.
* Add services for dynamic customization.

## Installing
Put `customizer` dir in `<ha_config_dir>/custom_components/`

## Using
`configuration.yaml` options (all optional):

attribute | type           | description |
--        | --             | -- |
panel     | Bool (default false) | [Ignored in HA 0.53+] Whether to register [CustomUI configuration panel](https://github.com/andrey-git/home-assistant-custom-ui). |
custom_ui [HA 0.53+]| local / hosted<br>version_tag | Whether to fetch CustomUI files.<br>`local` loads it from `<config_dir>/www/custom_ui/state-card-custom-ui.html`.<br>`hosted` loads it from https://raw.githubusercontent.com/andrey-git/home-assistant-custom-ui/master/state-card-custom-ui.html<br>version_tag (for example 20170830) loads a tagged version from 'https://github.com/andrey-git/home-assistant-custom-ui/releases/download/20170830/state-card-custom-ui.html' |
hide_customui_attributes | Bool (default true) | [Ignored in HA 0.53+] Hide attributes used in CustomUI from more-info popups. |
hide_attributes | List of strings | List of attributes to hide from more-info popups. (Requires CustomUI) |

Example HA 0.53:
```yaml
customizer:
  custom_ui: local
  hide_attributes:
    - node_id
    - value_index
```

Example HA 0.52:
```yaml
customizer:
  panel: true
  hide_customui_attributes: false
  hide_attributes:
    - node_id
    - value_index
```

## Services

The component exposes a `set_attribute` service.
It sets (or clears) persistent attribute of an entity overriding any value set in code.
Like specifying it in `homeassistant -> customize` YAML section.


Note that calling `homeassistant.reload_core_config` service or changing customization via Config panel will reset overrides to their yaml state.

Service fields:

name | description | example
-- | -- | --
entity_id | Entity ID to set the attribute on | light.patio
attribute | Name of the attribute to set | friendly_name
value | (Optional) Value to set. Leave unspecified in order to clear set value. Note that when clearing attribute it will be empty (and not set-by-code) until next entity update | My light'
