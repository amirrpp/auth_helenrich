from django import forms
from django.core.mail import send_mail
from webshop.models import ProductRating, Product
from webrating.models import Rating


class FormFeedback(forms.Form):
    user_name = forms.CharField(label='Name', max_length=100, error_messages={'required': 'Error. Name'})
    user_email = forms.CharField(label='E-mail', max_length=100, required=False)
    user_phone = forms.CharField(label='Phone', max_length=13,
                                 error_messages={'required': 'Error. Phone'})
    user_message = forms.CharField(label='Message', max_length=255, widget=forms.Textarea, required=False)

    @staticmethod
    def process(request):
        form_feedback = FormFeedback(request.POST or None)
        if request.POST and form_feedback.is_valid():
            subject = "oknaeuro.kiev.ua"
            user_name = form_feedback.cleaned_data['user_name']
            user_email = form_feedback.cleaned_data['user_email']
            user_phone = form_feedback.cleaned_data['user_phone']
            user_message = form_feedback.cleaned_data['user_message']
            message = user_name + '\n' + user_phone + '\n' + user_message + '\n' + user_email
            recipients = ['steffan.psi@gmail.com']
            send_mail(subject, message, 'TEST !!!', recipients)
            print(request)
            return True, form_feedback
        else:
            return False, form_feedback


class FormRatingGlobal(forms.Form):
    user_name = forms.CharField(label='Name', max_length=100, error_messages={'required': 'Error. Name'})
    user_email = forms.CharField(label='E-mail', max_length=100, required=False)
    user_rating = forms.FloatField(label='Rating', error_messages={'required': 'Error. Phone'})
    user_message = forms.CharField(label='Message', max_length=255, widget=forms.Textarea, required=True,
                                   error_messages={'required': 'Error. Message'})

    @staticmethod
    def process(request):
        if request.POST:
            form_rating = FormRatingGlobal(request.POST or None)
            if request.POST and form_rating.is_valid():
                user_name = form_rating.cleaned_data['user_name']
                user_email = form_rating.cleaned_data['user_email']
                user_rating = form_rating.cleaned_data['user_rating']
                user_message = form_rating.cleaned_data['user_message']
                rating = Rating()
                rating.user_name = user_name
                rating.rating = user_rating
                rating.comment = user_message
                rating.email = user_email
                rating.save()

                subject = "test"
                message = user_name + '\n' + user_rating.__str__() + '\n' + user_message + '\n' + user_email
                recipients = ['deniszorinets@gmail.com']
                # send_mail(subject, message, 'TEST !!!', recipients)
                return True, form_rating
            else:
                return False, form_rating


class FormRating(forms.Form):
    user_name = forms.CharField(label='Name', max_length=100, error_messages={'required': 'Error. Name'})
    product_id = forms.FloatField(widget=forms.HiddenInput())
    user_email = forms.CharField(label='E-mail', max_length=100, required=False)
    user_rating = forms.FloatField(label='Rating', error_messages={'required': 'Error. Phone'})
    user_message = forms.CharField(label='Message', max_length=255, widget=forms.Textarea, required=True,
                                   error_messages={'required': 'Error. Message'})

    @staticmethod
    def process(request):
        if request.POST:
            form_rating = FormRating(request.POST or None)
            if request.POST and form_rating.is_valid():
                user_name = form_rating.cleaned_data['user_name']
                user_email = form_rating.cleaned_data['user_email']
                user_rating = form_rating.cleaned_data['user_rating']
                user_message = form_rating.cleaned_data['user_message']
                rating = ProductRating()
                rating.user_name = user_name
                rating.rating = user_rating
                rating.product = Product.objects.filter(id=form_rating.cleaned_data['product_id']).first()
                rating.comment = user_message
                rating.email = user_email
                rating.save()

                subject = "test"
                message = user_name + '\n' + user_rating.__str__() + '\n' + user_message + '\n' + user_email
                recipients = ['deniszorinets@gmail.com']
                # send_mail(subject, message, 'TEST !!!', recipients)
                return True, form_rating
            else:
                return False, form_rating

