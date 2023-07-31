from django import forms

from blog.models import Blog


class AddBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'image', 'is_published')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["content"].widget.attrs.update({"class": "form-control", 'style': "height: 150px"})
        self.fields["image"].widget.attrs.update({"class": "form-control"})
        self.fields["is_published"].widget.attrs.update({"class": "form-check-input"})


class UpdateBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'image', 'is_published')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["content"].widget.attrs.update({"class": "form-control", 'style': "height: 150px"})
        self.fields["is_published"].widget.attrs.update({"class": "form-check-input"})

