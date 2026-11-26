#!/usr/bin/env python3
"""
Create the Research Fair 2027 Gantt database in Notion.

WHY THIS EXISTS
---------------
An AI assistant cannot log into your Notion workspace. This script does the
next best thing: with an integration token YOU create, it builds the whole
schedule in your own workspace in one command.

SETUP (about 5 minutes)
-----------------------
1. pip install notion-client
2. Go to https://www.notion.so/my-integrations -> "New integration"
   - Name it anything, e.g. "Schedule Builder"
   - Type: Internal
   - Capabilities: Insert content + Read content
3. Copy the "Internal Integration Secret" (starts with ntn_)
4. Open THIS page in Notion:
   https://app.notion.com/p/2257338a50b280fa9968e98453518ebd
   -> ... menu (top right) -> Connections -> Connect to -> "Schedule Builder"
   (Without this step every API call returns 404.)
5. Set the token and run:

   Windows PowerShell:
     $env:NOTION_TOKEN="ntn_your_token_here"
     python notion_setup.py

   macOS / Linux:
     export NOTION_TOKEN="ntn_your_token_here"
     python notion_setup.py

6. Open the page. The database "RF2027 — Gantt Schedule" appears as a child.
   Then: open the table -> New view -> Timeline -> "Show timeline by" -> Start,
   and switch on separate start/end properties.

Notes
-----
* Owner is a SELECT, not a PEOPLE property, so the script does not need your
  teammates' Notion user IDs. Convert it later if you prefer.
* The script is idempotent: re-running skips tasks that already exist.
* Tested against Notion-Version 2026-03-11 (databases/data-sources split).
"""

import os
import sys
import time

try:
    from notion_client import Client
    from notion_client.errors import APIResponseError, APIErrorCode
except ImportError:
    sys.exit("Missing dependency. Run:  pip install notion-client")

# ---------------------------------------------------------------- configuration

PARENT_PAGE_ID = "2257338a50b280fa9968e98453518ebd"   # from your Notion URL
DATABASE_TITLE = "RF2027 — Gantt Schedule"
API_VERSION = "2026-03-11"

OWNERS = ["Aaron", "Ellaine", "Jolex", "All"]
PHASES = [
    "0. Compliance", "1. Evidence", "2. Writing",
    "3. Poster", "4. Review", "5. Production", "6. Submission",
]
STATUSES = ["Not started", "In progress", "Blocked", "Done"]

