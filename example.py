import flet
from flet import *

from validator import Validator, Lenght, Email, EqualTo


def main(page: Page):

    lenght_validator = Lenght(
        max_lenght=20,
        error_border_color="red",
        error_message="Max lenght must be 20 chars long",
        success_border_color="green",
        success_message="20 chars are accepted",
    )
    
    email_validator = Email(
        error_border_color="red",
        error_message="Email",
        success_border_color="green",
        success_message="Good Email",
    )
    

    login_field = TextField(
        hint_text="Username", on_change=Validator(email_validator, lenght_validator, page=page, validators_list=True)
    )

    password_field = TextField(
        hint_text="Password",
        password=True,
        on_change=Validator(lenght_validator, page=page),
    )

    equal_to_validator = EqualTo(
        field=password_field,
        error_message='Passwords do not match',
        error_border_color='red',
        success_message='Passwords match',
        success_border_color='green'
    )
    
    confirm_password = TextField(
        hint_text='Password',
        password=True,
        on_change=Validator(equal_to_validator, page=page)
    )
    
    page.add(login_field, password_field, confirm_password)


flet.app(target=main)
