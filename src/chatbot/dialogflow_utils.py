import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument
from functools import wraps
from flask import Blueprint, request, make_response, abort
import config


class DialogflowClient:
    def __init__(self, project_id, session_id, language='en'):
        self.DIALOGFLOW_PROJECT_ID = project_id
        self.DIALOGFLOW_LANGUAGE_CODE = language
        self.SESSION_ID = session_id
        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(
            self.DIALOGFLOW_PROJECT_ID, self.SESSION_ID)

    def query(self, queryText):
        text_input = dialogflow.types.TextInput(
            text=queryText, language_code=self.DIALOGFLOW_LANGUAGE_CODE)
        query_input = dialogflow.types.QueryInput(text=text_input)
        try:
            response = self.session_client.detect_intent(
                session=self.session, query_input=query_input)
        except InvalidArgument as e:
            response = {"error": str(e)}
        return response


class DialogflowResponse:
    def __init__(self, response):
        self.response_object = response
        self.queryText = response.query_result.query_text
        self.detectedIntent = response.query_result.intent.display_name
        self.detectedIntentConfidence = response.query_result.intent_detection_confidence
        try:
            self.fulfillmentText = str(response.query_result.fulfillment_messages[0].text.text[0])
        except Exception as e:
            self.fulfillmentText = ''

class WebhookRequest:
    def __init__(self, data):
        self.parameters = data["queryResult"]["parameters"]
        self.user_id = data['session'].split('/')[-1]
        self.query_text = data['queryResult']['queryText']
        self.intent = data['queryResult']['intent']['displayName']


def auth_webhook(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if request.headers.get('AUTH') == config.DIALOG_FLOW_AUTH:
            return f(*args, **kwargs)
        else:
            abort(403)
    return wrapper
