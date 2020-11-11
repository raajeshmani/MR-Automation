#!bin/zsh
# I make Raajesh's life easier 
#
#
# $ source .zshrc
#
# to update the commands after editing

# Use this command and if DefaultUser is set leave the 2nd line blank .. else replace with username
# cat .anyconnect 
function connect-vpn() {
    /opt/cisco/anyconnect/bin/vpn -s connect vpn.cerner.com <<"EOF"

<<PASSWORD>>
y
EOF
}

function disconnect-vpn() {
    /opt/cisco/anyconnect/bin/vpn -s disconnect vpn.cerner.com
}

function iced-coffee() {
    # Compiles, builds JS & Server on a new terminal window on each tab
    osascript -e 'tell application "Terminal"' -e 'activate' -e 'do script' -e 'do script "cd ~/Careaware/connect-messenger-js && npm run compile:watch" in front window' -e 'tell application "System Events" to keystroke "t" using {command down}' -e 'delay 0.2' -e 'do script "cd ~/Careaware/blackcomb_server && npm run build:watch" in front window' -e 'end tell'
    # Play some Music
    osascript -e 'tell application "Spotify"' -e 'activate' -e 'tell application "System Events" to key code 49' -e 'end tell'
    # Get the VPN up & running for pass & verification
    connect-vpn
    # Restart the server in RubyMine
    osascript -e 'tell application "RubyMine"' -e 'activate' -e 'tell application "System Events" to key code 120 using {command down}' -e 'delay 2' -e 'tell application "System Events" to keystroke "r" using {control down}' -e 'end tell'
}

function magic-birthday-pill() {
    cd ~/raajesh-git/Python-Automation-
    python3 ~/raajesh-git/Python-Automation-/setBirthdayToCalendar.py
}

# Make Me A - fn for scaling

function makeMeA() {
    if [ "$1" = "iced-coffee" ]
    then 
        cat ~/raajesh-git/Python-Automation-/assets/greet.txt
        $1
    else
        $1
    fi
}

# Cd into working directories

function cm() {
    cd ~/Careaware/connect-messenger-js 
}

function bc() {
	cd ~/Careaware/blackcomb_server
}

