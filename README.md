# Weekend Explorer

Weekend Explorer is a Reflex-based web application with Google OAuth login.

## Prerequisites

- Python 3.8 or higher
- pip

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:

   Create a `.env` file in the root directory:
   ```
   GOOGLE_CLIENT_ID=your-google-client-id
   GOOGLE_CLIENT_SECRET=your-google-client-secret
   GOOGLE_REDIRECT_URI=http://localhost:3000/auth/google/callback
   SECRET_KEY=your-secret-key
   ```

   Or set them in PowerShell:
   ```powershell
   $env:GOOGLE_CLIENT_ID = "your-google-client-id"
   $env:GOOGLE_CLIENT_SECRET = "your-google-client-secret"
   $env:GOOGLE_REDIRECT_URI = "http://localhost:3000/auth/google/callback"
   ```

## Running the Application

Start the Reflex application:

```bash
reflex run
```

The application will be available at `http://localhost:3000`

## Development

For development mode with auto-reload:

```bash
reflex run --loglevel debug
```

## Project Structure

```
app/
├── __init__.py          # Reflex app initialization
├── config.py            # Configuration (Google OAuth, DB)
├── models.py            # Database models (User)
├── state.py             # Reflex state management
├── routes.py            # Route definitions
└── pages/
    └── home.py          # Home page
```

