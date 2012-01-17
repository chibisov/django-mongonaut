from django import forms

from mongoengine.fields import EmbeddedDocumentField, ListField
from mongonaut.widgets import get_widget

class DocumentListForm(forms.Form):
    """ The main document list form """
    mongo_id = forms.MultipleChoiceField(required=True, widget=forms.CheckboxSelectMultiple)
    

class DocumentDetailForm(forms.Form):
    pass
    
CHECK_ATTRS = dict(
        choices='choices',
        required='required',
        help_text='help_text',
        name='name'
    )


def document_detail_form_munger(form, document_type, document, initial=True):
    """ Adds document field to a form. Not sure what to call this but Factory is not it.
    Handle during GET """    
    for key in sorted(document_type._fields.keys()):
        field = document_type._fields[key]
        print field.__dict__
        print '-------'
        if isinstance(field, EmbeddedDocumentField):            
            continue
        if isinstance(field, ListField):                                
            continue
        form.fields[key] = forms.CharField(
            key, 
            required=field.required,
            widget=get_widget(field))
        if initial:
            form.fields[key].initial = getattr(document, key)            
        
        for field_key, form_attr in CHECK_ATTRS.items():
            if hasattr(field, field_key):
                value = getattr(field, field_key)
                setattr(form.fields[key], field_key, value)
    return form


