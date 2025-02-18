on run {input, parameters}
	if input is {} then
		display dialog "Please select a Keynote file" buttons {"OK"} default button "OK" with icon stop
		return
	end if
	
	-- Get input Keynote file path
	set inputPath to POSIX path of (item 1 of input)
	
	-- Create output folder path (same name as keynote file but as a folder)
	set inputFileName to text 1 thru ((offset of "." in inputPath) - 1) of inputPath
	set outputPath to inputFileName & "_slides"
	
	-- Create the output directory if it doesn't exist
	do shell script "mkdir -p " & quoted form of outputPath
	
	try
		tell application "Keynote"
			-- Open the document
			set theDocument to open inputPath
			set documentName to the name of theDocument
			
			-- Convert POSIX path to HFS path for Keynote
			set targetFolderHFSPath to POSIX file outputPath as string
			
			-- Export slides as PNG images
			export theDocument as slide images to file targetFolderHFSPath with properties {image format:PNG, skipped slides:false}
			
			-- Clean up
			close theDocument
		end tell
		
		-- Show success message with output location
		display dialog "Slides exported successfully to:" & return & return & outputPath buttons {"OK"} default button "OK" with icon note
		
	on error errorMessage
		-- Show error message if something goes wrong
		display dialog "Error: " & errorMessage buttons {"OK"} default button "OK" with icon stop
	end try
	
	return input
end run
