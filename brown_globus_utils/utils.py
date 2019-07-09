import os
import globus_sdk
from dotenv import load_dotenv

def get_tc():
    """Get Globus transfer client

    This function loads GLOBUS_CLIENT_ID from .env file
    """
    load_dotenv()
    GLOBUS_CLIENT_ID = os.getenv("GLOBUS_CLIENT_ID")

    client = globus_sdk.NativeAppAuthClient(GLOBUS_CLIENT_ID)
    client.oauth2_start_flow()

    authorize_url = client.oauth2_get_authorize_url()
    print('Please go to this URL and login: {0}'.format(authorize_url))

    # this is to work on Python2 and Python3 -- you can just use raw_input() or
    # input() for your specific version
    get_input = getattr(__builtins__, 'raw_input', input)
    auth_code = get_input(
        'Please enter the code you get after login here: ').strip()
    token_response = client.oauth2_exchange_code_for_tokens(auth_code)

    globus_auth_data = token_response.by_resource_server['auth.globus.org']
    globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']

    # most specifically, you want these tokens as strings
    AUTH_TOKEN = globus_auth_data['access_token']
    TRANSFER_TOKEN = globus_transfer_data['access_token']

    # a GlobusAuthorizer is an auxiliary object we use to wrap the token. In
    # more advanced scenarios, other types of GlobusAuthorizers give us
    # expressive power
    authorizer = globus_sdk.AccessTokenAuthorizer(TRANSFER_TOKEN)
    tc = globus_sdk.TransferClient(authorizer=authorizer)

    return tc


def print_endpoints(tc):
    print("Endpoints administered by me:")
    for ep in tc.endpoint_search(filter_scope="administered-by-me"):
        print("[{}] {}".format(ep["id"], ep["display_name"]))


def transfer_sync(tc, source_endpoint, target_enpoint, source_loc, target_loc, isfile):
    """Transfer a directory, recursively, from source to targe.
    The source and target endpoints are specified by name

    Args:
    tc (transfer client - see get_tc())
    source_endpoint(str)
    target_enpoint(str)
    source_dir(str)
    target_dir(str)
    label
    """

    sids = tc.endpoint_search(source_endpoint, filter_scope="administered-by-me")
    tids = tc.endpoint_search(target_enpoint, filter_scope="administered-by-me")

#     assert(len(sids) == 1 & len(tids) ==1)
    print(type(sids))
    source_endpoint_id = sids[0]["id"]
    target_endpoint_id = tids[0]["id"]


    tdata = globus_sdk.TransferData(tc, source_endpoint_id,
                                        target_endpoint_id,
                                        label="brown-globus-utils",
                                        sync_level="checksum")

    if isfile:
            tdata.add_item(source_loc, target_loc)
    else:
            tdata.add_item(source_loc, target_loc, recursive=True)

    transfer_result = tc.submit_transfer(tdata)

    return transfer_result["task_id"]