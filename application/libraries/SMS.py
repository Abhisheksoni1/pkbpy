from urllib.parse import urlencode
from urllib.request import Request, urlopen


class SendSms:
    API_KEY = 'JdZnXhVsBAk-hgstgiWAUINOSIm8ey3DtVVcW4oBHP'

    def send_otp(self, number, otp):
        # Data for text message. This is the text message data.

        sender = "PETUKI";  # This is who the message appears to be from.

        numbers = "91" + str(number)  # A single number or a comma-separated list of numbers

        message = "Use this " + str(otp) + " code as your login One Time Password (OTP)."

        data = urlencode({'apikey': SendSms.API_KEY, 'numbers': numbers, 'message': message, 'sender': sender})
        data = data.encode('utf-8')
        request = Request("https://api.textlocal.in/send/?")
        f = urlopen(request, data)
        fr = f.read()
        return (fr)

    def pkb_order_before_confirmation(self, number):
        # Data for text message. This is the text message data.

        sender = "PETUKI"  # This is who the message appears to be from.
        numbers = "91" + str(number)  # A single number or a comma-separated list of numbers
        message = "Thank you for ordering food from Petu ki Biryani. We will notify once your order is confirmed"
        data = urlencode({'apikey': SendSms.API_KEY, 'numbers': numbers, 'message': message, 'sender': sender})
        data = data.encode('utf-8')
        request = Request("https://api.textlocal.in/send/?")
        f = urlopen(request, data)
        fr = f.read()
        return (fr)

    def pkb_order_confirmation(self, number, order_id, estimated_delivery_time=45):
        # Data for text message. This is the text message data.

        sender = "PETUKI"  # This is who the message appears to be from.
        numbers = "91" + str(number)  # A single number or a comma-separated list of numbers

        message = """Thank you for ordering food from Petu ki Biryani. Your order
Id is #""" + str(order_id) + """. Your order is confirmed and will be delivered at your given
address in """ + str(estimated_delivery_time) + """ minutes."""

        data = urlencode({'apikey': SendSms.API_KEY, 'numbers': numbers, 'message': message, 'sender': sender})
        data = data.encode('utf-8')
        request = Request("https://api.textlocal.in/send/?")
        f = urlopen(request, data)
        fr = f.read()
        print(fr)
        return (fr)

    def pkb_order_delivered(self, number, credit_point, total_point):
        sender = "PETUKI"  # This is who the message appears to be from.
        numbers = "91" + str(number)  # A single number or a comma-separated list of numbers.

        message = """Your order is delivered. We have credited """+str(credit_point)+""" points worth INR """+str(credit_point)+""" into your account. Redeem them in your next order. Balance """+str(total_point)+"""."""

        data = urlencode({'apikey': SendSms.API_KEY, 'numbers': numbers, 'message': message, 'sender': sender})
        data = data.encode('utf-8')
        request = Request("https://api.textlocal.in/send/?")
        f = urlopen(request, data)
        fr = f.read()
        print(fr)
        return (fr)

    def pkb_order_canceled(self, number, order_id):
        sender = "PETUKI"  # This is who the message appears to be from.
        numbers = "91" + str(number)  # A single number or a comma-separated list of numbers.
        message = """Your order #"""+str(order_id)+""" is cancelled. The loyalty bonus points will be
credited back to your PKB wallet within 24 hours."""
        data = urlencode({'apikey': SendSms.API_KEY, 'numbers': numbers, 'message': message, 'sender': sender})
        data = data.encode('utf-8')
        request = Request("https://api.textlocal.in/send/?")
        f = urlopen(request, data)
        fr = f.read()
        print(fr)
        return (fr)

