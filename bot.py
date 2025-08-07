import os
import requests
from flask import Flask, request, Response, jsonify
from urllib.parse import urljoin
from uuid import uuid4
import json
from dotenv import load_dotenv

# Import with error handling for deployment
try:
    from exporter import *
except ImportError as e:
    print(f"Warning: Could not import exporter module: {e}")
    # Create dummy functions to prevent crashes
    def post_response(*args, **kwargs):
        print("post_response called but exporter not available")
    
    def channel_history(*args, **kwargs):
        return []
    
    def parse_channel_history(*args, **kwargs):
        return "Export functionality not available"
    
    def user_list(*args, **kwargs):
        return []
    
    def channel_replies(*args, **kwargs):
        return []
    
    def parse_replies(*args, **kwargs):
        return "Export functionality not available"

try:
    from config import is_user_allowed, is_channel_allowed, add_allowed_user, remove_allowed_user, add_allowed_channel, remove_allowed_channel, list_allowed_users, list_allowed_channels
except ImportError as e:
    print(f"Warning: Could not import config module: {e}")
    # Create dummy functions to prevent crashes
    def is_user_allowed(user_id):
        return True  # Allow all users if config not available
    
    def is_channel_allowed(channel_id):
        return True  # Allow all channels if config not available
    
    def add_allowed_user(user_id):
        return True
    
    def remove_allowed_user(user_id):
        return True
    
    def add_allowed_channel(channel_id):
        return True
    
    def remove_allowed_channel(channel_id):
        return True
    
    def list_allowed_users():
        return []
    
    def list_allowed_channels():
        return []

app = Flask(__name__)
load_dotenv(os.path.join(app.root_path, ".env"))

# Health check endpoint for Render
@app.route("/health")
def health_check():
    return jsonify({"status": "healthy", "service": "slack-exporter"}), 200

# Flask routes

@app.route("/slack/events/export-channel", methods=["POST"])
def export_channel():
    data = request.form

    try:
        team_id = data["team_id"]
        team_domain = data["team_domain"]
        ch_id = data["channel_id"]
        ch_name = data["channel_name"]
        response_url = data["response_url"]
        command_args = data["text"]
        user_id = data["user_id"]
    except KeyError as e:
        return Response(f"Sorry! I got an unexpected response (KeyError: {e})."), 200

    # Check if user is allowed to use the exporter
    if not is_user_allowed(user_id):
        post_response(response_url, f"❌ Access denied. User {user_id} is not authorized to use this exporter.")
        return Response(), 200

    # Check if channel is allowed to be exported
    if not is_channel_allowed(ch_id):
        post_response(response_url, f"❌ Access denied. Channel {ch_id} is not authorized for export.")
        return Response(), 200

    post_response(response_url, "Retrieving history for this channel...")
    ch_hist = channel_history(ch_id, response_url)

    export_mode = str(command_args).lower()

    exports_subdir = "exports"
    exports_dir = os.path.join(app.root_path, exports_subdir)
    file_ext = ".txt" if export_mode == "text" else ".json"
    filename = "%s-ch_%s-%s%s" % (team_domain, ch_id, str(uuid4().hex)[:6], file_ext)
    filepath = os.path.join(exports_dir, filename)
    loc = urljoin(request.url_root, "download/%s" % filename)

    if not os.path.isdir(exports_dir):
        os.makedirs(exports_dir, exist_ok=True)

    with open(filepath, mode="w", encoding="utf-8") as f:
        if export_mode == "text":
            num_msgs = len(ch_hist)
            sep = "=" * 24
            header_str = "Channel Name: %s\nChannel ID: %s\n%s Messages\n%s\n\n" % (
                ch_name,
                ch_id,
                num_msgs,
                sep,
            )
            data_ch = header_str + parse_channel_history(
                ch_hist, user_list(team_id, response_url)
            )
            f.write(data_ch)
        else:
            json.dump(ch_hist, f, indent=4, ensure_ascii=False)

    post_response(
        response_url,
        "Done! This channel's history is available for download here (note that this link "
        "is single-use): %s" % loc,
    )

    return Response(), 200


