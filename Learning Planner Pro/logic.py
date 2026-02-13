import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os
import shutil
import sys

# Get the directory where the executable is running
if getattr(sys, 'frozen', False):
    # Running as a bundled app
    base_dir = sys._MEIPASS
else:
    # Running as script
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Path to bundled (read-only) json files
bundled_checkbox__path = os.path.join(base_dir, 'checkbox_states.json')
bundled_reminder__path = os.path.join(base_dir, 'reminder.json')
bundled_credentials_path = os.path.join(base_dir, 'credentials.json')

# Path to working (writable) json files in App Data
if getattr(sys, 'frozen', False):
    if os.name == "nt":
        working_dir = os.path.join(os.getenv('APPDATA'), 'StudentPlanner')
    elif os.name == "posix":
        working_dir = os.path.join(os.path.expanduser('~/Library/Application Support'), 'StudentPlanner')
        
    os.makedirs(working_dir, exist_ok=True)
else:
    working_dir = os.path.dirname(os.path.abspath(__file__))

working_checkbox_path = os.path.join(working_dir, 'checkbox_states.json')
working_reminder_path = os.path.join(working_dir, 'reminder.json')
working_modules_path = os.path.join(working_dir, 'modules.json')
working_token_path = os.path.join(working_dir, 'token.json')

# If working jsons doesn't exist, copy from bundled json files
if not os.path.exists(working_checkbox_path):
    try: shutil.copyfile(bundled_checkbox__path, working_checkbox_path)
    except: pass

if not os.path.exists(working_reminder_path):
    try: shutil.copyfile(bundled_reminder__path, working_reminder_path)
    except: pass


def file_exists(path):
    return os.path.exists(path)

