# slack-exporter

A Slack bot and standalone script for exporting messages and file attachments from public and private channels, using Slack's new Conversations API.

A similar service is provided by Slack for workspace admins at [https://my.slack.com/services/export](https://my.slack.com/services/export) (where `my` can be replaced with your full workspace name to refer to a workspace different than your default). However, it can only access public channels, while `slack-exporter` can retrieve data from any channel accessible to your user account.

## Features

- ✅ Export public and private channel conversations
- ✅ Export direct messages and group DMs
- ✅ Export reply threads
- ✅ Download file attachments
- ✅ Support for both JSON and text formats
- ✅ Rate limiting handling
- ✅ Slack bot with slash commands
- ✅ Standalone command-line tool
- ✅ Ready for Render deployment
- ✅ Access control for users and channels
- ✅ Web-based admin interface
- ✅ Command-line management tools

## Quick Start (Render Deployment)

For the fastest setup, deploy directly to Render:

1. **Fork this repository** to your GitHub account
2. **Deploy to Render** using the [Deployment Guide](DEPLOYMENT.md)
3. **Configure your Slack app** with the provided `slack.yaml`
4. **Test the slash commands** in your Slack workspace

## Authentication with Slack

There are two ways to use `slack-exporter` (detailed below). Both require a Slack API token to be able to communicate with your workspace.

1. Visit [https://api.slack.com/apps/](https://api.slack.com/apps/) and sign in to your workspace.
2. Click `Create New App`. If prompted to select "how you'd like to configure your app's scopes", choose the `App Manifest` option. You can configure the app manually instead, but you will be prompted to enter an app name and additional steps to set up permissions instead of the single step below. Once creates, select your workspace.
3. You should then be prompted for an app manifest. Paste the contents of the `slack.yaml` file (in the root of this repo) into the YAML box.
4. Select `Install to Workspace` at the top of that page (or `Reinstall to Workspace` if you have done this previously) and accept at the prompt.
5. Copy the `OAuth Access Token` (which will generally start with `xoxp` for user-level permissions and may be located in a section like "OAuth & Permissions" in the sidebar).

## Usage

### As a standalone script

`exporter.py` can create an archive of all conversation history in your workspace which is accessible to your user account.

1. Either add 

    ```text
    SLACK_USER_TOKEN = xoxp-xxxxxxxxxxxxx...
    ```
    
    to a file named `.env` in the same directory as `exporter.py`, or run the following in your shell (replacing the value with the user token you obtained in the [Authentication with Slack](#authentication-with-slack) section above).

    ```shell script
    export SLACK_USER_TOKEN=xoxp-xxxxxxxxxxxxx...
    ```

2. If you cloned this repo, make sure that dependencies are installed by running `pip install -r requirements.txt` in the repo root directory.
3. Run `python exporter.py --help` to view the available export options. You can test that access to Slack is working by listing available conversations: `python exporter.py --lc`.

### As a Slack bot

`bot.py` is a Slack bot that responds to "slash commands" in Slack channels (e.g., `/export-channel`). To connect the bot to the Slack app generated in [Authentication with Slack](#authentication-with-slack), create a file named `.env` in the root directory of this repo, and add the following line:

```text
SLACK_USER_TOKEN = xoxp-xxxxxxxxxxxxx...
``` 

Save this file and run the Flask application in `bot.py` such that the application is exposed to the Internet. This can be done via a web server (e.g., Heroku), as well as via the ngrok service, which assigns your `localhost` server a public URL.

To use the ngrok method:

1. [Download](https://ngrok.com/download) the appropriate binary.
2. Run `python bot.py`
3. Run the ngrok binary with `path/to/ngrok http 5000`, where `5000` is the port on which the Flask application (step 2) is running. Copy the forwarding HTTPS address provided.

4. Create the following slash commands will be created (one for each applicable Flask route in `bot.py`):

    | Command         | Request URL                               | Arguments    | Example Usage        |
    |-----------------|-------------------------------------------|--------------|----------------------|
    | /export-channel | https://`[host_url]`/slack/events/export-channel | json \| text | /export-channel text |
    | /export-replies | https://`[host_url]`/slack/events/export-replies | json \| text | /export-replies json |

    To do this, update the `slash-commands` section in `slack.yaml` and replace `YOUR_HOST_URL_HERE` with something like `https://xxxxxxxxxxxx.ngrok.io` (if using ngrok). Then navigate back to `OAuth & Permissions` and click `(Re)install to Workspace` to add these slash commands to the workspace (ensure the OAuth token in your `.env` file is still correct).

## Deployment

### Render (Recommended)

See the [Deployment Guide](DEPLOYMENT.md) for detailed instructions on deploying to Render.

### Other Platforms

The application can be deployed to any platform that supports Python web applications:

- **Heroku**: Use the provided `requirements.txt` and set the start command to `gunicorn bot:app`
- **Railway**: Similar to Render deployment
- **DigitalOcean App Platform**: Supports Python applications
- **AWS/GCP/Azure**: Deploy as a container or serverless function

## Development

### Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up your `.env` file with your Slack token
4. Run the bot: `python bot.py`
5. Use ngrok or similar for local testing with Slack

### Testing

- Health check: `curl http://localhost:5000/health`
- Test Slack integration with ngrok
- Verify file downloads work correctly

## Access Control

The application includes comprehensive access control to restrict which users and channels can be exported:

### User Management
- Only specific users can use the export commands
- User IDs must be added to the allowed list
- Format: `U097LRDRB8F` (starts with 'U')

### Channel Management
- Only specific channels can be exported
- Channel IDs must be added to the allowed list
- Format: `C099EEMH26N` (starts with 'C')

### Management Methods

**Command Line:**
```bash
# List all allowed users and channels
python manage_access.py --list

# Add a user
python manage_access.py --add-user U097LRDRB8F

# Add a channel
python manage_access.py --add-channel C099EEMH26N

# Remove a user
python manage_access.py --remove-user U097LRDRB8F

# Remove a channel
python manage_access.py --remove-channel C099EEMH26N
```

**Web Interface:**
- Visit `/admin` on your deployed application
- Use the web interface to manage users and channels
- Real-time updates and status monitoring

**API Endpoints:**
- `GET /admin/users` - List allowed users
- `POST /admin/users` - Add a user
- `DELETE /admin/users/<user_id>` - Remove a user
- `GET /admin/channels` - List allowed channels
- `POST /admin/channels` - Add a channel
- `DELETE /admin/channels/<channel_id>` - Remove a channel
- `GET /admin/status` - Get overall status

## Security Considerations

- Never commit your Slack token to version control
- Files are automatically deleted after download
- Basic input validation is implemented
- Rate limiting is handled automatically
- Access control restricts users and channels
- Configuration files are stored securely

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Author

[Seb Seager](https://github.com/sebseager)

## License

This software is available under the [GPL](LICENSE).
