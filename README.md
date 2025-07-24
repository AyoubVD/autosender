# WhatsApp Message Scheduler API

This project is a FastAPI backend for scheduling and sending WhatsApp messages, with a Node.js service for WhatsApp integration.

## Features
- Manage recipients (CRUD)
- Send WhatsApp messages from your own account
- SQLite database for storage

## Requirements
- Python 3.10+
- Node.js 16+
- WhatsApp account (for integration)

## Setup

### 1. Clone the repository
```bash
git clone <repo-url>
cd autosender
```

### 2. Python Backend
```bash
cd backend
pip install -r requirements.txt
```

### 3. Node.js WhatsApp Service
```bash
npm install
```

Create a file `whatsapp-service/index.js` with the following content:
```js
const { create } = require('@open-wa/wa-automate');
const express = require('express');
const app = express();
app.use(express.json());

create().then(client => {
  app.post('/send', async (req, res) => {
    const { to, message } = req.body;
    try {
      await client.sendText(to, message);
      res.send({ status: 'success' });
    } catch (err) {
      res.status(500).send({ status: 'error', error: err.toString() });
    }
  });

  app.listen(3001, () => console.log('WhatsApp API listening on port 3001'));
});
```

Start the service:
```bash
node whatsapp-service/index.js
```
Scan the QR code with your WhatsApp app.

### 4. Run the FastAPI Backend
```bash
uvicorn backend.main:app --reload
```

## Usage
- Use the `/recipients/` endpoints to manage recipients.
- Use the `/send_whatsapp/` endpoint to send a WhatsApp message:
  - `to`: WhatsApp number in international format (e.g., `+1234567890`)
  - `message`: The message text

## Troubleshooting
- Ensure the Node.js WhatsApp service is running and connected (QR code scanned).
- Check logs in both the FastAPI and Node.js services for errors.
- Make sure ports 8000 (FastAPI) and 3001 (Node.js) are open and not blocked.

## License
MIT
