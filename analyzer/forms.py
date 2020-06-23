from django.forms import Form, ModelForm
from .models import Analysis
from django import forms


class EmptyForm(Form):
    pass


"""
class AnalysisForm(ModelForm):
    '''A form based on the Analysis model.'''
    class Meta:
        model = Analysis
        fields = '__all__'
        
"""
class AnalysisForm(Form):
    store_title = forms.CharField(max_length=200)
    image = forms.ImageField()

    widget = {
            'store_title': forms.Select,
            'image': forms.Select,
        }

    def clean(self):
        cleaned_data = super(AnalysisForm, self).clean()
        store_title = cleaned_data.get('store_title')
        image = cleaned_data.get('image')
        if not image:
            raise forms.ValidationError('Please check that you uploaded an image or video.')
"""