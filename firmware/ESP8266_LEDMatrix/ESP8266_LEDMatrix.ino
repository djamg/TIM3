#include <NTPClient.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>
#include <ESP8266HTTPClient.h>
#include <ArduinoJson.h>
#include <Arduino_JSON.h>

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW //PAROLA_HW
#define MAX_DEVICES 4
#define CLK_PIN D5  // or SCK
#define DATA_PIN D7 // or MOSI
#define CS_PIN D8   // or SS
MD_Parola P = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

#define WLAN_SSID "ERROR2"
#define WLAN_PASS "n150wireless"

String serverName = "http://869b504f4449.ngrok.io/api/list";

WiFiClient client;
WiFiUDP ntpUDP;
const long utcOffsetInSeconds = 19800;
NTPClient timeClient(ntpUDP, "aaaa", utcOffsetInSeconds);

textEffect_t scrollEffect = PA_SCROLL_LEFT;
textPosition_t scrollAlign = PA_LEFT; // how to align the text
int scrollPause = 0;
int scrollSpeed = 0;
char curMessage[75] = {"IoT Countdown Timer"};
long finalTime = 0;
long currentTimeStamp = 0;

void setup()
{

  Serial.begin(115200);
  P.begin();
  P.setTextAlignment(PA_CENTER);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  P.print("By AMG");
  delay(300);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
    P.print("Booting");
  }
  P.print("WifiOK");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  timeClient.begin();
}

void loop()
{
  long epochTime = timeClient.getEpochTime();
  if (WiFi.status() == WL_CONNECTED)
  { //Check WiFi connection status

    HTTPClient http; //Declare an object of class HTTPClient

    http.begin(serverName);    //Specify request destination
    int httpCode = http.GET(); //Send the request

    if (httpCode > 0)
    { //Check the returning code

      String payload = http.getString(); //Get the request response payload
      Serial.println(payload);           //Print the response payload
      JSONVar myObject = JSON.parse(payload);
      Serial.println(myObject);
      finalTime = myObject["time_end"];
      currentTimeStamp = myObject["timestamp"];
      Serial.print("finalTime: ");
      Serial.println(finalTime);
      Serial.print("NTPEpochTime: ");
      Serial.println(epochTime);
    }

    http.end(); //Close connection

    timeDifference(finalTime, currentTimeStamp);
  }

  delay(35000); //Send a request every 30 seconds
}

int timeDifference(long a, long b)
{
  long c = a - b;
  Serial.print("timeDifference: ");
  Serial.println(c);
  secondsToHM(c);
}

long secondsToHM(long epochTime)
{
  if (epochTime > 0)
  {
    int hours = epochTime / 3600;
    int mins1 = epochTime % 3600;
    int mins2 = mins1 / 60;
    String led = String(hours, DEC) + ":" + String(mins2, DEC);
    Serial.print("secondsToHM");
    Serial.print(hours);
    Serial.print(":");
    Serial.println(mins2);
    Serial.println(led);
    P.print(led);
  }
  else
  {
    Serial.println("No Events");
    P.print("CHILL");
  }
  //return ;
}
