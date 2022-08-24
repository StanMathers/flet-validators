import flet
from flet import *

from validator import Validator, Lenght, Email, EqualTo


def main(page: Page):

    lenght_validator = Lenght(
        max_lenght=10,
        error_border_color="red",
        error_message="Some error message",
        success_border_color="green",
        success_message="Seems good!",
    )
    
    email_validator = Email(
        error_border_color="red",
        error_message="Wrong Email",
        success_border_color="green",
        success_message="Good Email",
    )
    

    login_field = TextField(
        hint_text="Username", on_change=Validator(email_validator, page=page)
    )

    password_field = TextField(
        hint_text="Password",
        password=True,
        on_change=Validator(lenght_validator, page=page),
    )

    # EqualTo validator
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
