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
  const { temperature, humidity, smartHomeStatus } = useMQTT();
  const [motionData, setMotionData] = useState<SensorLogEntry[] | null>(null);
  const [gasAlertActive, setGasAlertActive] = useState<boolean | null>(null);

  useEffect(() => {
    const fetchMotionData = async () => {
      const data = await getMotionData();
      setMotionData(data);
    };

    fetchMotionData();
    const interval = setInterval(fetchMotionData, 5000);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const fetchGasData = async () => {
      try {
        const alerts = await getGasData(1);
        const hasActiveAlert = alerts.some((alert) => alert.alertEnd === null);
        setGasAlertActive(hasActiveAlert);
      } catch (error) {
        console.error("[GasSensor] Database error:", error);
        setGasAlertActive(null);
      }
    };

    fetchGasData();
    const interval = setInterval(fetchGasData, 5000);

    return () => clearInterval(interval);
  }, []);

  const isOffline = !smartHomeStatus;
  const isLoading = smartHomeStatus === null;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-5">
      <SensorCard
        icon={<Thermometer />}
        status={temperature === null ? "loading" : "normal"}
        title="Temperature"
        value={temperature?.toString() ?? "--"}
        valueType={temperature === null || isOffline || isLoading ? "" : "°C"}
      />
      <SensorCard
        icon={<Droplet />}
        status={humidity === null ? "loading" : "normal"}
        title="Humidity"
        value={humidity?.toString() ?? "--"}
        valueType={humidity === null || isOffline || isLoading ? "" : "%"}
      />
      <SensorCard
        icon={
          motionData && motionData.length > 0 ? (
            <ShieldAlert />
          ) : (
            <ShieldCheck />
          )
        }
        status={
          motionData === null || isOffline || isLoading
            ? "loading"
            : motionData.length > 0
              ? "danger"
              : "normal"
        }
        title="Motion Sensor"
        value={
          motionData === null || isOffline || isLoading
            ? "--"
            : motionData.length.toString()
        }
        valueType={
          motionData === null || isOffline || isLoading ? "" : "last hr"
        }
      />
      <SensorCard
        icon={<Flame />}
        status={
          gasAlertActive === null || isOffline || isLoading
            ? "loading"
            : gasAlertActive
              ? "danger"
              : "normal"
        }
        title="Gas Sensor"
        value={
          gasAlertActive === null || isOffline || isLoading
            ? "--"
            : gasAlertActive
              ? "ALERT"
              : "Safe"
        }
        valueType=""
      />
    </div>
  );
};
