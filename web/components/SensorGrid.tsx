"use client";
import { useState, useEffect } from "react";
import { SensorCard } from "./SensorCard";
import {
  Thermometer,
  Droplet,
  Flame,
  ShieldAlert,
  ShieldCheck,
} from "lucide-react";
import { useMQTT } from "./MQTTProvider";
import { SensorLogEntry, getMotionData, getGasData } from "@/lib/api";

export const SensorGrid = () => {
  const { temperature, humidity, gasDetected } = useMQTT();
  const [motionData, setMotionData] = useState<SensorLogEntry[]>([]);
  const [gasAlertFallback, setGasAlertFallback] = useState<boolean | null>(
    null
  );

  // Fetch motion data
  useEffect(() => {
    const fetchMotionData = async () => {
      const data = await getMotionData();
      setMotionData(data);
    };
    fetchMotionData();
  }, []);

  // Fetch gas alert from database (primary source)
  useEffect(() => {
    const fetchGasData = () => {
      console.log("[GasSensor] Fetching from database...");
      getGasData(1)
        .then((alerts) => {
          console.log("[GasSensor] Database returned alerts:", alerts);

          // Check if there's an active alert (alertEnd is null)
          const hasActiveAlert = alerts.some(
            (alert) => alert.alertEnd === null
          );
          console.log("[GasSensor] Database has active alert:", hasActiveAlert);
          setGasAlertFallback(hasActiveAlert);
        })
        .catch((error) => {
          console.error("[GasSensor] Database error:", error);
          setGasAlertFallback(null); // Keep null to show loading
        });
    };

    // Initial fetch
    fetchGasData();

    // Poll database every 5 seconds
    const interval = setInterval(fetchGasData, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-5">
      <SensorCard
        icon={<Thermometer />}
        status={temperature === null ? "loading" : "normal"}
        title="Temperature"
        value={temperature?.toString() ?? "--"}
        valueType="°C"
      />
      <SensorCard
        icon={<Droplet />}
        status={humidity === null ? "loading" : "normal"}
        title="Humidity"
        value={humidity?.toString() ?? "--"}
        valueType="%"
      />
      <SensorCard
        icon={motionData.length > 0 ? <ShieldAlert /> : <ShieldCheck />}
        status={motionData === null ? "loading" : "normal"}
        title="PIR Activity"
        value={motionData === null ? "--" : motionData.length.toString()}
        valueType="detections/hr"
      />
      <SensorCard
        icon={<Flame />}
        status={
          // If both database and MQTT have no data, show loading
          gasAlertFallback === null && gasDetected === null
            ? "loading"
            : // Otherwise prioritize MQTT over database (real-time > historical)
              (gasDetected !== null ? gasDetected : gasAlertFallback)
              ? "danger"
              : "normal"
        }
        title="Gas Sensor"
        value={
          gasAlertFallback === null && gasDetected === null
            ? "--"
            : (gasDetected !== null ? gasDetected : gasAlertFallback)
              ? "ALERT"
              : "Safe"
        }
        valueType=""
      />
    </div>
  );
};
