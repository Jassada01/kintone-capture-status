# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Python bot that automates capturing screenshots of Status history from Kintone records. The bot logs into Kintone, retrieves records from a specified App ID, clicks on Status history for each record, and saves screenshots with the record ID as filename.

## Environment Setup

The project uses a `.env` file for configuration. Required environment variables:
- `KINTONE_DOMAIN`: Your Kintone domain (e.g., xxx.cybozu.com)
- `KINTONE_USERNAME`: Kintone username
- `KINTONE_PASSWORD`: Kintone password
- `KINTONE_APP_ID`: The App ID to capture status from

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

## Architecture

The project consists of modular components:

- **main.py**: Entry point that orchestrates the workflow
- **kintone_client.py**: Handles Kintone API authentication and record retrieval
- **browser_automation.py**: Selenium/Playwright automation for browser interactions
- **screenshot_manager.py**: Screenshot capture and file saving logic
- **screenshots/**: Output directory for captured images (named as `record_{ID}.png`)

### Workflow
1. Load credentials from .env
2. Authenticate with Kintone API
3. Fetch all records from specified App ID
4. For each record:
   - Open record detail page in browser
   - Click Status history button
   - Wait for content to load
   - Capture screenshot
   - Save to screenshots/ directory
5. Clean up and report results
