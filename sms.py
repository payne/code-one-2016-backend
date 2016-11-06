from flask import Flask, request, redirect
import requests
import twilio.twiml
import cPickle as pickle
from chore_state import Chore_Status_Stack

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def reply_payment():
    """Respond and greet the caller by name."""

    url = 'http://hack.nullify.online/update/chore/status/complete'
    message_body = request.values.get('Body', None)

    if "Approve" or "Approve" in message_body:
         # Save and update the chore status
        with open('chore_state.p', 'rb') as pickle_file:
            status_stack = pickle.load(pickle_file)

        chore_vars = status_stack.pop()

        with open('chore_state.p', 'wb') as pickle_file:
            pickle.dump(status_stack, pickle_file)

        chore_vars["status"] = "completed"
        payload = {"username": chore_vars["username"], "title": chore_vars["title"], "status": chore_vars["status"]}
        r = requests.post(url, json=payload)
        print r.text

        reply_message = "Thank you for using First National Bank your the chore payment for %s completing the chore %s has has been approved and the funds have been successfully transfered." % (chore_vars["username"].title(), chore_vars["title"])

    elif "Deny" or "deny" in message_body:
        # Save and update the chore status
        with open('chore_state.p', 'rb') as pickle_file:
            status_stack = pickle.load(pickle_file)

        chore_vars = status_stack.pop()

        with open('chore_state.p', 'wb') as pickle_file:
            pickle.dump(status_stack, pickle_file)

        chore_vars["status"] = "not-completed"
        payload = {"username": chore_vars["username"], "title": chore_vars["title"], "status": chore_vars["status"]}
        r = requests.post(url, json=payload)
        print r.text

        reply_message = "Thank you for using First National Bank your chore payment for %s completing the chore %s has been denied and no funds have been transfered." % (chore_vars["username"].title(), chore_vars["title"])
    else:
        # Save and update the chore status
        with open('chore_state.p', 'rb') as pickle_file:
            status_stack = pickle.load(pickle_file)

        chore_vars = status_stack.pop()
        status_stack.push(chore_vars)

        with open('chore_state.p', 'wb') as pickle_file:
            pickle.dump(status_stack, pickle_file)

        reply_message = "I am sorry I did not understand your response. Please reply Approve or Deny the requested payment for %s completing the chore %s." % (chore_vars["username"].title(), chore_vars["title"])
    resp = twilio.twiml.Response()
    resp.message(reply_message)

    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)