sudo apt-get install ./kasmvncserver_*.deb

# Add your user to the ssl-cert group
sudo addgroup $USER ssl-cert

# YOU MUST DISCONNECT AND RECONNECT FOR GROUP MEMBERSHIP CHANGE TO APPLY

# start KasmVNC, you will be prompted to create a KasmVNC user and select a desktop environment
vncserver

# Tail the logs
tail -f ~/.vnc/*.log