from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    id = forms.IntegerField(required=False)
    firstName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Employee
        fields = ['firstName', 'lastName', 'email', 'age', 'id']

    def clean(self):
        cleaned_data = super(EmployeeForm, self).clean()
        email = cleaned_data.get('email', None)
        id = cleaned_data.get('id', None)
        if not email:
            return cleaned_data
        check_ip_exist = Employee.objects.filter(email=email, is_active=1)
        if id:
            check_ip_exist = Employee.objects.filter(email=email, is_active=1).exclude(id=id)
            if check_ip_exist:
                raise forms.ValidationError('Entered Email field is already exist!')
        else:
            if check_ip_exist:
                raise forms.ValidationError('Entered Email field is already exist!')
        return cleaned_data