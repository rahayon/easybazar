from django import forms

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(initial=1, label='')
    update_quantity = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput)


# class WishListAddForm(forms.Form):
#     quantity = forms.IntegerField(initial=1, label='',widget=forms.HiddenInput)
#     update_quantity = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput)