# (id, task, owner, start, end, phase, notes)
TASKS = [
    ("T01", "Registration form + PHP 1,500 team fee", "Jolex", "2026-11-14", "2026-11-17", "0. Compliance", "PHP 500 x 3. Registration and payment both close 5 Dec"),
    ("T02", "Proof of Enrollment x3 students", "Jolex", "2026-11-14", "2026-11-17", "0. Compliance", "Registrar request; allow 1 working day"),
    ("T03", "Adviser's Conforme signed", "Aaron", "2026-11-14", "2026-11-17", "0. Compliance", "Organizer-supplied form"),
    ("T04", "Organizer clarification: AI use, rubric, eligibility", "Aaron", "2026-11-14", "2026-11-17", "0. Compliance", "GATE G0. Decides whether the paper can exist"),
    ("T05", "Principal endorsement letter", "Jolex", "2026-11-14", "2026-11-17", "0. Compliance", "Semi-block; noted-by adviser"),
    ("T06", "Parental consent + DepEd Order 66 Annex C", "Jolex", "2026-11-14", "2026-11-17", "0. Compliance", "Required before any fieldwork"),
    ("T07", "DepEd Advisory 184 s. 2026 attached", "Jolex", "2026-11-14", "2026-11-17", "0. Compliance", "Principals and division offices ask for this"),
    ("T08", "Barangay letters x3 (Barangays 671-687)", "Ellaine", "2026-11-14", "2026-11-17", "0. Compliance", "Send 2 weeks before any visit"),
    ("T09", "Manila City Health Department letter", "Ellaine", "2026-11-14", "2026-11-17", "0. Compliance", "Ask for sanitary inspector to accompany"),
    ("T10", "Manila CENRO / Dept of Public Services letter", "Ellaine", "2026-11-14", "2026-11-17", "0. Compliance", "Septage and environmental records"),
    ("T11", "DENR-EMB NCR FOI request", "Ellaine", "2026-11-14", "2026-11-17", "0. Compliance", "File via foi.gov.ph; 15 working days"),
    ("T12", "Maynilad data request letter", "Ellaine", "2026-11-14", "2026-11-17", "0. Compliance", "Expect a data-sharing agreement; 3-6 weeks"),
    ("T13", "Eligibility check: Grade 7-12 confirmation", "Aaron", "2026-11-14", "2026-11-18", "0. Compliance", "CSC has historically been Grade 7-12 only"),

    ("T14", "G1 site verification walk + centreline", "Aaron", "2026-11-18", "2026-11-21", "1. Evidence", "GATE G1. Everything site-specific depends on this"),
    ("T15", "Access-tier pilot survey (20-30 tanks)", "Ellaine", "2026-11-18", "2026-11-24", "1. Evidence", "Do not open tanks. Exterior observation only"),
    ("T16", "Quotations: lab, hauling, vacuum unit, gate fee", "Ellaine", "2026-11-18", "2026-11-24", "1. Evidence", "Three offers where practicable"),
    ("T17", "Receiving facility capacity + fee confirmation", "Ellaine", "2026-11-18", "2026-11-22", "1. Evidence", "Name the plant and its permit"),
    ("T18", "Reference verification of 24 claims", "Aaron", "2026-11-18", "2026-11-21", "1. Evidence", "Use the source verification annex"),
    ("T19", "Legal routing: permits + employment framework", "Aaron", "2026-11-18", "2026-11-22", "1. Evidence", "RA 9003 / 9275 / 11058 / 10173 check"),

    ("T20", "Paper sections 1-2: Background + Diagnosis", "Aaron", "2026-11-20", "2026-11-23", "2. Writing", "About 600 words"),
    ("T21", "Paper sections 3-4: Barrier + Design", "Aaron", "2026-11-22", "2026-11-25", "2. Writing", "About 550 words. Contains the two-arm test"),
    ("T22", "Paper sections 5-7: Plan + Budget + Economics", "Ellaine", "2026-11-22", "2026-11-25", "2. Writing", "About 500 words"),
    ("T23", "Paper sections 8-9: KPIs + Scaling blueprint", "Jolex", "2026-11-23", "2026-11-26", "2. Writing", "About 350 words"),
    ("T24", "Paper sections 10-11: Implications + Limitations", "Aaron", "2026-11-25", "2026-11-26", "2. Writing", "About 250 words"),
    ("T25", "References in APA 7", "Aaron", "2026-11-25", "2026-11-26", "2. Writing", "Cite Palanca-Tan 2017, not 2015"),
    ("T26", "Word count reconciliation (max 2,200)", "Jolex", "2026-11-26", "2026-11-26", "2. Writing", "Count all non-reference text"),

    ("T27", "Poster content outline", "Jolex", "2026-11-21", "2026-11-23", "3. Poster", "Portrait 3:4"),
    ("T28", "Poster layout and build", "Jolex", "2026-11-24", "2026-11-27", "3. Poster", "Same claims as the paper"),
    ("T29", "Poster-paper content sync", "Jolex", "2026-11-27", "2026-11-29", "3. Poster", "Every number must match"),
    ("T30", "Poster export PNG or JPG", "Jolex", "2026-11-30", "2026-11-30", "3. Poster", "Optional 1800x2400 px"),

    ("T31", "Technical review of paper", "Aaron", "2026-11-27", "2026-11-28", "4. Review", "Independent read"),
    ("T32", "Legal and budget review", "Ellaine", "2026-11-27", "2026-11-28", "4. Review", "Check every peso and every permit"),
    ("T33", "Source and originality review", "Aaron", "2026-11-28", "2026-11-29", "4. Review", "Plagiarism + provenance check"),
    ("T34", "Adviser review and sign-off", "All", "2026-11-29", "2026-11-30", "4. Review", "Book the slot early"),
    ("T35", "Revisions round", "All", "2026-11-30", "2026-12-01", "4. Review", "Fix, do not restyle"),

    ("T36", "Final formatting: TNR 12, Letter, 1in, 1.5", "Jolex", "2026-12-01", "2026-12-02", "5. Production", "Verify in the exported file"),
    ("T37", "AI declaration finalised honestly", "Aaron", "2026-12-01", "2026-12-03", "5. Production", "Cannot be signed before the ruling"),
    ("T38", "Rendered artifact inspection", "All", "2026-12-02", "2026-12-02", "5. Production", "Open the actual PDF and PNG"),
    ("T39", "Content freeze", "All", "2026-12-03", "2026-12-03", "5. Production", "No edits after this date"),

    ("T40", "Submit to rf.ysc@upalchemes.org", "Jolex", "2026-12-04", "2026-12-04", "6. Submission", "Target before 6 PM"),
    ("T41", "Receipt confirmation", "Jolex", "2026-12-04", "2026-12-04", "6. Submission", "Retain the record"),
    ("T42", "Contingency buffer", "All", "2026-12-05", "2026-12-05", "6. Submission", "Hard deadline 11:59 PM PHT"),
]


RETRYABLE = {
    getattr(APIErrorCode, "RateLimited", "rate_limited"),
    getattr(APIErrorCode, "InternalServerError", "internal_server_error"),
    getattr(APIErrorCode, "ConflictError", "conflict_error"),
}


