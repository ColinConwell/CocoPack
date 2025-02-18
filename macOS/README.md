## Scripts for MacOS Automation

### AppleScript Tools

#### rsync_selected.scpt
A Finder integration script that enables easy file synchronization using rsync. This script:

- Can be triggered from Finder with selected files/folders
- Allows syncing to either:
  - Local destinations
  - Remote SSH destinations (automatically detects hosts from ~/.ssh/config)
- Features:
  - Interactive destination selection
  - Directory path input
  - Secure file transfer using rsync
  - Preserves file attributes (-a flag)
  - Verbose output (-v flag)
  - Requires admin privileges for execution

##### Usage:
1. Select files/folders in Finder
2. Run the script
3. Choose destination type (Local or SSH host)
4. Enter target directory path
5. Enter admin password when prompted

##### Installation:
1. Save the script in `~/Library/Scripts/Finder/` for Finder integration
2. Enable Scripts menu in Finder preferences if not already enabled

Note: For remote destinations, ensure your SSH config file (~/.ssh/config) is properly configured with your host entries.

