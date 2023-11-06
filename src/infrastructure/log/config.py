from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class LoggingConfig:
    level: str = 'DEBUG'
    render_json_logs: bool = False
    show_locals: bool = True
    max_frames: int = 100
    locals_max_length: int | None = None
    locals_max_string: int | None = None
