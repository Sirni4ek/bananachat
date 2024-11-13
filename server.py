import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

# Directory to store message files
messages_dir = "messages"

# Create the messages directory if it doesn't exist
if not os.path.exists(messages_dir):
    os.makedirs(messages_dir)

# HTML template with a form to add new messages
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat Interface</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            background-color: #f5f5f5;
            margin: 0;
            padding: 20px;
        }
        .chat-container {
            max-width: 500px;
            width: 100%;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.2);
            padding: 20px;
            overflow: hidden;
        }
        .message {
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 15px;
            display: inline-block;
            max-width: 80%;
        }
        .user-message {
            background-color: #d1e7dd;
            align-self: flex-start;
        }
        .other-message {
            background-color: #e2e3e5;
            align-self: flex-end;
        }
        .message-form {
            margin-top: 20px;
            display: flex;
            flex-direction: column;
        }
        .message-form textarea {
            resize: none;
            padding: 10px;
            font-size: 1rem;
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .message-form button {
            margin-top: 10px;
            padding: 10px;
            font-size: 1rem;
            border: none;
            border-radius: 5px;
            background-color: #007bff;
            color: white;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        {messages}
        
        <!-- Form to add a new message -->
        <form action="/" method="post" class="message-form">
            <textarea name="message" rows="3" placeholder="Write a new message..." required></textarea>
            <button type="submit">Send</button>
        </form>
    </div>
</body>
</html>
'''

# Helper function to load messages from text files
def load_messages():
    files = sorted([f for f in os.listdir(messages_dir) if f.endswith(".txt")])
    messages = []
    for idx, file_name in enumerate(files):
        with open(os.path.join(messages_dir, file_name), "r") as file:
            message_content = file.read().strip()
            # Alternating message classes for a chat effect
            message_class = "user-message" if idx % 2 == 0 else "other-message"
            messages.append(f'<div class="message {message_class}">{message_content}</div>')
    return "\n".join(messages)

# Custom HTTP request handler
class ChatHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle GET request to display the chat interface
        if self.path == "/":
            messages_html = load_messages()
            html_content = HTML_TEMPLATE.format(messages=messages_html)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content.encode("utf-8"))
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        # Handle POST request to add a new message
        if self.path == "/":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            message_data = urllib.parse.parse_qs(post_data.decode('utf-8'))
            new_message = message_data.get("message", [""])[0].strip()

            if new_message:
                # Save the new message to a new text file
                message_count = len(os.listdir(messages_dir)) + 1
                file_path = os.path.join(messages_dir, f"text{message_count}.txt")
                with open(file_path, "w") as f:
                    f.write(new_message)

            # Redirect to the main page to show updated messages
            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()

# Function to start the server
def run(server_class=HTTPServer, handler_class=ChatHTTPRequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Serving on port {port}...")
    httpd.serve_forever()

# Start the server
if __name__ == "__main__":
    run()

