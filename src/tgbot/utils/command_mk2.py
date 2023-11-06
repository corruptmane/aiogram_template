import re
import shlex
import string
from typing import Any, Dict, Iterable, Literal, Optional, Sequence, Type, Union

from aiogram import Bot, F
from aiogram.filters import Command, CommandObject
from aiogram.filters.command import CommandException, CommandPatternType
from aiogram.types import Message
from pydantic import BaseModel


class CommandMk2(Command):
    def __init__(
            self,
            *patterns: CommandPatternType,
            commands: Optional[Union[Sequence[CommandPatternType], CommandPatternType]] = None,
            prefix: str = "/",
            ignore_case: bool = False,
            ignore_mention: bool = False,
            magic: Optional['F'] = None,
            response_model: Type[BaseModel] = None,
            response_model_name: Optional[str | Literal['vars']] = None,
    ):
        if commands is not None:
            patterns = (*patterns, *commands)

        original_commands = [self.extract_command(f'_{pattern}').command for pattern in patterns]
        super().__init__(
            commands=original_commands, prefix=prefix, ignore_case=ignore_case,
            ignore_mention=ignore_mention, magic=magic
        )
        if response_model is None:
            self.response_model_name = 'vars'
        elif response_model_name:
            self.response_model_name = response_model_name
        else:
            self.response_model_name = self._camel_to_snake_case(response_model.__name__)
        self.formatter = string.Formatter()
        self.signatures = self._parse_signatures(patterns)
        self.response_model = response_model

    async def __call__(self, message: Message, bot: Bot) -> Union[bool, Dict[str, Any]]:
        if not isinstance(message, Message):
            return False

        text = message.text or message.caption
        if not text:
            return False

        try:
            command = await self.parse_command(text=text, bot=bot)
        except CommandException:
            return False
        result = {"command": command}
        if command.magic_result and isinstance(command.magic_result, dict):
            result.update(command.magic_result)
        if self.signatures:
            command_ctx_vars = self._parse_vars(command)
            if self.response_model is None:
                returns_vars = command_ctx_vars
            else:
                model = self.response_model(**command_ctx_vars)
                if self.response_model_name == 'vars':
                    returns_vars = model.model_dump()
                else:
                    returns_vars = {self.response_model_name: model}
            result.update(returns_vars)
        return result

    @staticmethod
    def _camel_to_snake_case(text: str) -> str:
        return re.sub(
            # This is CamelCase to snake_case converter
            '([a-z0-9])([A-Z]+)',
            r'\1_\2',
            text,
        ).lower()

    def _parse_signatures(self, commands: Iterable[CommandPatternType]) -> Dict[str, list[str]]:
        signatures = {}
        for command in commands:
            extracted = self.extract_command(f'{self.prefix}{command}')
            fields = []
            if not extracted.args:
                continue
            for _, field_name, _, _ in self.formatter.parse(extracted.args):
                if not field_name:
                    continue
                field_name = field_name.strip()
                self._validate_field_name(field_name)
                fields.append(field_name)
            signatures.update({extracted.command: fields})
        return signatures

    def _parse_vars(self, command: CommandObject) -> Dict[str, str]:
        fields = self.signatures[command.command]
        if not command.args or not fields:
            return {}
        return dict(zip(fields, shlex.split(command.args)))

    @staticmethod
    def _validate_field_name(field_name: str) -> None:
        if ' ' in field_name:
            raise ValueError(
                f"""Invalid command argument: \"{field_name}\"!\n
                Please, name it correctly, using snake_case syntax.\n
                This name will be transformed into python variable name later."""
            )
