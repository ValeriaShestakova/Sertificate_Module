from django import forms


class SearchForm(forms.Form):
    CHOICES = [('hash', 'Поиск по хеш-коду'),
               ('fullname', 'Поиск по ФИО'), ]
    search_type = forms.ChoiceField(label='Тип поиска', choices=CHOICES, widget=forms.RadioSelect())
    search_str = forms.CharField(label='Введите запрос')
