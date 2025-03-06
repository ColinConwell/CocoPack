tell application "Microsoft PowerPoint"
    open "{input_path}"
    set thePresentation to active presentation
    
    set slideCount to count of slides in thePresentation
    repeat with i from 1 to slideCount
        set current slide of thePresentation to slide i of thePresentation
        set slideFile to "{output_path}/Slide" & i & ".png"
        save thePresentation in slideFile as save as PNG
    end repeat
    
    close thePresentation saving no
end tell