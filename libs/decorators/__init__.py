# from flask import Flask, request, jsonify, redirect, url_for

# from functools import wraps

# from libs import tokenize



# def authentication_required(f):
#   @wraps(f)
#   def decorated(*args, **kwargs):
#     if "Authorization" in request.headers:
#       token = request.headers.get("Authorization")
#       if token is None:
#         return jsonify(
#           message="Authorization Header missing. Could not validate user",
#           status=False
#           )
#       payload = tokenize.getPayload(token)
#       if payload is None:
#         return jsonify(
#           message="Invalid token request, refresh the token", 
#           status=False
#           )

#       kwargs['payload'] = payload

#     else:
#       return redirect(url_for('loginUser'))

#     r = f(*args, **kwargs)

#     return r

#   return decorated