from pyfcm import FCMNotification


# server_key = 'AAAAeRxTIbQ:APA91bHUtDQ9XqAdlNMHNZ1hr62yDv9BATA7EZT3DhLT14C5sIgAWcEntjPsdmkcEPhqFDPOmSwJW3KM1oPBLXRLYiFwoU_lbnhN_aGXOcPeV2pj-2ny37R53Cnl4_60-Bm83r8cbso6'
server_key = 'AAAAeRxTIbQ:APA91bHUtDQ9XqAdlNMHNZ1hr62yDv9BATA7EZT3DhLT14C5sIgAWcEntjPsdmkcEPhqFDPOmSwJW3KM1oPBLXRLYiFwoU_lbnhN_aGXOcPeV2pj-2ny37R53Cnl4_60-Bm83r8cbso6'

push_service = FCMNotification(api_key=server_key)


def Order_notification(device_token, order_no):

    message_title = "Order Placed"
    message_body = "Your Order no #{} successfully Placed".format(order_no)

    result = push_service.notify_single_device(registration_id=device_token, message_title=message_title,
                                               message_body=message_body)
    return result


def Register_notification(device_token):
    message_title = "Log-in successful"
    message_body = 'You are successfully logged-in with PKB.Thank you.'

    result = push_service.notify_single_device(registration_id=device_token, message_title=message_title,
                                               message_body=message_body)
    return result


def notifications(device_token,message):
    result = push_service.notify_single_device(registration_id=device_token,
                                               message_body=message)
    return result
