"use client";

import { createContext, useContext, useState, useEffect } from "react";
import { client } from "@/lib/mqtt";

// Type definitions
export type SensorData = {
  sensor_type: "temperature" | "humidity" | "gas" | "motion";
  value?: number;
  unit?: string;
  detected?: boolean;
  timestamp: string;
};

export type RfidCheck = {
  card_id: string;
  timestamp: string;
};

export type DeviceStatus = {
  state: "open" | "closed" | "on" | "off";
  timestamp: string;
};

// Type definition for MQTT context value
type MQTTContextValue = {
  connected: boolean;
  latestSensorData: SensorData | null;
  latestRfidCheck: RfidCheck | null;
  doorStatus: DeviceStatus | null;
  windowStatus: DeviceStatus | null;
  fanStatus: DeviceStatus | null;
  publishMessage: (topic: string, message: object) => void;
};

// Context for MQTT provider
const MQTTContext = createContext<MQTTContextValue>({
  connected: false,
  latestSensorData: null,
  latestRfidCheck: null,
  doorStatus: null,
  windowStatus: null,
  fanStatus: null,
  publishMessage: () => {},
});

// MQTT Provider component
export function MQTTProvider({ children }: { children: React.ReactNode }) {
  // State variables
  const [connected, setConnected] = useState(false);
  const [latestSensorData, setLatestSensorData] = useState<SensorData | null>(
    null
  );
  const [latestRfidCheck, setLatestRfidCheck] = useState<RfidCheck | null>(
    null
  );
  const [doorStatus, setDoorStatus] = useState<DeviceStatus | null>(null);
  const [windowStatus, setWindowStatus] = useState<DeviceStatus | null>(null);
  const [fanStatus, setFanStatus] = useState<DeviceStatus | null>(null);

  // Function to publish messages to MQTT broker
  const publishMessage = (topic: string, message: object) => {
    client.publish(topic, JSON.stringify(message), (err) => {
      if (err) {
        console.error("Error publishing message:", err);
      } else {
        console.log("Message published to topic:", topic);
      }
    });
  };

  // Effect to handle MQTT connection and message handling
  useEffect(() => {
    const deviceId = "esp32_main";
    const handleConnect = () => {
      console.log("Connected to MQTT broker");
      setConnected(true);

      client.subscribe(`devices/${deviceId}/data`, (err) => {
        if (err) console.error("Error subscribing to data topic:", err);
      });

      client.subscribe(`devices/${deviceId}/rfid/check`, (err) => {
        if (err) console.error("Error subscribing to rfid check topic:", err);
      });

      client.subscribe(`devices/${deviceId}/status/#`, (err) => {
        if (err) console.error("Error subscribing to status topic:", err);
      });

      client.subscribe(`devices/${deviceId}/response/status`, (err) => {
        if (err)
          console.error("Error subscribing to response status topic:", err);
      });

      setTimeout(() => {
        publishMessage(`devices/${deviceId}/request/status`, {
          requestId: Date.now().toString(),
          timestamp: new Date().toISOString(),
        });
      }, 200);
    };

    // Function to handle incoming messages from MQTT broker
    const handleMessage = (topic: string, message: Buffer) => {
      try {
        const data = JSON.parse(message.toString());
        console.log("Received message on topic:", topic, data);

        if (topic.endsWith("/data")) {
          setLatestSensorData(data);
        } else if (topic.endsWith("/rfid/check")) {
          setLatestRfidCheck(data);
        } else if (topic.endsWith("/status/door")) {
          setDoorStatus(data);
        } else if (topic.endsWith("/status/window")) {
          setWindowStatus(data);
        } else if (topic.endsWith("/status/fan")) {
          setFanStatus(data);
        } else if (topic.endsWith("/response/status")) {
          if (data.fan) setFanStatus(data.fan);
          if (data.door) setDoorStatus(data.door);
          if (data.window) setWindowStatus(data.window);
          console.log("Status updated from response:", data);
        }
      } catch (error) {
        console.error("Error parsing message:", error);
      }
    };

    // Function to handle disconnection from MQTT broker
    const handleDisconnect = () => {
      console.log("MQTT disconnected");
      setConnected(false);
    };

    // Function to handle errors from MQTT broker
    const handleError = (error: Error) => {
      console.error("MQTT error:", error);
      setConnected(false);
    };
    // Register handlers
    client.on("connect", handleConnect);
    client.on("message", handleMessage);
    client.on("close", handleDisconnect);
    client.on("error", handleError);

    // Cleanup when component unmounts
    return () => {
      client.off("connect", handleConnect);
      client.off("message", handleMessage);
      client.off("close", handleDisconnect);
      client.off("error", handleError);
    };
  }, []);

  // Value to be passed to the context provider
  const value: MQTTContextValue = {
    connected,
    latestSensorData,
    latestRfidCheck,
    doorStatus,
    windowStatus,
    fanStatus,
    publishMessage,
  };
  return <MQTTContext.Provider value={value}>{children}</MQTTContext.Provider>;
}

// Hook to use MQTT context
export function useMQTT() {
  const context = useContext(MQTTContext);
  if (context === undefined) {
    throw new Error("useMQTT must be used within a MQTTProvider");
  }
  return context;
}
