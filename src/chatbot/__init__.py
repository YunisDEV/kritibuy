from flask import Blueprint, request, make_response, abort
import config
from functools import wraps
import json
from .dialogflow_client import DialogflowClient, DialogflowResponse, WebhookRequest
from ..account.security import authorize
from ..db import session, Message, Order, OrderInfo, User


chatbot = Blueprint('chatbot', __name__)


def auth_webhook(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.headers.get('AUTH') == config.DIALOG_FLOW_AUTH:
            return f(*args, **kwargs)
        else:
            abort(403)
    return wrapper


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
    try:
        data = WebhookRequest(json.loads(request.data))
        print(
            f'Ordering: {data.parameters.get("products")} ---> {data.parameters.get("companies")} by {data.user_id}'
        )
        user = session.query(User).filter(User.id == data.user_id).one()
        order = Order(
            orderedTo=session.query(User).filter(
                User.brandName == data.parameters.get("companies")).one().id,
            orderedBy=user.id,
            orderedProduct=data.parameters.get("products"),
            orderText=data.query_text
        )
        session.add(order)
        session.commit()
        response = 'Ordered Successfully'

        return make_response({
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            response
                        ]
                    }
                }
            ]
        })
    except Exception as e:
        print(e)
        response = 'Error occured on server'
        return make_response({
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            response
                        ]
                    }
                }
            ]
        })


exampleRespone = {
    'responseId': '8c47ff35-65d6-454c-b393-f61794d59f6d-fddac391',
    'queryResult': {
        'queryText': 'Order web application from Pragmatech',
        'parameters': {
            'products': 'web',
            'companies': 'Pragmatech'
        },
        'allRequiredParamsPresent': True,
        'outputContexts': [
            {
                'name': 'projects/kritibuy-mbhb/agent/sessions/4cf16b0a-295a-c1eb-f889-2998111bbfe4/contexts/__system_counters__',
                'parameters': {
                    'no-input': 0.0,
                    'no-match': 0.0,
                    'products': 'web',
                    'products.original': 'web application',
                    'companies': 'Pragmatech',
                    'companies.original': 'Pragmatech'
                }
            }
        ],
        'intent': {
            'name': 'projects/kritibuy-mbhb/agent/intents/bae01e57-0c0a-4aec-9042-c651ea8c0cd4',
            'displayName': 'OrderLongTime'
        },
        'intentDetectionConfidence': 1.0,
        'languageCode': 'en'
    },
    'originalDetectIntentRequest': {
        'source': 'DIALOGFLOW_CONSOLE',
        'payload': {}
    },
    'session': 'projects/kritibuy-mbhb/agent/sessions/4cf16b0a-295a-c1eb-f889-2998111bbfe4'
}
