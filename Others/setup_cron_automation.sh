#!/bin/bash

# Setup cron automation for requirements documentation
# This script sets up a cron job to automatically update requirements documentation

echo "🔄 Setting up cron automation for requirements documentation..."

# Get the absolute path of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTO_UPDATE_SCRIPT="$SCRIPT_DIR/auto_update_requirements.sh"

# Make sure the auto-update script is executable
chmod +x "$AUTO_UPDATE_SCRIPT"

# Create a temporary file for the cron job
TEMP_CRON=$(mktemp)

# Add the cron job (runs every day at 9 AM)
echo "0 9 * * * cd $SCRIPT_DIR && $AUTO_UPDATE_SCRIPT >> $SCRIPT_DIR/cron.log 2>&1" > "$TEMP_CRON"

# Add the cron job to the user's crontab
crontab "$TEMP_CRON"

# Clean up
rm "$TEMP_CRON"

echo "✅ Cron job set up successfully!"
echo "📅 The requirements documentation will be automatically updated every day at 9 AM"
echo "📝 Logs will be saved to: $SCRIPT_DIR/cron.log"
echo ""
echo "To view the cron job:"
echo "  crontab -l"
echo ""
echo "To remove the cron job:"
echo "  crontab -r" 