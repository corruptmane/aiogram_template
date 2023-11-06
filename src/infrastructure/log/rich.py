import shutil
from typing import TextIO

import structlog
from rich.console import Console
from rich.traceback import Traceback

from src.infrastructure.log.config import LoggingConfig


class RichExceptionFormatter:
    def __init__(self, config: LoggingConfig) -> None:
        self.show_locals = config.show_locals
        self.max_frames = config.max_frames
        self.locals_max_length = config.locals_max_length
        self.locals_max_string = config.locals_max_string
        self.term_width, *_ = shutil.get_terminal_size((80, 123))

    def __call__(self, sio: TextIO, exc_info: structlog.typing.ExcInfo) -> None:
        sio.write("\n")
        Console(file=sio, color_system="truecolor").print(
            Traceback.from_exception(
                *exc_info,
                show_locals=self.show_locals,
                max_frames=self.max_frames,
                locals_max_string=self.locals_max_string,
                locals_max_length=self.locals_max_length,
                width=self.term_width,
            )
        )
