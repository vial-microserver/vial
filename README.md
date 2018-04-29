# NodeMCU Relay Control
Micropython script to work as a http server to control nodemcu pins.

ESP8266 doesn't come with a web framework. So I had to repurpose the http_webserver example
script to control the GPIO pins.

## Example usage
To make pin 2 output and switch it on, send get request to http://<ip-address-of-nodemcu>/write/2/on
