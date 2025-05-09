import json
import logging
import typing
from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen


logger = logging.getLogger("coderedcms")


class RecaptchaResponse(typing.NamedTuple):
    success: typing.Union[bool, None]
    score: float
    error_codes: typing.List[str]
    original_data: typing.Dict[str, typing.Any]


def verify_response(recaptcha_response: str, secret_key: str, remoteip: str):
    """
    Verifies a response from reCAPTCHA front-end.

    * recaptcha_response = The token from the front-end, typically
      ``g-recaptcha-response`` in POST parameters.

    * secret_key = reCAPTCHA secret/private API key.

    * remoteip = The form submitter's IP address.
    """
    params = {
        "secret": secret_key,
        "response": recaptcha_response,
        "remoteip": remoteip,
    }
    request = Request(
        url="https://www.google.com/recaptcha/api/siteverify",
        method="POST",
        data=bytes(urlencode(params), encoding="utf8"),
        headers={
            "Content-type": "application/x-www-form-urlencoded",
        },
    )
    response = urlopen(request)
    data = json.loads(response.read().decode("utf8"))
    response.close()
    # Default to sentinel values if not provided by Google.
    rr = RecaptchaResponse(
        success=data.get("success", None),
        score=data.get("score", -1.0),
        error_codes=data.get("error-codes", []),
        original_data=data,
    )
    logger.info(f"reCAPTCHA response: {rr}")
    return rr
