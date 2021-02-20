import time
from typing import List, Union

import blinkt
from arrow import Arrow, now


class Color:
    R: int
    G: int
    B: int

    def __init__(self, red: int, green: int, blue: int, name: str = "") -> None:
        self.R = red
        self.G = green
        self.B = blue
        self.name = name

    def __repr__(self) -> str:
        return f"<Color: {self.name} 0x{self.R:02x}{self.G:02x}{self.B:02x}>"


class Colors:
    OFF: None = None

    GREEN: Color = Color(0x00, 0xFF, 0x80, "green")
    RED: Color = Color(0xFF, 0x00, 0x00, "red")
    YELLOW: Color = Color(0xFF, 0xFF, 0x00, "yellow")

    DARK_GREEN: Color = Color(0x00, 0xCC, 0x66, "dark-green")
    DARK_RED: Color = Color(0xCC, 0x00, 0x00, "dark-red")
    DARK_YELLOW: Color = Color(0xCC, 0xCC, 0x00, "dark-yellow")


class Event:
    record_id: int
    start_time: Arrow
    end_time: Arrow
    color: Color

    def __init__(
        self, record_id: int, start_time: Arrow, end_time: Arrow, color: Color
    ) -> None:
        self.record_id = record_id
        self.start_time = start_time
        self.end_time = end_time
        self.color = color

    def __repr__(self) -> str:
        return f"<Event id:{self.record_id} s:{self.start_time} e:{self.end_time} c:{self.color}>"


class Database:
    events: List[Event]

    def __init__(self) -> None:
        self.events = list()

    def __len__(self) -> int:
        return len(self.events)

    def __repr__(self) -> str:
        lines = ["- " + repr(evt) for evt in self.events]

        lines.insert(0, f"<Database {id(self):#x} len:{len(self)}>")

        return "\n".join(lines)

    def create_event(self, start_time: Arrow, end_time: Arrow, color: Color) -> None:
        self.events.append(Event(len(self), start_time, end_time, color))

    def find_current_event(self) -> Union[Event, None]:
        current_time: Arrow = now()

        for event in self.events:
            if ((event.start_time.hour > current_time.hour) or (event.start_time.minute > current_time.minute) or (event.start_time.second > current_time.second)):
                continue

            if event.end_time <= current_time:
                continue

            return event

        return None


def init() -> Database:
    db = Database()

    db.create_event(
        now().replace(hour=0, minute=0),
        now().replace(hour=6, minute=0),
        color=Colors.OFF,
    )
    db.create_event(
        now().replace(hour=6, minute=0),
        now().replace(hour=6, minute=50),
        color=Colors.RED,
    )
    db.create_event(
        now().replace(hour=6, minute=50),
        now().replace(hour=7, minute=0),
        color=Colors.YELLOW,
    )
    db.create_event(
        now().replace(hour=7, minute=0),
        now().replace(hour=8, minute=0),
        color=Colors.GREEN,
    )
    db.create_event(
        now().replace(hour=8, minute=0),
        now().replace(hour=13, minute=30),
        color=Colors.OFF,
    )
    db.create_event(
        now().replace(hour=13, minute=30),
        now().replace(hour=15, minute=45),
        color=Colors.RED,
    )
    db.create_event(
        now().replace(hour=15, minute=45),
        now().replace(hour=16, minute=30),
        color=Colors.YELLOW,
    )
    db.create_event(
        now().replace(hour=16, minute=30),
        now().replace(hour=17, minute=0),
        color=Colors.GREEN,
    )
    db.create_event(
        now().replace(hour=17, minute=0),
        now().replace(hour=23, minute=59),
        color=Colors.OFF,
    )

    return db


def main():
    db = init()

    while True:
        time.sleep(30)
        evt = db.find_current_event()
        if evt is not None:
            blinkt.set_all(evt.R, evt.G, rgb.B, 0.5)
        else:
            blink.clear()
        # evt


if __name__ == "__main__":
    main()
