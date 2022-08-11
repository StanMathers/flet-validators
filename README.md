## Flet Validators


### Todo:
#### Validators
- [x] Email()
- [x] Lenght()
- [ ] Url()
- [ ] EqualTo()

#### Validators container
- [x] Validator()
- [ ] SubmitValidator()

#### Messages/Popups
- [ ] Toast()

## Classes
*NOTE: Every class inherits from GenericValidator and all its attributes are available*
> Parent Class
* GenericValidator(error_border_color: str = None,
        success_border_color: str = None,
        reset_border_color: str = None,
        success_message: str = None,
        error_message: str = None,
        reset_message: str = None,)
    
    ### Colors
    * error_border_color: TextField changes border color when error is occured
    * success_border_color: TextField changes border color when validation was success
    * reset_border_color: TextField changes border color when it's empty after validations

    ###  Messages
    * error_message: TextField changes hint_text when validation error is occured
    * success_message: TextField changes hint_text when validation was success
    * reset_message: TextField changes hint_text when it's empty after validations

> Children Classes (GenericValidator)
* Email()
* Lenght(max_lenght: int, min_lenght: int = 0)
    * max_lenght: Max number of characters allowed
    * min_lenght: Min number of characters allowed (0 by default)

```python
import flet
from flet import *

from validator import Validator, Lenght, Email


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

    page.add(login_field, password_field)


flet.app(target=main)

```