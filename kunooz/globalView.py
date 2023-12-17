from rest_framework.views import exception_handler
from rest_framework.renderers import JSONRenderer

def custom_exception_handler(exc, context):
  # Call REST framework's default exception handler first,
  # to get the standard error response.
  response = exception_handler(exc, context)
  print("#"*92,response.data)
  # Now add the HTTP status code to the response.
  if response is not None:

    errors = []
    try:
        message = response.data.get('detail')
    except: # for djoser error that doesnt contain .get
        message = response.data[0]
    if not message:
        for field, value in response.data.items():
            errors.append("{} : {}".format(field, " ".join(value)))
        response.data = { 'errors': errors}
    else:
        response.data = {'errors': [message]}
  return response

class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
          "status": "success",
          "code": status_code,
          "data": data,
          "messages": None
        }
        if status_code == 204:
            renderer_context['response'].status_code = 200
            response["status"] = "success"

        if not str(status_code).startswith('2'):
            response["status"] = "error"
            response["data"] = None
            try:
                if data["detail"]:
                    response["messages"] = data["detail"]
            except :
                response["messages"] = data

        return super(CustomRenderer, self).render(response, accepted_media_type, renderer_context)