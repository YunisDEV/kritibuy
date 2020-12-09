from flask import Blueprint, request, make_response
import json
from .dialogflow_utils import DialogflowClient, DialogflowResponse, WebhookRequest, auth_webhook
from ..account.security import authorize
from ..db import session, Message
from .webhook import webhook


chatbot = Blueprint('chatbot', __name__)


@chatbot.route('/query', methods=['POST'])
@authorize('Personal')
def chatbot_query(user):
    try:
        data = json.loads(request.data)
        cli = DialogflowClient(
            project_id='kritibuy-mbhb',
            session_id=user.id,
            language='en'
        )
        response = cli.query(data["queryText"])
        response = DialogflowResponse(response)
        session.add_all([
            Message(
                user=user.id,
                type='me',
                message=data["queryText"]
            ),
            Message(
                user=user.id,
                type='you',
                message=response.fulfillmentText
            )
        ])
        session.commit()
        return {"response": response.fulfillmentText}
    except Exception as e:
        print(e)
        return {"response": str(e)}


# Order handling
@chatbot.route('/webhook', methods=['POST', 'GET'])
@auth_webhook
def webhook_main():
    try:
        if request.method == 'GET':
            return make_response({"api_version": 1})
        data = WebhookRequest(json.loads(request.data))
        resp = webhook[data.intent](data)
        print(data)
        return make_response(resp)
    except Exception as e:
        return make_response({
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        "Webhook problem occured. Contact admin of application"
                    ]
                }
            }
        ]
    })