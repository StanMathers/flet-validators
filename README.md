## Flet Validators


### Todo:
#### Validators
- [x] Email()
- [x] Lenght()
- [ ] Url()
- [x] EqualTo()

#### Validators container
- [x] Validator()
- [ ] SubmitValidator()

#### Messages/Popups
- [ ] Toast()

### Speacial features
- Now **Validator** class has special property called **all_validated** returning True if all the validations were success, otherwise False

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
* EqualTo(field: Type[Control])
    * field: Takes TextField as an argument and compares current value to its argument

## Lenght, Email
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
## EqualTo and *all_validated*
```python
import flet
from flet import *

from validator import Validator, Lenght, Email, EqualTo


def main(page: Page):
    """
    Here we validate `lenght` and `email` of login_field and check if `confirm_login` is equal to `login_field`.
    At last, we create button to check if everything is correct to validate correct data by using `all_validated` property.
    If validations are correct, it return True, otherwise False 
    """

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


```
