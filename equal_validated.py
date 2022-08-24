import flet
from flet import *

from validator import Validator, Lenght, Email, EqualTo


def main(page: Page):

    lenght_validator = Lenght(
        max_lenght=50,
        error_border_color="red",
        error_message="Max lenght must be 10 characters",
        success_border_color="green",
        success_message="Lenght is acceptable",
    )
    
    email_validator = Email(
        error_border_color="red",
        error_message="Wrong Email",
        success_border_color="green",
        success_message="Good Email",
    )
    

    login_field = TextField(
        hint_text="Username", on_change=Validator(email_validator, lenght_validator, page=page)
    )
    
    confirm_login = TextField(
        hint_text="Username", on_change=Validator(
            EqualTo(error_border_color="red",
                    error_message="Email do not match",
                    success_border_color="green",
                    success_message="Good Email",
                    field=login_field),
            page=page
        )
    )

  
    submit_btn = ElevatedButton(text='Check validation', on_click=lambda x: print(login_field.on_change.all_validated and confirm_login.on_change.all_validated))
    
    page.add(login_field, confirm_login, submit_btn)


flet.app(target=main)
