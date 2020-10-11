#!bin/zsh
# I make Raajesh's life easier 
#
#
# $ source .zshrc
#
# to update the commands after editing

function iced-coffee() {
    # Compiles, builds JS & Server on a new terminal window on each tab
    osascript -e 'tell application "Terminal"' -e 'activate' -e 'do script' -e 'do script "cd ~/Careaware/connect-messenger-js && npm run compile:watch" in front window' -e 'tell application "System Events" to keystroke "t" using {command down}' -e 'delay 0.2' -e 'do script "cd ~/Careaware/blackcomb_server && npm run build:watch" in front window' -e 'end tell'
    # Play some Music
    osascript -e 'tell application "Spotify"' -e 'activate' -e 'tell application "System Events" to key code 49' -e 'end tell'
    # Get the VPN up & running for pass & verification
    osascript -e 'tell application "Cisco AnyConnect Secure Mobility Client"' -e 'activate' -e 'delay 18' -e 'end tell'
    # Restart the server in RubyMine
    osascript -e 'tell application "RubyMine"' -e 'activate' -e 'tell application "System Events" to key code 120 using {command down}' -e 'delay 2' -e 'tell application "System Events" to keystroke "r" using {control down}' -e 'end tell'
}

# Make Me A - fn for scaling
# cerner_2^5_2020

function makeMeA() {
    if [ "$1" = "iced-coffee" ]
    then 
        cat ~/raajesh-git/Python-Automation-/assets/greet.txt
        $1
    fi
}