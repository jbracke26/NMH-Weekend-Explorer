# NMH Weekend Explorer
## Quick Start 

1. Install Python 3.8+ if not already installed.

2. Open the project in VS Code.

3. Press `Cmd + J` to open the terminal.

4. Create virtual environment: `python3 -m venv venv`

5. Activate environment: `source venv/bin/activate`

6. Install dependencies: `pip install -r requirements.txt`

7. Create or populate `.env` file with your keys in thise style:

   GOOGLE_CLIENT_ID=...
   GOOGLE_CLIENT_SECRET=...
   GOOGLE_MAPS_API_KEY=...
   ADMIN_EMAILS=admin@nmhschool.org
   TEACHER_EMAILS=teacher@nmhschool.org


8. Run: `reflex run` - opens at http://localhost:3000
