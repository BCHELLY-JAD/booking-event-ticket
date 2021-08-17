from django import forms

class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%Y/%m/%d %H:%M'],widget=forms.TextInput(attrs={'id':'id_date'}))

class CommentForm(forms.Form): 
    text = forms.CharField(max_length=200, 
        widget=forms.TextInput( 
            attrs={'class' : 'form-control', 'placeholder' : 'add a comment', 'name' : 'description', 'id' : 'type'}))
     