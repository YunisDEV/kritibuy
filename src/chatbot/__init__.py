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


# Order handling
@chatbot.route('/webhook', methods=['POST', 'GET'])
@auth_webhook
def webhook_main():
    if request.method == 'GET':
        return make_response({"api_version": 1})
    data = WebhookRequest(json.loads(request.data))
    resp = webhook[data.intent](data)
    old = []
    with open('src/chatbot/webhook.debug.json') as f:
        old = json.load(f)
        old.append({'query':data.query_text,'response':resp["fulfillmentMessages"][0]["text"]["text"][0]})
    with open('src/chatbot/webhook.debug.json','w') as f:
        json.dump(old,f)
    return make_response(resp)