# WhatsApp Message Scheduler

## Project Structure

- `backend/` - FastAPI backend, scheduling, WhatsApp integration
- `frontend/` - (Optional) Web dashboard

## Setup (Backend)

1. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```sh
   pip install -r backend/requirements.txt
   ```
3. Run the FastAPI server:
   ```sh
   uvicorn backend.main:app --reload
   ```

Visit [http://localhost:8000](http://localhost:8000) to check the API is running.

---

## API Guide: Recipient Endpoints

You can interact with the API using tools like `curl`, Postman, or the built-in Swagger UI at [http://localhost:8000/docs](http://localhost:8000/docs).

### Create a Recipient
```sh
curl -X POST "http://localhost:8000/recipients/" \
     -H "Content-Type: application/json" \
     -d '{"name": "John Doe", "phone_number": "+1234567890"}'
```

### List All Recipients
```sh
curl "http://localhost:8000/recipients/"
```

### Get a Recipient by ID
```sh
curl "http://localhost:8000/recipients/1"
```

### Update a Recipient
```sh
curl -X PUT "http://localhost:8000/recipients/1" \
     -H "Content-Type: application/json" \
     -d '{"name": "Jane Doe"}'
```

### Delete a Recipient
```sh
curl -X DELETE "http://localhost:8000/recipients/1"
```

---

For more details and to try the API interactively, visit the [Swagger UI](http://localhost:8000/docs) after starting the server.
