from flask import Blueprint, request, make_response, abort
import config
from functools import wraps
import json
from .dialogflow_utils import DialogflowClient, DialogflowResponse, WebhookRequest, auth_webhook
from ..account.security import authorize
from ..db import session, Message, Order,  User, ServerError, Permission
from .utils import getCompany

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
    try:
        data = WebhookRequest(json.loads(request.data))
        print(
            f'Ordering: {data.parameters.get("product")} ---> {data.parameters.get("company")} by {data.user_id}'
        )
        try:
            user = session.query(User).filter(
                User.id == int(data.user_id)).one()
            if not user:
                raise Exception()
        except Exception as e:
            raise Exception('User not found with id: '+data.user_id, 15)
        try:
            company = getCompany(data.parameters.get("company"))
        except Exception as e:
            print('Errorr'+str(e))
            raise Exception('Company not found with brandName: ' +
                            data.parameters.get("company"), 12)
        try:
            if not data.parameters.get("product") in company.brandProductTypes:
                raise Exception()
        except Exception as e:
            raise Exception('Company is not serving such product', 19)
        try:
            order = Order(
                orderedTo=company.id,
                orderedBy=user.id,
                orderedProduct=data.parameters.get("product"),
                orderText=data.query_text
            )
            session.add(order)
            session.commit()
        except Exception as e:
            raise Exception('Order can not be created', 18)

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
        e = tuple(e.args)
        print(e)
        error = ServerError(
            where='Webhook',
            errorCode=e[1],
            errorDesc=e[0],
        )
        session.add(error)
        session.commit()
        response = error.errorDesc+'. Error ID: ' + str(error.id)
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
