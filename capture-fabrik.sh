#!/bin/bash

# Navigate Safari and take screenshots using AppleScript

osascript <<'EOF'
tell application "Safari"
    activate
    
    # Wait for page to load
    delay 2
    
    # Get the URL of the front window
    set currentURL to URL of current tab of window 1
    
    # If not on the right page, navigate there
    if currentURL does not contain "fabrik-madrid-tables" then
        set URL of current tab of window 1 to "https://emilianoechevarriafever.github.io/fabrik-madrid-tables/"
        delay 3
    end if
    
    # Scroll to top
    do JavaScript "window.scrollTo(0, 0);" in current tab of window 1
    delay 1
end tell

# Take screenshot of Safari window
screencapture -l$(osascript -e 'tell app "Safari" to id of window 1') /Users/emiliano.echevarria@feverup.com/Documents/GitHub/fabrik-madrid-tables/screenshot-1-top.png

# Scroll to map section
osascript -e 'tell application "Safari" to do JavaScript "window.scrollTo(0, 400);" in current tab of window 1'
sleep 1

screencapture -l$(osascript -e 'tell app "Safari" to id of window 1') /Users/emiliano.echevarria@feverup.com/Documents/GitHub/fabrik-madrid-tables/screenshot-2-map.png

# Scroll to ticket selector
osascript -e 'tell application "Safari" to do JavaScript "window.scrollTo(0, 800);" in current tab of window 1'
sleep 1

screencapture -l$(osascript -e 'tell app "Safari" to id of window 1') /Users/emiliano.echevarria@feverup.com/Documents/GitHub/fabrik-madrid-tables/screenshot-3-tickets.png

# Get page state information via JavaScript
osascript <<'INNER_EOF'
tell application "Safari"
    set selectedTab to do JavaScript "
        var pill = document.querySelector('.ticket-pill.active');
        pill ? pill.textContent.trim() : 'None';
    " in current tab of window 1
    
    set blueZones to do JavaScript "
        var blues = [];
        document.querySelectorAll('.map-zone.active').forEach(function(el) {
            blues.push(el.getAttribute('data-zone'));
        });
        var pistaActive = document.getElementById('pistaGroup') && document.getElementById('pistaGroup').classList.contains('active');
        if (pistaActive) blues.push('pistaGroup');
        blues.join(', ') || 'None';
    " in current tab of window 1
    
    return "Selected Tab: " & selectedTab & "\nBlue Zones: " & blueZones
end tell
INNER_EOF

EOF

echo "Screenshots saved to:"
echo "- screenshot-1-top.png"
echo "- screenshot-2-map.png"
echo "- screenshot-3-tickets.png"
