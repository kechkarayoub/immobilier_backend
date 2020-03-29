from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import ugettext as _
import random


def send_email(subject, text_content, from_address, to_address, html_content=None):
    if to_address == "kechkarayoub@gmail.com":
        print('in send email task')
    msg = EmailMultiAlternatives(_(subject), text_content, from_address, [to_address])
    if html_content:
        msg.attach_alternative(html_content, "text/html")
    try:
        if to_address == "kechkarayoub@gmail.com":
            print('try send email')
        msg.send()
        if to_address == "kechkarayoub@gmail.com":
            print('email sent')
    except Exception as e:
        if to_address == "kechkarayoub@gmail.com":
            print('error')
            print(repr(e))
            # for just the message, or str(e), since print calls str under the hood
            print(e)
            # the arguments that the exception has been called with.
            # the first one is usually the message. (OSError is different, though)
            print(e.args)
        pass


def generate_random_color(with_complementary=False):
    random_color = '#%02X%02X%02X' % (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    if with_complementary:
        return random_color, get_complementary_color(random_color)
    return random_color


def get_complementary_color(hex_color):
    # strip the # from the beginning
    color = hex_color[1:]
    # convert the string into hex
    color = int(color, 16)
    # invert the three bytes
    # as good as substracting each of RGB component by 255(FF)
    complementary_color = 0xFFFFFF ^ color
    # convert the color back to hex by prefixing a #
    complementary_color = "#%06X" % complementary_color
    return complementary_color


def choices_format_to_tuple(choices):
    return tuple((choice[0], _(choice[1])) for choice in choices)


def choices_format_to_dict(choices):
    return {choice[0]: _(choice[1]) for choice in choices}


def generate_id(last_id=None):
    if not last_id:
        return "AEXXXXXXXX1"
    last_id = last_id.replace("AE", "").replace("X", "")
    last_id = int(last_id) + 1
    last_id = str(last_id)
    if len(last_id) >= 9:
        new_id = "AE" + last_id
    else:
        new_id = "AE" + ("X"*(9 - len(last_id) % 9)) + last_id
    return new_id


def get_list_social_links_images():
    return {
        "facebook": settings.BACKEND_URL_ROOT + static("contact/images/facebook.png"),
        "google-plus": settings.BACKEND_URL_ROOT + static("contact/images/gplus.png"),
        "instagram": settings.BACKEND_URL_ROOT + static("contact/images/instagram.png"),
        "linkedin": settings.BACKEND_URL_ROOT + static("contact/images/linkedin.png"),
        "twitter": settings.BACKEND_URL_ROOT + static("contact/images/twitter.png"),
        "youtube": settings.BACKEND_URL_ROOT + static("contact/images/youtube.png"),
    }


def is_email_valid(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
