"use client";

import mqtt from "mqtt";

export const client = mqtt.connect(process.env.NEXT_PUBLIC_MQTT_BROKER!, {
  username: process.env.NEXT_PUBLIC_MQTT_USERNAME!,
  password: process.env.NEXT_PUBLIC_MQTT_PASSWORD!,
});

// setup the callbacks
client.on("connect", function () {
  console.log("Connected");
});

client.on("error", function (error) {
  console.log(error);
});
