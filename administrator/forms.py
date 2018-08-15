from django import forms
from django.contrib.auth import get_user_model
# Create forms here

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['email', 'first_name', 'last_name', 'middle_name']

	def clean_password2(self):
		# Check that the two password entries match
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and (password1 != password2):
			raise forms.ValidationError("Passwords don't match")
		return password2


class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email']
