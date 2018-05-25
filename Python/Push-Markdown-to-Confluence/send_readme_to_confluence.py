#!/usr/bin/python3

from http import HTTPStatus
from typing import Tuple
import markdown
import os
import requests
import sys

# This "simple" script has been developed to allow me to punt README.md files (which are common in
# repositories I contribute to) into an Atlassian Confluence instance. The idea is that I could
# trigger this script via a git hook, to ensure that accurate and up-to-date information is
# available to non-git users (plus, it's nicer to read an HTML page in a browser, and have a web
# search of documentation, than to be forced to search for and read Markdown documents via the
# terminal). Additionally, I anticipate that this script will be called via a Makefile, with a
# target of "doco".  Example:
#
# $ make doco
# 200: OK - Confluence article https://localhost/ has now been updated
#
# While I could probably use a plugin that displays Markdown from a git repo, I wanted to:
#
# - Save a few $$$ in testing (plugins aren't free)
# - Use this toy to experiment with the Confluence API
# - Be able to tolerate a loss of connectivity between the Confluence instance and the git server
#
# TODO:
#
#   - Improve the output on success
#   - Confluence URL, content ID, markdown filename etc should be parameters
#   - Add coloured output (e.g. HTTP response codes etc)


# Type aliases/synonyms
RequestsSession = requests.sessions.Session
UpdateResp = Tuple[requests.models.Response, str]


# Globals
CONFLUENCE_BASE_URL = "https://your-confluence-instance.example.com"
CONFLUENCE_API_URL = "{}/rest/api".format(CONFLUENCE_BASE_URL)
CONFLUENCE_CONTENT_ROUTE = "/content"
CONTENT_ID = 1234567
CAPATH = "/path/to/your/cafile"


def build_session(username: str, pw_filepath: str) -> RequestsSession:
    """
    This function takes a username and the path to a password file, and
    returns a "requests" session object
    """

    # Ensure that the password file is readable
    if not os.access(pw_filepath, os.R_OK):
        print("{}: FATAL - password file is not a readable file".format(sys.argv[0]))
        sys.exit(1)

    # Open and read the password file
    with open(pw_filepath, "r") as f:
        pw_file_text = f.read()

    # Perform simple checking of the file contents
    pw_file_parts = pw_file_text.split()
    if len(pw_file_parts) != 1:
        print("{}: FATAL - password file should contain a single password string only".format(sys.argv[0]))
        sys.exit(1)

    # Instantiate session object
    s = requests.Session()

    # Setup authentication parameters to be used with this session
    s.auth = (username, pw_file_parts[0])
    return s


def get_content_metadata(session: RequestsSession, content_id: int, **kwargs: dict) -> dict:
    """
    This function takes a requests session object, and a Confluence content
    ID, and attempts to return the current revision ID of the specified content
    ID
    """

    # Override the default capath if the user provided their own
    capath = kwargs["verify"] if "verify" in kwargs else CAPATH

    # Ensure that capath is a readable file
    if not os.access(str(capath), os.R_OK):
        print("{}: FATAL - capath is not a readable file".format(sys.argv[0]))
        sys.exit(1)

    # Build the URL from GLOBALS
    # FIXME: Should these globals be pulled from config? Probably not?
    url = "{}{}/{}".format(CONFLUENCE_API_URL, CONFLUENCE_CONTENT_ROUTE, str(content_id))

    # Attempt to fetch response from Confluence
    r = session.get(url, verify=capath)

    # Alert the user if the HTTP request has failed
    if not r.ok:
        present_message("get_content_metadata", url, "GET", r.status_code, "FATAL")
        sys.exit(1)

    # Attempt to access this content ID's version number
    try:
        content_metadata = r.json()
    # ValueError is raised if response does not contain valid JSON
    except ValueError:
        print("{}: FATAL - Response body was not valid JSON".format(sys.argv[0]))
        sys.exit(1)

    # Return the "version" integer, required to be able to update the page
    return content_metadata


# Return is (requests.models.Response, str):
# I could also pass content_metadata INTO this function from main, to avoid passing extra
# data back out (it would already be available to the caller in this scenario), but for the
# time being, I've decided to just pass the data back out in a tuple.
def update_page(session: RequestsSession, content_id: int, new_body: str, **kwargs: dict) -> UpdateResp:
    """
    This function takes a requests session object, a Confluence content ID,
    and a new document body. Returns a "requests" response object
    """
    content_metadata = get_content_metadata(session, content_id)

    # Extract the required data
    try:
        uri = content_metadata["_links"]["webui"]
        data = {
                "version": {
                    "number": content_metadata["version"]["number"] + 1,
                },
                "title": content_metadata["title"],
                "type": content_metadata["type"],
                "body": {
                    "storage": {
                        "value": new_body,
                        "representation": "storage"
                    }
                }
        }
    except KeyError:
        print("{}: FATAL - JSON object returned by the API is missing required keys".format(sys.argv[0]))
        sys.exit(1)

    url = construct_content_url(content_id)

    # Perform HTTP PUT to API endpoint
    r = session.put(url, json=data, headers={"Content-Type": "application/json"})

    # Alert the user if the HTTP request has failed
    if not r.ok:
        present_message("update_page", url, "PUT", r.status_code, "FATAL")
        sys.exit(1)

    # UpdateResp is of type Tuple[requests.models.Response, str]
    return (r, uri)


# This function should probably be genericised to "construct_url", but as I but
# I don't know all the ins and outs of the API yet, I'm only tackling _this_
# specific problem at the moment. This will be improved in future if required
def construct_content_url(content_id: int) -> str:
    """
    This simple function takes a Confluence content ID, and returns an API
    URL string
    """

    url = "{}{}/{}".format(CONFLUENCE_API_URL, CONFLUENCE_CONTENT_ROUTE, str(content_id))
    return url


def get_file_contents(filepath: str="README.md") -> str:
    """
    This function opens and reads `filepath`, and returns the file's body
    """
    with open(filepath) as f:
        md = f.read()
    # Return the raw, unrendered Markdown text, as a string
    return md


def present_message(caller: str, url: str, http_method: str, resp_code: int, message: str) -> None:
    """
    This simple function takes a number of params and then prints them to stdout
    """
    output = []
    output.append("Response: HTTP {} ({})".format(str(resp_code), HTTPStatus(resp_code).name))
    output.append("Info: {}".format(message))
    output.append("URL: {}".format(url))
    print("\n".join(output))


def usage() -> None:
    """
    Simple void function which prompts the user on how to use this tool, and exits
    """
    print("{} username path-to-password-file".format(sys.argv[0]))
    sys.exit(1)


def main(username: str, password: str, content_id: int) -> None:
    """
    This simple function takes a username, a password filepath, and a
    content ID, then goes on to fetch the contents of the file, and HTTP PUT
    it into Confluence. This is a void function.
    """
    s = build_session(username, password)
    new_body = get_file_contents()
    r, uri = update_page(s, content_id, markdown.markdown(new_body))

    # Provide some output to the user
    present_message("main", CONFLUENCE_BASE_URL + uri, "PUT", 200, "Content has been updated")


if __name__ == "__main__":
    # Ensure that we've been primed with a username and password
    if "-h" in sys.argv or "--help" in sys.argv or len(sys.argv) != 3:
        usage()

    # Call the main function with the user's args
    main(sys.argv[1], sys.argv[2], CONTENT_ID)
