import appdaemon.plugins.hass.hassapi as hass

class SonosAlarm(hass.Hass):
    def initialize(self):
        entities = [
            "group.sonos_alarm",
            "input_number.alarm_volume",
            "input_number.alarm_snooze",
            "input_number.alarm_clock_hour",
            "input_number.alarm_clock_minute",
        ]
        self.target = None

        for e in entities:
            self.listen_state(self.update_alarm, e)

    def update_alarm(self, entity=None, attribute=None, old=None, new=None, kwargs=None):
        self.log("update_alarm")
        alarm_correct = self.check_alarm()
        if not alarm_correct:
            ids = self.args["ids"]
            hour = float(self.get_state("input_number.alarm_clock_hour"))
            minute = float(self.get_state("input_number.alarm_clock_minute"))
            snooze = float(self.get_state("input_number.alarm_snooze"))
            volume = float(self.get_state("input_number.alarm_volume"))
            enabled = self.get_state("group.sonos_alarm")
            times = []


            for i in range(len(ids)):
                m = (minute + i * snooze) % 60
                h = hour + int((minute + i * snooze) / 60)
                time = "{:02d}:{:02d}:00".format(int(h) , int(m))
                times.append(time)

                self.call_service(
                    "sonos/update_alarm",
                    entity_id=self.args["entity_id"],
                    alarm_id=ids[i],
                    time=time,
                    volume=volume,
                    enabled=enabled,
                )

                self.call_service(
                    "homeassistant/update_entity",
                    entity_id="switch.sonos_alarm_{}".format(ids[i]),
                )

            self.target = {
                "ids": ids,
                "times": times,
                "enabled": enabled,
                "volume": volume,
            }
            self.log("Next iteration")
            self.run_in(self.update_alarm, 2)
        else:
            self.log("Wecker updated correctly")
            self.target=None

    def check_alarm(self):
        if self.target is None:
            return False
        else:
            for i in range(len(self.target["ids"])):
                state = self.get_state(
                    "switch.sonos_alarm_{}".format(self.target["ids"][i]), attribute="all"
                )
                attr = state["attributes"]
                state = state["state"]

                if (
                    state != self.target["enabled"]
                    or attr["time"] != self.target["times"][i]
                    or attr["volume"] != self.target["volume"]
                ):
                    return False
            return True
