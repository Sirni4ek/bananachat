import os

# Path to the directory with the messages
messages_dir = "messages"

# Get the list of text files in the messages directory
files = [f for f in os.listdir(messages_dir) if f.endswith(".txt")]

# Sort files alphabetically for consistent ordering
files.sort()

# Start the HTML structure
html_content = '''
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
    </style>
</head>
<body>
    <div class="chat-container">
'''

# Loop through each file, read its content, and add it to the HTML
for idx, file_name in enumerate(files):
    with open(os.path.join(messages_dir, file_name), "r") as file:
        message_content = file.read().strip()
        
        # Determine message style
        message_class = "user-message" if idx % 2 == 0 else "other-message"
        
        # Add the message to the HTML content
        html_content += f'<div class="message {message_class}">{message_content}</div>\n'

# Close the HTML structure
html_content += '''
    </div>
</body>
</html>
'''

# Write the HTML content to a file
with open("chat_interface.html", "w") as html_file:
    html_file.write(html_content)

print("Chat interface generated as 'chat_interface.html'")

