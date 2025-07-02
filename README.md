# Webhook File Upload and Email System

A Python Flask-based webhook system that allows file uploads with content and automatically sends emails to a default recipient.

## Features

- **File Upload**: Support for various file types (txt, pdf, png, jpg, jpeg, gif, doc, docx, xls, xlsx)
- **Content Addition**: Add custom content/message with each file upload
- **Email Notifications**: Automatic email sending with file attachments
- **Web Interface**: User-friendly web form for uploads
- **Webhook API**: RESTful API endpoint for programmatic access
- **Secure Configuration**: Environment-based configuration management

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and configure it with your settings:

```bash
cp env.example .env
```

Edit the `.env` file with your configuration:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Default Recipient
DEFAULT_RECIPIENT=default-user@example.com

# File Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### 3. Email Setup (Gmail Example)

For Gmail, you'll need to:
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password in the `MAIL_PASSWORD` field

### 4. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## Usage

### Web Interface

1. **Main Page**: Visit `http://localhost:5000` for the main interface
2. **Upload Page**: Visit `http://localhost:5000/upload` for the upload form
3. **Status Check**: Visit `http://localhost:5000/status` for system health

### Webhook API

#### Endpoint: `POST /webhook`

**Parameters:**
- `file`: The file to upload (multipart/form-data)
- `content`: Optional text content/message
- `recipient`: Optional email recipient (defaults to DEFAULT_RECIPIENT)
- `subject`: Optional email subject

**Example using curl:**

```bash
curl -X POST http://localhost:5000/webhook \
  -F "file=@/path/to/your/document.pdf" \
  -F "content=This is an important document" \
  -F "recipient=user@example.com" \
  -F "subject=Document Upload"
```

**Example using Python requests:**

```python
import requests

url = 'http://localhost:5000/webhook'
files = {'file': open('document.pdf', 'rb')}
data = {
    'content': 'This is an important document',
    'recipient': 'user@example.com',
    'subject': 'Document Upload'
}

response = requests.post(url, files=files, data=data)
print(response.json())
```

## API Response Format

### Success Response
```json
{
    "success": true,
    "message": "File uploaded and email sent successfully",
    "filename": "20231201_143022_document.pdf",
    "recipient": "user@example.com"
}
```

### Error Response
```json
{
    "error": "Error message description"
}
```

## File Structure

```
mail-server/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── env.example        # Example environment configuration
├── README.md          # This file
├── uploads/           # Uploaded files directory (created automatically)
└── templates/         # HTML templates (if using web interface)
```

## Security Considerations

1. **Change the SECRET_KEY**: Always change the default secret key in production
2. **Secure Email Credentials**: Use environment variables for email credentials
3. **File Validation**: Only allowed file types are accepted
4. **File Size Limits**: Configure appropriate file size limits
5. **HTTPS**: Use HTTPS in production environments

## Troubleshooting

### Email Not Sending
- Check your email credentials in the `.env` file
- Verify SMTP settings for your email provider
- For Gmail, ensure you're using an App Password, not your regular password

### File Upload Issues
- Check file size limits
- Verify file type is in the allowed extensions list
- Ensure the uploads directory has write permissions

### Server Not Starting
- Verify all dependencies are installed
- Check that the `.env` file exists and is properly configured
- Ensure port 5000 is not already in use

## Development

To run in development mode with auto-reload:

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

## Production Deployment

For production deployment:

1. Set `FLASK_ENV=production`
2. Set `FLASK_DEBUG=False`
3. Use a production WSGI server like Gunicorn
4. Configure proper logging
5. Set up HTTPS
6. Use a proper database for file storage if needed

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
``` 