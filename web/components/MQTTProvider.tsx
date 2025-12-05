"use client";

import { createContext, useContext, useState, useEffect } from "react";

import { client } from "@/lib/mqtt";

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

type MQTTContextValue = {
  connected: boolean;
  latestSensorData: SensorData | null;
  latestRfidCheck: RfidCheck | null;
  doorStatus: DeviceStatus | null;
  windowStatus: DeviceStatus | null;
  fanStatus: DeviceStatus | null;
};

const MQTTContext = createContext<MQTTContextValue>({
  connected: false,
  latestSensorData: null,
  latestRfidCheck: null,
  doorStatus: null,
  windowStatus: null,
  fanStatus: null,
});

export function MQTTProvider({ children }: { children: React.ReactNode }) {
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
    };

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
        }
      } catch (error) {
        console.error("Error parsing message:", error);
      }
    };

    const handleDisconnect = () => {
      console.log("MQTT disconnected");
      setConnected(false);
    };

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

  const value: MQTTContextValue = {
    connected,
    latestSensorData,
    latestRfidCheck,
    doorStatus,
    windowStatus,
    fanStatus,
  };
  return <MQTTContext.Provider value={value}>{children}</MQTTContext.Provider>;
}

export function useMQTT() {
  const context = useContext(MQTTContext);
  if (context === undefined) {
    throw new Error("useMQTT must be used within a MQTTProvider");
  }
  return context;
}
