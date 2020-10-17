import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument


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
        self.fulfillmentText = response.query_result.fulfillment_messages[0].text.text[0]
