from django import forms

from .models import Bidding, Listing, Comment, Bidding

CATEGORIES = (
    ('Art', 'Art'),
    ('Automotive & Powersports', 'Automotive & Powersports'),
    ('Beauty', 'Beauty'),
    ('Books', 'Books'),
    ('Electronics', 'Electronics'),
    ('Musical instruments', 'Musical instruments'),
    ('Pet Supplies', 'Pet Supplies'),
    ('Software', 'Software'),
    ('Sports', 'Sports'),
    ('Tools', 'Tools'),
    ('Toys & Games', 'Toys & Games'),
    ('Watches', 'Watches'),
    ('Other', 'Other'),
)

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = [
            'title',
            'description',
            'category',
            'image',
            'starting_bid'
        ]
        widgets ={
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'height: 30px; width: 30%'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 150px; width: 30%',
            }),

            'category': forms.Select(attrs={
                'class': 'form-control',
                'style': 'height: 35px; width: 30%'
            }),

            'starting_bid': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'height: 30px; width: 15%'
            }),

            'image': forms.FileInput(attrs={
                'class': 'input-group',
                'style': 'height: 30px; width: 30%'
            })

        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'comment'
        ]
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'style': 'height: 70px; width: 30%'
            })
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bidding
        fields = [
            'amount'
        ]
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'style': 'height: 30px; width: auto'
            })
        }