def with_retry(fn, *args, **kwargs):
    """Retry on 429 / 5xx with exponential backoff."""
    for attempt in range(6):
        try:
            return fn(*args, **kwargs)
        except APIResponseError as exc:
            code = getattr(exc, "code", None)
            status = getattr(exc, "status", None)
            retryable = code in RETRYABLE or (isinstance(status, int) and (status == 429 or status >= 500))
            if retryable and attempt < 5:
                time.sleep(2 ** attempt)
                continue
            raise


def main():
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        sys.exit("NOTION_TOKEN is not set. See the SETUP block at the top of this file.")

    notion = Client(auth=token, notion_version=API_VERSION)

    print("Creating database ...")
    try:
        db = with_retry(
            notion.databases.create,
            parent={"type": "page_id", "page_id": PARENT_PAGE_ID},
            title=[{"type": "text", "text": {"content": DATABASE_TITLE}}],
            initial_data_source={"properties": {
                "Task": {"title": {}},
                "Task ID": {"rich_text": {}},
                "Owner": {"select": {"options": [
                    {"name": o, "color": c} for o, c in zip(
                        OWNERS, ["blue", "green", "orange", "purple"])
                ]}},
                "Start": {"date": {}},
                "End": {"date": {}},
                "Phase": {"select": {"options": [
                    {"name": p, "color": "default"} for p in PHASES
                ]}},
                "Status": {"select": {"options": [
                    {"name": "Not started", "color": "gray"},
                    {"name": "In progress", "color": "blue"},
                    {"name": "Blocked", "color": "red"},
                    {"name": "Done", "color": "green"},
                ]}},
                "Notes": {"rich_text": {}},
            }},
        )
    except APIResponseError as exc:
        if getattr(exc, "code", None) == "unauthorized":
            sys.exit(
                "Unauthorized. Two likely causes:\n"
                "  1. The token is wrong.\n"
                "  2. The integration is not connected to the parent page.\n"
                "     Open the page -> ... -> Connections -> add your integration."
            )
        if getattr(exc, "code", None) == "object_not_found":
            sys.exit(
                "Page not found. Open the page, use ... -> Connections, and add "
                "your integration. Then rerun."
            )
        raise

    db_id = db["id"]
    ds_id = db["data_sources"][0]["id"]
    print(f"  database     {db_id}")
    print(f"  data source  {ds_id}")

    # Skip tasks that already exist, so the script is safe to re-run
    existing = set()
    cursor = None
    while True:
        kwargs = {"data_source_id": ds_id, "page_size": 100}
        if cursor:
            kwargs["start_cursor"] = cursor
        page = with_retry(notion.data_sources.query, **kwargs)
        for result in page["results"]:
            title = result["properties"].get("Task", {}).get("title", [])
            if title:
                existing.add(title[0]["plain_text"])
        if not page.get("has_more"):
            break
        cursor = page.get("next_cursor")

    created = 0
    for task_id, name, owner, start, end, phase, notes in TASKS:
        if name in existing:
            print(f"  skip  {task_id}  (already present)")
            continue
        with_retry(
            notion.pages.create,
            parent={"type": "data_source_id", "data_source_id": ds_id},
            properties={
                "Task": {"title": [{"type": "text", "text": {"content": name}}]},
                "Task ID": {"rich_text": [{"type": "text", "text": {"content": task_id}}]},
                "Owner": {"select": {"name": owner}},
                "Start": {"date": {"start": start, "end": end}},
                "End": {"date": {"start": end}},
                "Phase": {"select": {"name": phase}},
                "Status": {"select": {"name": "Not started"}},
                "Notes": {"rich_text": [{"type": "text", "text": {"content": notes}}]},
            },
        )
        created += 1
        print(f"  add   {task_id}  {name}")

    print(f"\nDone. {created} task(s) added.")

    # Try to create the Timeline view automatically.
    try:
        ds = with_retry(notion.data_sources.retrieve, data_source_id=ds_id)
        props = ds["properties"]
        start_id = props["Start"]["id"]
        end_id = props["End"]["id"]
        with_retry(
            notion.request,
            path="views",
            method="POST",
            body={
                "database_id": db_id,
                "data_source_id": ds_id,
                "name": "Gantt",
                "type": "timeline",
                "configuration": {
                    "type": "timeline",
                    "date_property_id": start_id,
                    "end_date_property_id": end_id,
                    "show_table": True,
                    "preference": {"zoom_level": "week"},
                },
            },
        )
        print("Timeline view created.")
    except Exception as exc:  # noqa: BLE001 - view API may be unavailable
        print("\nCould not create the Timeline view automatically.")
        print(f"  reason: {type(exc).__name__}")
        print("  Fix in 20 seconds by hand:")
        print("    open the database -> + New view -> Timeline")
        print("    -> Layout -> 'Show timeline by' -> Start")
        print("    -> enable separate start/end properties")

    print("\nNext: open the database, sort by Start, group by Phase.")
    print("Colour by Owner using conditional formatting if available.")


if __name__ == "__main__":
    main()
