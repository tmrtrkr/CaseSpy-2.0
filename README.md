CaseSpy-2.0 is updated version of CaseSpy. It is a tool to cheat in online exams without being detected. It apply OCR on a taken screen shot of a question and sends it to the LLM providers API' (grok and chatgpt).
It consist of PC server service which is CaseSpy and an Android Client to send request to this. Note: This project is created to demonstrate how online exams and testa are vulnerable to OS level apps that works with
3rd party apps.

Installation:
1) Clone the repo
2) Clone the mobile App client Repo
3) Install the android app to your phone
4) Install the dependencies: openai,flask,flask_cors,pathlib,PIL,customtkinter,tkinter,pytesseract,numpy
5) Be sure the firewall is off
6) Add tcp/Ip inbound rule for any ip for port 5000
7) Be sure that your mobile phone and your pc is in the same wifi network
8) Run the main.py and go to the ip that is written in the console via an web explorer
9) Write the ip to the related field in the mobile app and press apply button
10) Configure the screenshot window or windows x1,y1(top left) x2,y2(bottom right
11) Use the mobile app to take screen shot
12) enter your grok or openai API key to CaseSpy UI in your pc
13) Select the related LLM that you will use
14) You can send the screenshot with the related button on your mobile UI
15) done.