@app.route("/slack/events/export-replies", methods=["POST"])
def export_replies():
    data = request.form

    try:
        team_id = data["team_id"]
        team_domain = data["team_domain"]
        ch_id = data["channel_id"]
        ch_name = data["channel_name"]
        response_url = data["response_url"]
        command_args = data["text"]
        user_id = data["user_id"]
    except KeyError as e:
        return Response(f"Sorry! I got an unexpected response (KeyError: {e})."), 200

    # Check if user is allowed to use the exporter
    if not is_user_allowed(user_id):
        post_response(response_url, f"❌ Access denied. User {user_id} is not authorized to use this exporter.")
        return Response(), 200

    # Check if channel is allowed to be exported
    if not is_channel_allowed(ch_id):
        post_response(response_url, f"❌ Access denied. Channel {ch_id} is not authorized for export.")
        return Response(), 200

    post_response(response_url, "Retrieving reply threads for this channel...")
    print(ch_id)
    ch_hist = channel_history(ch_id, response_url)
    print(ch_hist)
    ch_replies = channel_replies(
        [x["ts"] for x in ch_hist if "reply_count" in x],
        ch_id,
        response_url=response_url,
    )

    export_mode = str(command_args).lower()

    exports_subdir = "exports"
    exports_dir = os.path.join(app.root_path, exports_subdir)
    file_ext = ".txt" if export_mode == "text" else ".json"
    filename = "%s-re_%s-%s%s" % (team_domain, ch_id, str(uuid4().hex)[:6], file_ext)
    filepath = os.path.join(exports_dir, filename)
    loc = urljoin(request.url_root, "download/%s" % filename)

    if export_mode == "text":
        header_str = "Threads in: %s\n%s Messages" % (ch_name, len(ch_replies))
        data_replies = parse_replies(ch_replies, user_list(team_id, response_url))
        sep = "=" * 24
        data_replies = "%s\n%s\n\n%s" % (header_str, sep, data_replies)
    else:
        data_replies = ch_replies

    if not os.path.isdir(exports_dir):
        os.makedirs(exports_dir, exist_ok=True)

    with open(filepath, mode="w", encoding="utf-8") as f:
        if export_mode == "text":
            f.write(data_replies)
        else:
            json.dump(data_replies, f, indent=4, ensure_ascii=False)

    post_response(
        response_url,
        "Done! This channel's reply threads are available for download here (note that this "
        "link is single-use): %s" % loc,
    )

    return Response(), 200


@app.route("/download/<filename>")
def download(filename):
    path = os.path.join(app.root_path, "exports", filename)
    
    # Security check: ensure filename doesn't contain path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        return Response("Invalid filename", status=400)

    if not os.path.exists(path):
        return Response("File not found", status=404)

    def generate():
        with open(path, encoding="utf-8") as f:
            yield from f
        os.remove(path)

    mimetype = (
        "text/plain" if os.path.splitext(filename)[-1] == ".txt" else "application/json"
    )

    r = app.response_class(generate(), mimetype=mimetype)
    r.headers.set("Content-Disposition", "attachment", filename=filename)
    return r


# Management endpoints for access control
@app.route("/admin/users", methods=["GET"])
def list_users():
    """List all allowed users"""
    users = list_allowed_users()
    return jsonify({
        "allowed_users": users,
        "count": len(users)
    })


@app.route("/admin/users", methods=["POST"])
def add_user():
    """Add a user to the allowed list"""
    data = request.get_json()
    if not data or "user_id" not in data:
        return jsonify({"error": "user_id is required"}), 400
    
    user_id = data["user_id"]
    if add_allowed_user(user_id):
        return jsonify({
            "success": True,
            "message": f"User {user_id} added successfully",
            "allowed_users": list_allowed_users()
        })
    else:
        return jsonify({
            "success": False,
            "error": f"Failed to add user {user_id}"
        }), 400


@app.route("/admin/users/<user_id>", methods=["DELETE"])
def remove_user(user_id):
    """Remove a user from the allowed list"""
    if remove_allowed_user(user_id):
        return jsonify({
            "success": True,
            "message": f"User {user_id} removed successfully",
            "allowed_users": list_allowed_users()
        })
    else:
        return jsonify({
            "success": False,
            "error": f"User {user_id} not found or failed to remove"
        }), 404


@app.route("/admin/channels", methods=["GET"])
def list_channels():
    """List all allowed channels"""
    channels = list_allowed_channels()
    return jsonify({
        "allowed_channels": channels,
        "count": len(channels)
    })


@app.route("/admin/channels", methods=["POST"])
def add_channel():
    """Add a channel to the allowed list"""
    data = request.get_json()
    if not data or "channel_id" not in data:
        return jsonify({"error": "channel_id is required"}), 400
    
    channel_id = data["channel_id"]
    if add_allowed_channel(channel_id):
        return jsonify({
            "success": True,
            "message": f"Channel {channel_id} added successfully",
            "allowed_channels": list_allowed_channels()
        })
    else:
        return jsonify({
            "success": False,
            "error": f"Failed to add channel {channel_id}"
        }), 400


@app.route("/admin/channels/<channel_id>", methods=["DELETE"])
def remove_channel(channel_id):
    """Remove a channel from the allowed list"""
    if remove_allowed_channel(channel_id):
        return jsonify({
            "success": True,
            "message": f"Channel {channel_id} removed successfully",
            "allowed_channels": list_allowed_channels()
        })
    else:
        return jsonify({
            "success": False,
            "error": f"Channel {channel_id} not found or failed to remove"
        }), 404


@app.route("/admin/status", methods=["GET"])
def admin_status():
    """Get overall status of access control"""
    return jsonify({
        "allowed_users": list_allowed_users(),
        "allowed_channels": list_allowed_channels(),
        "user_count": len(list_allowed_users()),
        "channel_count": len(list_allowed_channels())
    })


@app.route("/admin", methods=["GET"])
def admin_interface():
    """Serve the admin interface HTML"""
    try:
        with open("admin_interface.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Admin interface not found", 404


if __name__ == "__main__":
    # For development only - use gunicorn in production
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
