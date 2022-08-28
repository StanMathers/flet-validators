import flet
from flet import *
from flet.page import ControlEvent

from typing import Any, Type
from email_validator import EmailNotValidError, validate_email


class GenericValidator:
    def __init__(
        self,
        error_border_color: str = None,
        success_border_color: str = None,
        reset_border_color: str = None,
        success_message: str = None,
        error_message: str = None,
        reset_message: str = None,
    ) -> None:

        self.error_border_color = error_border_color
        self.success_border_color = success_border_color
        self.reset_border_color = reset_border_color

        self.success_message = success_message
        self.error_message = error_message
        self.reset_message = reset_message

    def _set_success(self, e: Type[ControlEvent]):
        e.control.border_color = self.success_border_color

    def _set_error(self, e: Type[ControlEvent]):
        e.control.border_color = self.error_border_color

    def _set_reset(self, e: Type[ControlEvent]):
        e.control.border_color = self.reset_border_color

    def _set_success_msg(self, e: Type[ControlEvent], kwargs):
        if kwargs["v_list"] is True:
            if str(e.control.helper_text).count(kwargs["l_char"]) == kwargs["n_items"]:
                e.control.helper_text = ""

            e.control.helper_text += (
                "-" + " ✓ " + self.success_message + "\n"
                if self.success_message is not None
                else None
            )

        else:
            e.control.helper_text = (
                self.success_message if self.success_message is not None else None
            )

    def _set_error_msg(self, e: Type[ControlEvent], kwargs):
        if kwargs["v_list"] is True:
            if str(e.control.helper_text).count(kwargs["l_char"]) == kwargs["n_items"]:
                e.control.helper_text = ""

            e.control.helper_text += (
                "-" + " ✕ " + self.error_message + "\n"
                if self.error_message is not None
                else None
            )

        else:
            e.control.helper_text = (
                self.error_message if self.error_message is not None else None
            )

    def _set_reset_msg(self, e: Type[ControlEvent], kwargs):

        e.control.helper_text = (
            self.reset_message if self.reset_message is not None else None
        )


class Validator:
    def __init__(
        self,
        *validator,
        page: Type[Page],
        validators_list: bool = None,
        listing_char: str = "-"
    ) -> None:
        self.validator = validator
        self.page = page
        self.validators_list = validators_list
        self.listing_char = listing_char

        self._vals = []
        self.all_validated = None

    def __call__(self, e: Type[ControlEvent]) -> Any:
        self.e = e

        # NoneType fix for concatenating
        if self.e.control.helper_text is None:
            e.control.helper_text = ""
            self.page.update()

        for i in self.validator:

            if len(self._vals) == len(self.validator):
                self._vals.clear()

            # Giving data to validator's **kwargs
            self._vals.append(
                i(
                    self.e,
                    v_list=self.validators_list,
                    n_items=len(self.validator),
                    l_char=self.listing_char,
                )
            )
            self.page.update()

            self.all_validated = all(self._vals)

        if self.validators_list is True:
            if str(e.control.helper_text).count(self.listing_char) == len(
                self.validator
            ):
                e.control.helper_text = ""


class Lenght(GenericValidator):
    def __init__(
        self,
        max_lenght: int,
        min_lenght=0,
        error_border_color: str = None,
        success_border_color: str = None,
        reset_border_color: str = None,
        success_message: str = None,
        error_message: str = None,
        reset_message: str = None,
    ) -> None:
        super().__init__(
            error_border_color,
            success_border_color,
            reset_border_color,
            success_message,
            error_message,
            reset_message,
        )
        self.max_lenght = max_lenght
        self.min_lenght = min_lenght

    def __call__(self, e: Type[ControlEvent], **kwargs) -> Any:
        field_lenght = len(e.control.value)

        if field_lenght > self.max_lenght:
            self._set_error_msg(e, kwargs)
            self._set_error(e)
            return False

        elif self.min_lenght < field_lenght < self.max_lenght:
            print(kwargs)
            self._set_success_msg(e, kwargs)
            self._set_success(e)
            return True

        elif field_lenght == 0:
            self._set_reset(e)
            self._set_reset_msg(e, kwargs)


class Email(GenericValidator):
    def __init__(
        self,
        granular_message=False,
        check_deliverability=False,
        allow_smtputf8=True,
        allow_empty_local=False,
        error_border_color: str = None,
        success_border_color: str = None,
        reset_border_color: str = None,
        success_message: str = None,
        error_message: str = None,
        reset_message: str = None,
    ) -> None:
        super().__init__(
            error_border_color,
            success_border_color,
            reset_border_color,
            success_message,
            error_message,
            reset_message,
        )

        self.granular_message = granular_message
        self.check_deliverability = check_deliverability
        self.allow_smtputf8 = allow_smtputf8
        self.allow_empty_local = allow_empty_local

    def __call__(self, e, **kwargs):
        print(kwargs)
        val = e.control.value
        try:
            if len(val) == 0:
                self._set_error_msg(e, kwargs)
                self._set_error(e)

            elif validate_email(
                val,
                check_deliverability=self.check_deliverability,
                allow_smtputf8=self.allow_smtputf8,
                allow_empty_local=self.allow_empty_local,
            ):
                self._set_success_msg(e, kwargs)
                self._set_success(e)
                return True

        except EmailNotValidError as g:
            self._set_error_msg(e, kwargs)
            self._set_error(e)
            return False


class EqualTo(GenericValidator):
    def __init__(
        self,
        error_border_color: str = None,
        success_border_color: str = None,
        reset_border_color: str = None,
        success_message: str = None,
        error_message: str = None,
        reset_message: str = None,
        field: Control = None,
    ) -> None:
        super().__init__(
            error_border_color,
            success_border_color,
            reset_border_color,
            success_message,
            error_message,
            reset_message,
        )
        self.field = field

    def __call__(self, e: Type[ControlEvent], **kwargs):
        current_field_val = e.control.value
        compare_field_val = self.field.value

        if current_field_val == compare_field_val:
            self._set_success_msg(e, kwargs)
            self._set_success(e)
            return True

        elif current_field_val != compare_field_val:
            self._set_error_msg(e, kwargs)
            self._set_error(e)
            return False

        else:
            self._set_reset_msg(e, kwargs)
            self._set_reset(e)
