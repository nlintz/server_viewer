import sys
import urllib
import urllib2
import json
import pprint

import oauth_helper as oauth

def start_oauth():
    app_info = oauth.AppInfo('e2hdmubkxyqk5tr', 'jso26ckz6ldg498')
    (request_token, requestURL) = get_request_token(app_info)
    return (request_token, app_info, requestURL)

def get_request_token(app_info):
    # Step 1: Get request token
    r = http_request("https://api.dropbox.com/1/oauth/request_token", oauth.mk_header_no_token(app_info))
    request_token = oauth.parse_token(r)

    # Step 2: Send user to the authorization page (we're not a web app, so we don't have a callback URL)
    requestURL = ("https://www.dropbox.com/1/oauth/authorize?oauth_token=%s\n" % urllib.quote_plus(request_token.key))
    # sys.stdin.readline()
    return request_token, requestURL

def get_access_token(request_token, app_info):
    # Step 3: Get access token
    r = http_request("https://api.dropbox.com/1/oauth/access_token", oauth.mk_header_with_token(app_info, request_token))
    access_token = oauth.parse_token(r)
    return access_token

def http_request(url, auth_header):
    req = urllib2.Request(url)
    req.add_header("Authorization", auth_header)
    return urllib2.urlopen(req).read()

if __name__ == "__main__":
    start_oauth()
    
