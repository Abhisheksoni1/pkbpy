

def get_owner_registration_verify_content(request ,data):
    content = """<html>
                <head>
                <title>Fildum Merchent Registrations </title>
                </head>
                <body>
                <p>Dear """ + data.get('first_name') + """ """ + data.get('last_name') + """,</p>

                You have recently registered with Fildum as Merchent. Before proceeding further,we would like to verify your email address, as your privacy is our top priority. This will also help us <br>
                to keep you updated on exciting news and opportunities.<br><br>
                <p>Your Credential are below:</p>
                <p>User Name: """ + data.get('user_name') + """ </p>
                <p>Password: """ + data.get('password') + """ </p>
                Before login please <a href=""" + data.get('link') + """>click here</a> to verify your email address you have registered with us.<br>

                <p>Please Note: For security purposes, this link will expire after you have used it once. For any more query or issue with resetting your password, you can get in touch with us at pkb2019@gmail.com</p>

                <p>Regards<br>
                Fildum Team</p>
                </body>
                </html>"""
    return content


def get_user_registeration_verify_content(request, data):
    content = """<html>
                    <head>
                    <title>Fildum Merchent Registrations </title>
                    </head>
                    <body>
                    <p>Dear """ + data.get('first_name') + """ """ + data.get('last_name') + """,</p>

                    Kindly use below link to set new password.<br>
                    <a href=""" + data.get('link') + """>click here</a> to reset the password.<br>

                    <p>Please Note: For security purposes, this link will expire after you have used it once. For any more query or issue with resetting your password, you can get in touch with us at pkb2019@gmail.com</p>

                    <p>Regards<br>
                    Fildum Team</p>
                    </body>
                    </html>"""
    return content


def get_user_password_confirmation(request, data):
    content = """<html>
                    <head>
                    <title>Fildum Merchent Registrations </title>
                    </head>
                    <body>
                    <p>Dear """ + data.first_name + """ """ + data.last_name + """,</p>

                    Your Password is reset successfully.

                    <p> For any more query or issue with resetting your password, you can get in touch with us at pkb2019@gmail.com</p>

                    <p>Regards<br>
                    Fildum Team</p>
                    </body>
                    </html>"""
    return content





def get_manager_registration_verify_content(data):
    content = """<html>
                <head>
                <title>Fildum Store Manager Registrations </title>
                </head>
                <body>
                <p>Dear """ + data.get('first_name') + """ """ + data.get('last_name') + """,</p>

                You have recently registered with Fildum as Merchent. Before proceeding further,we would like to verify your email address, as your privacy is our top priority. This will also help us <br>
                to keep you updated on exciting news and opportunities.<br><br>
                <p>Your Credential are below:</p>
                <p>User Name: """ + data.get('user_name') + """ </p>
                <p>Password: """ + data.get('password') + """ </p>
                Before login please <a href=""" + data.get('link') + """>click here</a> to verify your email address you have registered with us.<br>

                <p>Please Note: For security purposes, this link will expire after you have used it once. For any more query or issue with resetting your password, you can get in touch with us at pkb2019@gmail.com</p>

                <p>Regards<br>
                Fildum Team</p>
                </body>
                </html>"""
    return content

