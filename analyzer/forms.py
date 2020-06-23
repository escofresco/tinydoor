from django.forms import Form
from .models import Analysis


class EmptyForm(Form):
    pass

class AnalysisForm(forms.ModelForm):
    '''A form based on the Analysis model.'''
    class Meta:
        model = Analysis
        fields = [
            'store_title',
            'image',
        ]