# SonosAlarmAutomation

App that brings alarm snoozing to SONOS using the custom component SonosAlarm.

## Requirements
`SonosAlarm` - https://github.com/AaronDavidSchneider/SonosAlarm

## Installation

Download the `SonosAlarm` directory from inside the `apps` directory here to your local `apps` directory, then add the configuration to enable the `SonosAlarm` module.

or use HACS
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

## App configuration

```yaml
alarm:
  module:    SonosAlarm
  class:     SonosAlarm
  entity_id: [your media_player]
  ids:
    - [ your alarm ids ]
```

## Additional configuration needed:

`groups.yaml`
```yaml
sonos_alarm:
    name: SONOS ALARM
    icon: mdi:alarm
    entities:
      - switch.sonos_alarm_[ your alarm ids ]
```

`configuration.yaml`
```yaml
input_number:
    alarm_snooze:
      name: Snooze Dauer
      min: 5 #optional
      max: 60 #optional
      step: 5 #optional
      icon: mdi:sleep #optional
    alarm_clock_hour:
      name: Stunde
      icon: mdi:timer #optional
      min: 4 #optional
      max: 10 #optional
      step: 1 #optional
    alarm_clock_minute:
      name: Minute
      icon: mdi:timer #optional
      min: 0 #optional
      max: 55 #optional
      step: 5 #optional
    alarm_volume:
      name: Lautstärke Wecker
      icon: mdi:volume-high #optional
      min: 0.0 #optional
      max: 0.3 #optional
      mode: box #optional
```
`min`, `max`,`step`,`mode`,`icon` are just personal preferences and optional.
