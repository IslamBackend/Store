from django import forms

from book.models import Category, Product


class ProductCreateForm(forms.Form):
    title = forms.CharField(max_length=100)
    price = forms.FloatField()
    rate = forms.FloatField()
    description = forms.CharField(widget=forms.Textarea())
    image = forms.ImageField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects)

    def __str__(self):
        return self.title


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('title',)

    def __str__(self):
        return self.title


class CommentCreateForm(forms.Form):
    name = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea())

    def __str__(self):
        return self.name


class ProductCreateForm2(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
