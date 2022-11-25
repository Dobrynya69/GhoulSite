from django import forms

SORT_CHOICES =(
    ('first_name', 'Name↓'),
    ('-first_name', 'Name↑'), 
    ('zxc_level', 'Level↓'), 
    ('-zxc_level', 'Level↑')
)

class FindUserForm(forms.Form):
    name = forms.CharField(max_length=25, label="", widget=forms.TextInput(attrs={'placeholder':'Enter name'}), required=False)
    order = forms.ChoiceField(choices=SORT_CHOICES,  label="", required=True)
