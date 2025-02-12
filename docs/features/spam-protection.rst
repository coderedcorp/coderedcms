Spam Protection
===============

CRX provides features to help block spam form submissions from your site.

These can be toggled in **Settings > CRX Settings > Forms**


Basic (honeypot)
----------------

The default spam protection technique is a simple honeypot. This adds a hidden field to all forms, which some spammers might mistake for a real field. If the hidden field is filled out, the submission is rejected and a generic error message is shown to the user.

While this technique is not the most effective, it can help stop some brute force spammers, and requires no additional setup or 3rd party services.


reCAPTCHA v3 (invisible)
------------------------

Google's reCAPTCHA v3 is invisible, meaning the visitor does not see anything and does not have to solve any challenges. This works by generating a score of how likely the submission is to be spam.

By default, CRX will show a generic error message for scores lower than 0.5. This can be adjusted in **Settings > CRX Settings > Forms**. If your visitors are complaining that they are getting errors when submitting forms, you may want to lower this number. If you are still receiving a lot of spam submissions, you may want to raise it.

**reCAPTCHA v3 requires API keys from Google.** When creating the API keys, you must select recAPTCHA v3, then enter those keys into **Settings > CRX Settings > Forms**.

`Create reCAPTCHA API keys <https://www.google.com/recaptcha/admin/create>`_


reCAPTCHA v2 ("I am not a robot")
---------------------------------

Google's reCAPTCHA v2 shows the famous "I am not a robot" checkbox on the form. This requires the visitor to click the box. In some cases, Google might require the visitor to solve a challenge, such as selecting images or solving a puzzle.

**reCAPTCHA v2 requires API keys from Google.** When creating the API keys, you must select recAPTCHA v2 "I am not a robot", then enter those keys into **Settings > CRX Settings > Forms**.

`Create reCAPTCHA API keys <https://www.google.com/recaptcha/admin/create>`_


Customizing the spam error message
----------------------------------

The spam error message can be customized on a per-page basis by overriding the ``get_spam_message`` function as so:

.. code-block:: python

   class FormPage(CoderedFormPage):
       ...

       def get_spam_message(self) -> str:
           return "Error submitting form. Please try again."

|

.. versionadded:: 5.0

   reCAPTCHA v2 and v3 support was added in CRX 5.0.
