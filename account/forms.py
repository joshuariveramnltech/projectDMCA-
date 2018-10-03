from django.contrib.auth import get_user_model
from django import forms
from django.forms import DateField, Textarea, FileInput
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Profile, LevelAndSection, Level,
    StudentProfile, StaffProfile, FacultyProfile
)
User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = (
            'email', 'first_name',
            'last_name', 'middle_name',
            'date_of_birth', 'gender', 'address',
            'is_active', 'is_student',
            'is_teacher', 'is_staff', 'is_superuser'
        )
        labels = {
            'is_active': 'Active',
            'is_student': 'Student',
            'is_teacher': 'Teacher',
            'is_staff': 'Staff',
            'is_superuser': 'Superuser'
        }

    date_of_birth = forms.DateField(
        widget=forms.DateInput(format='%m/%d/%Y',
                               attrs={'class': 'datepicker', 'placeholder': 'mm/dd/yyyy'}),
        input_formats=('%m/%d/%Y', )
    )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email', 'first_name',
            'last_name', 'middle_name',
            'date_of_birth', 'gender', 'address',
            'is_active', 'is_student',
            'is_teacher', 'is_staff',
            'is_superuser', 'password'
        )

        labels = {
            'is_active': 'Active',
            'is_student': 'Student',
            'is_teacher': 'Teacher',
            'is_staff': 'Staff',
            'is_superuser': 'Superuser'
        }

    date_of_birth = forms.DateField(
        widget=forms.DateInput(format='%m/%d/%Y',
                               attrs={'class': 'datepicker', 'placeholder': 'mm/dd/yyyy'}),
        input_formats=('%m/%d/%Y', )
    )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserEditForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'email', 'first_name',
            'last_name', 'middle_name',
            'date_of_birth', 'gender', 'address',
            'is_active', 'password'
        )

        labels = {
            'is_active': 'Active',
            'is_student': 'Student',
            'is_teacher': 'Teacher',
            'is_staff': 'Staff',
            'is_superuser': 'Superuser'
        }

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            format='%m/%d/%Y',
            attrs={'class': 'datepicker', 'placeholder': 'mm/dd/yyyy'}
        ),
        input_formats=('%m/%d/%Y', )
    )

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm  # update view
    add_form = UserCreationForm  # create view

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'email', 'is_active',
        'is_student', 'is_teacher',
        'is_staff', 'is_superuser'
    )
    list_filter = ('is_student', 'is_teacher', 'is_staff', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'middle_name', 'date_of_birth', 'gender', 'address')}),
        ('Status', {'fields': ('is_active', ), }),
        ('Permissions', {'fields': ('is_student',
                                    'is_teacher', 'is_staff', 'is_superuser')}),
    )

    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name',
                'last_name', 'middle_name',
                'date_of_birth', 'gender', 'address',
                'is_active', 'is_student',
                'is_teacher', 'is_staff',
                'is_superuser', 'password1',
                'password2'
            )
        }
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# for administrator/staff only
class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'phone_number', 'age']

        labels = {'photo': 'Profile Picture', 'age': 'Age'}

        widgets = {
            'phone_number': Textarea(attrs={'placeholder': '0999-999-9999', 'cols': 20, 'rows': 1})
        }


# for students/teachers/staff personal use only
class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['photo', 'phone_number', 'age']

        labels = {
            'photo': 'Profile Picture',
        }

        widgets = {
            'photo': FileInput(attrs={'class': 'file-field'})
        }


# for ordinary users only
class PersonalForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['date_of_birth', 'address']

        labels = {
            'date_of_birth': 'Birthday',
        }

    date_of_birth = forms.DateField(
        widget=forms.DateInput(
            attrs={'class': 'datepicker', 'placeholder': 'mm/dd/yyyy'},
            format='%m/%d/%Y'
        ),
        input_formats=('%m/%d/%Y', )
    )

    address = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': '', 'rows': 5, 'cols': 100}
        )
    )


# student profile form for admin
class StudentProfileAdminForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['user', ]
        labels = {
            'guardian_contact_number': 'Guardian\'s Contact Number',
        }


# faculty profile form for admin
class FacultyProfileAdminForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        exclude = ['user', ]
        labels = {'designated_year_level': 'Designated Year Level'}


# staff profile form for admin
class StaffProfileAdminForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        exclude = ['user', ]


# student personal profile form
class StudentPersonalProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        exclude = ['level_and_section', 'user']
        labels = {
            'guardian_contact_number': 'Guardian\'s Contact Number',
        }


# faculty personal profile form
class FacultyPersonalProfileForm(forms.ModelForm):
    class Meta:
        model = FacultyProfile
        exclude = ['user', 'designated_year_level']
        labels = {
            'school_graduated': 'School Graduated',
            'major': 'Course Major'
        }


# staff personal profile form
class StaffPersonalProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        exclude = ['user', ]
        labels = {}


# for administrator/staff only
class LevelAndSectionForm(forms.ModelForm):
    class Meta:
        model = LevelAndSection
        fields = ['level', 'section', 'adviser']


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        exclude = ['date_created', 'updated']
