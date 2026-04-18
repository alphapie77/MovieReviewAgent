# API Key Setup

## Quick Setup

1. **Copy template:**
   ```bash
   copy .env.template .env
   ```

2. **Edit .env file and add your Google API key:**
   ```
   GOOGLE_API_KEY=your_actual_key_here
   ```

3. **Get API Key:**
   - Visit: https://makersuite.google.com/app/apikey
   - Create new API key
   - Copy and paste into .env file

## Important Notes

- Phase 4 uses Phase 3's backend
- The .env file in `03_Phase3_MultiAgent/` is the main one
- You can also create .env here, it will be loaded by the backend
- **Never commit .env file to git** (already in .gitignore)

## Verify Setup

Run this to test:
```bash
cd 04_Phase4_WebInterface
python test_backend.py
```

If you see "Backend integration test passed", your API key is working!