def get_upcoming_events(creds):
    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone().isoformat()
        tomorrow = ((datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone()) + datetime.timedelta(days=1)).isoformat()
        
        events_result = (
         service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                q="task",
                timeMax=tomorrow,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return [] # Changed from returning list with string to empty list for easier handling

        results = []
        for event in events:
            results.append((event["id"], event["summary"], event.get("colorId", "1")))
        
        return results

    except HttpError as error:
        print(f"An error occurred: {error}")
        return []
    
def get_assignments(creds, upcoming):
    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone().isoformat()
        tomorrow = ((datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone()) + datetime.timedelta(days=1)).isoformat()
        
        if upcoming == True:
            events_result = service.events().list(
                calendarId="primary", timeMin=now, q="assignment", timeMax=tomorrow,
                singleEvents=True, orderBy="startTime"
            ).execute()
        else:
            events_result = service.events().list(
                calendarId="primary", q="assignment", maxResults=10, 
                singleEvents=True, orderBy="startTime"
            ).execute()
            
        events = events_result.get("items", [])
        if not events: return []

        results = []
        for event in events:
            results.append((event["id"], event["summary"], event.get("colorId", "1")))
        return results
    except HttpError as error:
        print(f"An error occurred: {error}")
        return []

def retrieve_event_details(creds, task_id):
    try:
        service = build("calendar", "v3", credentials=creds)
        event = service.events().get(calendarId="primary", eventId=task_id).execute()
        return {
            "id": event["id"],
            "summary": event["summary"],
            "colorId": event.get("colorId", "1"),
            "date": event["start"].get("date", event["start"].get("dateTime")[:10] if "dateTime" in event["start"] else ""),
            "start": event["start"].get("dateTime", event["start"].get("date")),
            "end": event["end"].get("dateTime", event["end"].get("date"))
        }
    except Exception as error:
        print(f"Error: {error}")
        return {}

def add_task(creds, title, module, start_time, end_time, date):
    try:
        service = build("calendar", "v3", credentials=creds)
        
        # 1. Initialize default colour (ID 8 is Graphite/Grey)
        colour = "8" 
        
        # 2. Try to match module to colour from JSON
        if os.path.exists(working_modules_path):
            with open(working_modules_path, "r") as f:
                modules = json.load(f)
                if modules.get('10') == module: colour = "10"
                elif modules.get('9') == module: colour = "9"
                elif modules.get('6') == module: colour = "6"
                elif modules.get('8') == module: colour = "8"

        event_body = {
            "summary": f"{title}",
            "description": "task",
            "colorId": colour,
            "start": {
                "dateTime": f"{date}T{start_time[:5]}:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": f"{date}T{end_time[:5]}:00",
                "timeZone": "Europe/London",
            }
        }
        
        service.events().insert(calendarId="primary", body=event_body).execute()
        
    except Exception as error:
        print(f"An error occurred in add_task: {error}")

def edit_task(creds, task_id, title, module, start_time, end_time, date):
    try:
        service = build("calendar", "v3", credentials=creds)
        colour = "8" # Default
        
        if os.path.exists(working_modules_path):
            with open(working_modules_path, "r") as f:
                modules = json.load(f)
                if modules.get('10') == module: colour = "10"
                elif modules.get('9') == module: colour = "9"
                elif modules.get('6') == module: colour = "6"
                elif modules.get('8') == module: colour = "8"

        event_body = {
            "summary": f"{title}",
            "description": "task",
            "colorId": colour,
            "start": {
                "dateTime": f"{date}T{start_time[:5]}:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": f"{date}T{end_time[:5]}:00",
                "timeZone": "Europe/London",
            }
        }
        service.events().patch(calendarId="primary", eventId=task_id, body=event_body).execute()
    except Exception as error:
        print(f"An error occurred in edit_task: {error}")

def delete_task(creds, task_id):
    try:
        service = build("calendar", "v3", credentials=creds)
        service.events().delete(calendarId="primary", eventId=task_id).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")

def add_assignment(creds, title, module, due_date, due_time):
    try:
        service = build("calendar", "v3", credentials=creds)
        colour = "8" # Default
        
        if os.path.exists(working_modules_path):
            with open(working_modules_path, "r") as f:
                modules = json.load(f)
                if modules.get('10') == module: colour = "10"
                elif modules.get('9') == module: colour = "9"
                elif modules.get('6') == module: colour = "6"
                elif modules.get('8') == module: colour = "8"

        event_body = {
            "summary": f"{title}",
            "description": "assignment",
            "colorId": colour,
            "start": {
                "dateTime": f"{due_date}T{due_time[:5]}:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": f"{due_date}T{due_time[:5]}:01",
                "timeZone": "Europe/London",
            }
        }
        service.events().insert(calendarId="primary", body=event_body).execute()
    except Exception as error:
        print(f"An error occurred in add_assignment: {error}")

def edit_assignment(creds, assignment_id, title, module, due_date, due_time):
    try:
        service = build("calendar", "v3", credentials=creds)
        colour = "8"
        
        if os.path.exists(working_modules_path):
            with open(working_modules_path, "r") as f:
                modules = json.load(f)
                if modules.get('10') == module: colour = "10"
                elif modules.get('9') == module: colour = "9"
                elif modules.get('6') == module: colour = "6"
                elif modules.get('8') == module: colour = "8"

        event_body = {
            "summary": f"{title}",
            "description": "assignment",
            "colorId": colour,
            "start": {
                "dateTime": f"{due_date}T{due_time[:5]}:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": f"{due_date}T{due_time[:5]}:01",
                "timeZone": "Europe/London",
            }
        }
        service.events().patch(calendarId="primary", eventId=assignment_id, body=event_body).execute()
    except Exception as error:
        print(f"An error: {error}")

def add_modules(module_1, module_2, module_3):
    dictionary = {
        "10" : f"{module_1}",
        "9" : f"{module_2}",
        "6" : f"{module_3}",
        "8" : "General"
    }
    with open(working_modules_path, "w") as outfile:
        json.dump(dictionary, outfile, indent=4)

def save_reminder_state(reminded, date):
    dictionary ={
        "reminded": f"{reminded}",
        "date": f"{date}"
    }
    with open(working_reminder_path, "w") as outfile:
        json.dump(dictionary, outfile, indent=4)