"use client";

import { createContext, useContext, useState, useEffect, useRef } from "react";
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
  temperature: number | null;
  humidity: number | null;
  smartHomeStatus: boolean | null;
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
  temperature: null,
  humidity: null,
  smartHomeStatus: null,
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
  const [temperature, setTemperature] = useState<number | null>(null);
  const [humidity, setHumidity] = useState<number | null>(null);
  const [smartHomeStatus, setSmartHomeStatus] = useState<boolean | null>(null);

  // Track last time data was received from ESP32
  const lastDataReceivedRef = useRef<number | null>(null);
  const statusCheckIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const initialLoadTimeRef = useRef<number>(Date.now()); // Track when page loaded

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

  const updateDeviceStatus = () => {
    const now = Date.now();
    const timeSinceLoad = now - initialLoadTimeRef.current;
    const timeSinceData = lastDataReceivedRef.current
      ? now - lastDataReceivedRef.current
      : null;

    if (timeSinceData !== null && timeSinceData < 30000) {
      setSmartHomeStatus(true); // Online - recent data
    } else if (timeSinceData === null && timeSinceLoad < 30000) {
      setSmartHomeStatus(null); // Loading - waiting for first data
      // Clear sensor data while loading
      setTemperature(null);
      setHumidity(null);
      setDoorStatus(null);
      setWindowStatus(null);
      setFanStatus(null);
    } else {
      setSmartHomeStatus(false); // Offline - no data for 30s+
      // Clear sensor data when offline
      setTemperature(null);
      setHumidity(null);
      setDoorStatus(null);
      setWindowStatus(null);
      setFanStatus(null);
    }
  };

  // Effect to handle MQTT connection and message handling
  useEffect(() => {
    const deviceId = "esp32_main";

    const handleConnect = () => {
      setConnected(true);
      setSmartHomeStatus(null);

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
        if (err) console.error("Error subscribing to response status topic:", err);
      });

      // Request initial status on connect
      setTimeout(() => {
        publishMessage(`devices/${deviceId}/request/status`, {});
      }, 500);
    };

    const handleMessage = (topic: string, message: Buffer) => {
      try {
        const data = JSON.parse(message.toString());

        if (topic.startsWith("devices/esp32_main/")) {
          lastDataReceivedRef.current = Date.now();
          updateDeviceStatus();
        }

        if (topic.endsWith("/data")) {
          setLatestSensorData(data);

          // Extract temperature and humidity from real-time sensor data
          if (data.sensor_type === "temperature" && data.value !== undefined) {
            setTemperature(data.value);
          }
          if (data.sensor_type === "humidity" && data.value !== undefined) {
            setHumidity(data.value);
          }
        } else if (topic.endsWith("/rfid/check")) {
          setLatestRfidCheck(data);
        } else if (topic.endsWith("/status/door")) {
          setDoorStatus(data);
        } else if (topic.endsWith("/status/window")) {
          setWindowStatus(data);
        } else if (topic.endsWith("/status/fan")) {
          setFanStatus(data);
        } else if (topic.endsWith("/response/status")) {
          // Handle comprehensive status response
          if (data.fan) {
            setFanStatus(data.fan);
          }
          if (data.door) {
            setDoorStatus(data.door);
          }
          if (data.window) {
            setWindowStatus(data.window);
          }
          if (data.temperature !== undefined) {
            setTemperature(data.temperature);
          }
          if (data.humidity !== undefined) {
            setHumidity(data.humidity);
          }
          console.log("Status response received:", data);
        }
      } catch (error) {
        console.error("Error parsing message:", error);
      }
    };

    const handleDisconnect = () => {
      setConnected(false);
      setSmartHomeStatus(null);
      lastDataReceivedRef.current = null;
    };

    const handleError = (error: Error) => {
      console.error("MQTT error:", error);
      setConnected(false);
      setSmartHomeStatus(null);
      lastDataReceivedRef.current = null;
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

  useEffect(() => {
    const deviceId = "esp32_main";

    statusCheckIntervalRef.current = setInterval(() => {
      updateDeviceStatus();

      // Request status every 20 seconds to keep connection alive
      publishMessage(`devices/${deviceId}/request/status`, {});
    }, 20000); // Every 20 seconds

    return () => {
      if (statusCheckIntervalRef.current) {
        clearInterval(statusCheckIntervalRef.current);
        statusCheckIntervalRef.current = null;
      }
    };
  }, [publishMessage]);

  // Value to be passed to the context provider
  const value: MQTTContextValue = {
    connected,
    latestSensorData,
    latestRfidCheck,
    doorStatus,
    windowStatus,
    fanStatus,
    temperature,
    humidity,
    smartHomeStatus,
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
