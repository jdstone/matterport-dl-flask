from flask import render_template, request
import os
import json
from app.home import bp


GRAPH_DATA_REQ = {}

def openDirReadGraphReqs(path, pageId):
    for root, dirs, filenames in os.walk(path):
        for file in filenames:
            with open(os.path.join(root, file), "r", encoding="UTF-8") as f:
                GRAPH_DATA_REQ[file.replace(".json", "")] = f.read().replace("[MATTERPORT_MODEL_ID]",pageId)


@bp.route('/')
def index():

    pageId = '87ehWawBGLj'

    openDirReadGraphReqs("graph_posts", pageId)

    if request.method == 'GET':

        global SHOWCASE_INTERNAL_NAME
        redirect_msg = None
        # orig_request = request.path


        if request.path.startswith("/js/showcase.js") and os.path.exists(f"js/{SHOWCASE_INTERNAL_NAME}"):
            redirect_msg = "using our internal showcase.js file"
            request.path = f"/js/{SHOWCASE_INTERNAL_NAME}"

        if request.path.startswith("/locale/messages/strings_") and not os.path.exists(f".{request.path}"):
            redirect_msg = "original request was for a locale we do not have downloaded"
            request.path = "/locale/strings.json"
        raw_path, _, query = request.path.partition('?')
        if "crop=" in query and raw_path.endswith(".jpg"):
            query_args = request.args(query)
            crop_addition = query_args.get("crop", None)
            if crop_addition is not None:
                crop_addition = f'crop={crop_addition[0]}'
            else:
                crop_addition = ''

            width_addition = query_args.get("width", None)
            if width_addition is not None:
                width_addition = f'width={width_addition[0]}_'
            else:
                width_addition = ''
            test_path = raw_path + width_addition + crop_addition + ".jpg"
            # if os.path.exists(f".{test_path}"):
            #     request.path = test_path
            #     redirect_msg = "dollhouse/floorplan texture request that we have downloaded, better than generic texture file"
        # if redirect_msg is not None or orig_request != request.path:
        #     logging.info(
        #         f'Redirecting {orig_request} => {request.path} as {redirect_msg}')


    elif request.method == 'POST':

        post_msg = None
        try:
            if request.path == "/api/mp/models/graph":
                request.send_response(200)
                request.end_headers()
                content_len = int(request.headers.get('content-length'))
                post_body = request.rfile.read(content_len).decode('utf-8')
                json_body = json.loads(post_body)
                option_name = json_body["operationName"]
                if option_name in GRAPH_DATA_REQ:
                    file_path = f"api/mp/models/graph_{option_name}.json"
                    if os.path.exists(file_path):
                        with open(file_path, "r", encoding="UTF-8") as f:
                            request.wfile.write(f.read().encode('utf-8'))
                            post_msg = f"graph of operationName: {option_name} we are handling internally"
                            return
                    else:
                        post_msg = f"graph for operationName: {option_name} we don't know how to handle, but likely could add support, returning empty instead"

                request.wfile.write(bytes('{"data": "empty"}', "utf-8"))
                return
        except Exception as error:
            post_msg = f"Error trying to handle a post request of: {str(error)} this should not happen"
            pass
        # finally:
        #     if post_msg is not None:
        #         logging.info(
        #             f'Handling a post request on {request.path}: {post_msg}')


    return render_template('home/index.html.j2',
                           
                           )

