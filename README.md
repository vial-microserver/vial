# NodeMCU Relay Control
Micropython script to work as a http server to control nodemcu pins.

ESP8266 doesn't come with a web framework. So I had to repurpose the http_webserver example
script to control the GPIO pins.

## Example usage
- To make pin 2 output and switch it on, send get request to http://*ip-address-of-nodemcu*/write/2/on
- To read from pin 2 with PULL_UP, send get request to http://*ip-address-of-nodemcu*/read/2?pull=up
- To measure from dht, http://*ip-address-of-nodemcu*/measure/2 (Returns two number separated by a comma)

## To Do
- Return json instead of text
- Confirm if the read process is not errenous

### Just so that I remember what I did
- Connect to nodemcu using picocom or micropython webrepl
- After nodemcu boots up, it will run boot.py followed by main.py
- You can send files to nodemcu as well using webrepl
- I have a raspberry pi zero which runs a single page webpage which sends ajax calls to this nodemcu
- since the pi zero runs pihole as well, i've set it up such that it runs on port 5000
- the webserver will start as soon as the pi zero is started (crontab @reboot)
