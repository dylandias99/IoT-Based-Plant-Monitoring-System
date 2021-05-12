#define light A1
#define moist A0
#define led 13
#include "DHT.h"

#define DHTPIN 8    
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

String command1 = "CONNECT";
String command2 = "PUMP";
String var;
String ack = "ACKNOWLEDGE";

void setup() {
  Serial.begin(9600);
  pinMode(light,INPUT);
  digitalWrite(led, LOW);
  dht.begin();
}

void loop() {
 if(Serial.available() > 0){
  var = Serial.readStringUntil("/r");
   if(var == command1){
    float lig = analogRead(light); 
    float lig_map = map(lig,0, 1023,0, 100);
    Serial.println(lig_map);
    delay(1000); 
    Serial.println(ack);
    float temp = dht.readTemperature(); 
    Serial.println(temp);
    delay(1000); 
    Serial.println(ack);
    float hum = dht.readHumidity(); 
    Serial.println(hum);
    delay(1000); 
    Serial.println(ack);
    float moist = analogRead(A0); 
    float moist_map = map(moist,0,1023,0,100); 
    Serial.println(moist_map);
    delay(1000); 
    Serial.println(ack);
  }
  else if (var == command2){
    digitalWrite(led, HIGH);
    delay(1000); 
    Serial.println(ack);
    }
 }
}
