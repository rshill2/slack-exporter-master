# Deployment Guide for Render

This guide will help you deploy the Slack Exporter to Render for testing and production use.

## Prerequisites

1. A Render account (free tier available)
2. A Slack workspace with admin permissions
3. A Slack app configured with the necessary permissions

## Step 1: Configure Your Slack App

1. Visit [https://api.slack.com/apps/](https://api.slack.com/apps/) and sign in to your workspace
2. Click `Create New App` and choose `App Manifest`
3. Paste the contents of `slack.yaml` into the YAML box
4. **Important**: Uncomment the `slash_commands` section in `slack.yaml` and replace `YOUR_HOST_URL_HERE` with your Render URL (you'll get this after deployment)
5. Select `Install to Workspace` and accept the permissions
6. Copy the `OAuth Access Token` (starts with `xoxp-`)

## Step 2: Deploy to Render

### Option A: Deploy via Render Dashboard

1. Go to [https://dashboard.render.com/](https://dashboard.render.com/)
2. Click `New +` and select `Web Service`
3. Connect your GitHub repository or use the public repository URL
4. Configure the service:
   - **Name**: `slack-exporter`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn bot:app`
   - **Plan**: `Free`

### Option B: Deploy via render.yaml (Recommended)

1. Push your code to a Git repository
2. In Render dashboard, click `New +` and select `Blueprint`
3. Connect your repository
4. Render will automatically detect and use the `render.yaml` configuration

## Step 3: Configure Environment Variables

In your Render service dashboard:

1. Go to `Environment` tab
2. Add the following environment variable:
   - **Key**: `SLACK_USER_TOKEN`
   - **Value**: Your Slack OAuth token (xoxp-...)
   - **Sync**: `No` (for security)

## Step 4: Update Slack App Configuration

1. Once deployed, copy your Render service URL (e.g., `https://slack-exporter.onrender.com`)
2. Go back to your Slack app configuration
3. Update the `slack.yaml` file with your actual Render URL:
   ```yaml
   url: https://your-app-name.onrender.com/slack/export-channel
   ```
4. Reinstall the app to your workspace

## Step 5: Test the Deployment

1. Visit your Render service URL + `/health` to verify the service is running
2. In any Slack channel, try the slash commands:
   - `/export-channel text` - Export channel as text
   - `/export-channel json` - Export channel as JSON
   - `/export-replies text` - Export reply threads as text
   - `/export-replies json` - Export reply threads as JSON

## Troubleshooting

### Common Issues

1. **Service not starting**: Check the logs in Render dashboard
2. **Slack commands not working**: Verify the URL in your Slack app configuration
3. **Permission errors**: Ensure your Slack token has the correct scopes
4. **File download issues**: Files are stored temporarily and auto-deleted after download

### Logs and Monitoring

- View logs in the Render dashboard under your service
- Monitor the `/health` endpoint for service status
- Check Slack app configuration for any webhook errors

## Security Considerations

1. **Environment Variables**: Never commit your Slack token to version control
2. **File Access**: Files are automatically deleted after download
3. **Input Validation**: The app includes basic security checks for file downloads
4. **Rate Limiting**: The app handles Slack API rate limits automatically

## Scaling Considerations

- **Free Tier**: Limited to 750 hours/month, sleeps after 15 minutes of inactivity
- **Paid Plans**: For production use, consider upgrading to a paid plan
- **File Storage**: For high-volume usage, consider implementing cloud storage (S3, etc.)

## Support

For issues with:
- **Render**: Check Render documentation and support
- **Slack API**: Consult Slack API documentation
- **This Application**: Check the logs and ensure proper configuration
