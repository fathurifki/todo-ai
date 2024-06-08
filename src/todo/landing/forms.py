from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.db import connection

User = get_user_model()


class UserCreationForm(forms.ModelForm):

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"autocomplete": "username"}),
        help_text="Enter your desired username.",
    )

    class Meta:
        model = User
        fields = ["email", "username"]

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                        [user.username, user.password, user.email]
                    )
            except Exception as e:
                print(f"An error occurred: {e}")
        return user

class SettingsForm(forms.ModelForm):

    password = forms.CharField(
        label="Password",
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ["email"]

    def save(self, commit: bool = True) -> User:
        user = super().save(commit=False)
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user