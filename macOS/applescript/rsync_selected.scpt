on run {input, parameters}
	-- Convert input paths to POSIX paths
	set filePaths to ""
	repeat with i from 1 to count of input
		set filePaths to filePaths & quoted form of POSIX path of (item i of input) & " "
	end repeat
	
	-- Show destination selection dialog
	set destinationList to {"Local"}
	try
		set sshConfigFile to (POSIX path of (path to home folder)) & ".ssh/config"
		-- Exclude lines starting with "Host *"
		set configContents to do shell script "awk '/^Host / && $2 !~ /^[*]/ {print $2}' " & sshConfigFile
		set destinationList to destinationList & (paragraphs of configContents)
	end try
	
	set chosenDestination to (choose from list destinationList with prompt "Select a Destination:" default items {"Local"})
	if chosenDestination is false then return -- User canceled
	
	set chosenDirectory to text returned of (display dialog "Enter the Directory Path on the Destination:" default answer "")
	
	-- Build rsync command
	set rsyncCommand to "/usr/bin/rsync -av " & filePaths
	if chosenDestination = {"Local"} then
		set rsyncCommand to rsyncCommand & quoted form of chosenDirectory
	else
		set rsyncCommand to rsyncCommand & chosenDestination & ":" & quoted form of chosenDirectory
	end if
	
	-- Execute rsync command
	do shell script rsyncCommand with administrator privileges
	
	return input
end run