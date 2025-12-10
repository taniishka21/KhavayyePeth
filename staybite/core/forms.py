from django import forms
from django.contrib.auth.models import User

class UserUpdateForm(forms.ModelForm):
    """
    A form for updating a user's profile.
    It's a ModelForm, which means it's directly tied to a model (in this case, the User model).
    This makes it easy to save changes to the database.
    """
    
    # We override the default email field to ensure it is always required
    email = forms.EmailField(required=True)

    class Meta:
        # The model that this form will be linked to
        model = User
        
        # The fields from the User model that will be included in the form
        fields = ['first_name', 'last_name', 'email']

