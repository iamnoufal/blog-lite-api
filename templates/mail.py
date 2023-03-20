from flask import render_template

def createAccount(user):
  body = """
    <h3>Welcome {{ user.name }}!</h3>
    <p>Hope you are having a good time</p>
    <p>Please click the below link to verify your account</p>
    <a href="http://127.0.0.1:8000/verify/{{ user.fs_uniquifier }}">http://127.0.0.1:8000/verify/{{ user.verifyLink }}</a>
    <i>With Regards,</i>
    <i>BlogLite team</i>
  """
  resp = render_template(body, user = user)
  return resp