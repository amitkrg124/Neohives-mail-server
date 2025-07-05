from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
from flask_mail import Mail, Message
import logging
from datetime import datetime
from dotenv import load_dotenv
import os  # This is the missing import
# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Email configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Default recipient email
DEFAULT_RECIPIENT = os.getenv('DEFAULT_RECIPIENT')

# Initialize Flask-Mail
mail = Mail(app)

def send_email(recipient, subject, content):
    """Send email."""
    try:
        msg = Message(
            subject=subject,
            sender=app.config['MAIL_USERNAME'],
            recipients=[recipient]
        )
        
        msg.body = content
        
        mail.send(msg)
        logger.info(f"Email sent successfully to {recipient}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint for content."""
    try:
        content = request.form.get('content', '')
        recipient = request.form.get('recipient', DEFAULT_RECIPIENT)
        subject = request.form.get('subject', 'Notification')

        # Prepare email content for main notification
        email_content = f"""
Web Hook Details

Content: {content}
        """.strip()

        # Send main notification to DEFAULT_RECIPIENT
        main_sent = send_email(DEFAULT_RECIPIENT, subject, email_content)

        # Send confirmation to recipient if different from DEFAULT_RECIPIENT
        confirmation_sent = True
        if recipient and recipient != DEFAULT_RECIPIENT:
            confirmation_content = f"""
Hello,

Your request has been received and processed.

Content: {content}

Thank you.
            """.strip()
            confirmation_sent = send_email(recipient, "Confirmation: " + subject, confirmation_content)

        if main_sent and confirmation_sent:
            return jsonify({
                'success': True,
                'message': 'Emails sent successfully',
                'recipient': recipient,
                'default_recipient': DEFAULT_RECIPIENT
            }), 200
        else:
            return jsonify({'error': 'Failed to send one or more emails'}), 500

    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/send', methods=['GET', 'POST'])
def send():
    """Web interface for sending emails."""
    if request.method == 'POST':
        try:
            content = request.form.get('content', '')
            recipient = request.form.get('recipient', DEFAULT_RECIPIENT)
            subject = request.form.get('subject', 'Notification')
            
            # Prepare email content
            email_content = f"""
Notification

Content: {content}

Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This is an automated notification from the system.
            """.strip()
            
            # Send email
            if send_email(recipient, subject, email_content):
                flash('Email sent successfully!', 'success')
            else:
                flash('Failed to send email', 'warning')
            
            return redirect(url_for('send'))
                
        except Exception as e:
            logger.error(f"Send error: {str(e)}")
            flash('An error occurred while sending email', 'error')
            return redirect(request.url)
    
    return render_template('send.html')

@app.route('/status')
def status():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'default_recipient': DEFAULT_RECIPIENT
    })                                                    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)