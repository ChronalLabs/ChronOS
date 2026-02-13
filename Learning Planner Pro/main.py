import os.path
from logic import bundled_credentials_path, working_token_path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# If modifying these scopes, delete the file token.json.
# The scope defines the level of access to the user's calendar.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def authentication():
  """
  Main function which handles the authentication and authorization process for the Google Calendar API.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(working_token_path):
    creds = Credentials.from_authorized_user_file(working_token_path, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          bundled_credentials_path, SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(working_token_path, "w") as token:
      token.write(creds.to_json())

  return creds

if __name__ == "__main__":
  authentication()