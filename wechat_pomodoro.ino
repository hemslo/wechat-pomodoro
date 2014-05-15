#include <SPI.h>
#include <HttpClient.h>
#include <Ethernet.h>
#include <EthernetClient.h>
#include "utility/stringbuffer.h"
#include "aJSON.h"


// Name of the server we want to connect to
const char kHostname[] = "api.dotide.com";

const IPAddress kIPAddress(112, 124, 43, 232);

const char kPath[] = "/v1/wechat-pomodoro/datastreams/n";

const char kToken[] = "Bearer 61e13e47ed0b1b6f6a0ebe598d5ddba0c386a0d856487ec84e973d06b1848220";

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };

// EthernetClient client;
// char payload[100] = {};

boolean counted = false;
int i = 0;

int start_time = 0;

int buzzPin =  3;    //Connect Buzzer on Digital Pin3

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
  pinMode(buzzPin, OUTPUT);

  while (Ethernet.begin(mac) != 1) {
    Serial.println("Error getting IP address via DHCP, trying again...");
    delay(15000);
  }
  Serial.println("Start");
}

void loop() {
  if (counted) {
    if(millis() - start_time > 10000) {
      digitalWrite(buzzPin, HIGH);
      delay(1);
      digitalWrite(buzzPin, LOW);
      delay(1);
    }
  } else {
    int err =0;
    EthernetClient c;
    HttpClient http(c);
    http.beginRequest();
    err = http.get(kIPAddress ,kHostname, kPath);
    http.sendHeader("Authorization", kToken);
    http.endRequest();

    if (err == 0) {
      Serial.println("startedRequest ok");

      err = http.responseStatusCode();
      if (err >= 0) {
        Serial.print("Got status code: ");
        Serial.println(err);

        err = http.skipResponseHeaders();
        if (err >= 0) {
          int bodyLen = http.contentLength();
          Serial.print("Content length is: ");
          Serial.println(bodyLen);
          Serial.println();
          Serial.println("Body returned follows:");

          char ch;
          char buff[300] = {};
          i = 0;
          // Whilst we haven't timed out & haven't reached the end of the body
          while ( http.connected() || http.available() ) {
            if (http.available()) {
              ch = http.read();
              Serial.print(ch);
              buff[i] = ch;
              i += 1;
            }
          }
          Serial.println();
          aJsonObject* root = aJson.parse(buff);
          aJsonObject* v = aJson.getObjectItem(root, "current_v");
          Serial.println("v");
          Serial.println(v->valueint);
          if (v->valueint > 1) {
            counted = true;
            start_time = millis();
          }

          for(int ai=0; ai<300; ai++){
              buff[ai] = 0;
          }
        } else {
          Serial.print("Failed to skip response headers: ");
          Serial.println(err);
        }
      } else {
        Serial.print("Getting response failed: ");
        Serial.println(err);
      }
    } else {
      Serial.print("Connect failed: ");
      Serial.println(err);
    }

    http.stop();

    Serial.println("finish");
  }
  // aJsonObject *root;
  // root = aJson.createObject();
  // aJson.addNumberToObject(root, "v", 2);
  // sprintf(payload, "%s", aJson.print(root));
  // Serial.println(payload);
  // while(1){
  //     // statement
  // }
  // Serial.println(payload);

  // if(!postPage(serverName,serverPort,pageName,params)) Serial.print(F("Fail "));
}

// byte postPage(char* domainBuffer, int thisPort, char* page, char* thisData)
// {
//   int inChar;
//   char outBuf[64];

//   Serial.print(F("connecting..."));

//   if(client.connect(domainBuffer,thisPort))
//   {
//     Serial.println(F("connected"));

//     // send the header
//     sprintf(outBuf,"POST %s HTTP/1.1",page);
//     client.println(outBuf);
//     sprintf(outBuf,"Host: %s",domainBuffer);
//     client.println(outBuf);
//     client.println(F("Connection: close\r\nContent-Type: application/json"));
//     sprintf(outBuf,"Content-Length: %u\r\n",strlen(thisData));
//     client.println(outBuf);

//     // send the body (variables)
//     client.print(thisData);
//   }
//   else
//   {
//     Serial.println(F("failed"));
//     return 0;
//   }

//   int connectLoop = 0;

//   while(client.connected())
//   {
//     while(client.available())
//     {
//       inChar = client.read();
//       Serial.write(inChar);
//       connectLoop = 0;
//     }

//     delay(1);
//     connectLoop++;
//     if(connectLoop > 10000)
//     {
//       Serial.println();
//       Serial.println(F("Timeout"));
//       client.stop();
//     }
//   }

//   Serial.println();
//   Serial.println(F("disconnecting."));
//   client.stop();
//   return 1;
// }
