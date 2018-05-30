from django import forms


class SearchForm(forms.Form):
    CHOICES = [('hash', 'Поиск хеш-коду'),
               ('fullname', 'Поиск по ФИО'),
               ('certificate_num', 'Поиск по номеру свидетельства'), ]
    search_type = forms.ChoiceField(label='Тип поиска', choices=CHOICES, widget=forms.RadioSelect())
    search_str = forms.CharField(label='Введите запрос')
