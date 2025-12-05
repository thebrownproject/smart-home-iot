"use client";

import { useMQTT } from "./MQTTProvider";

export default function MQTTStatus() {
  const { connected, latestSensorData } = useMQTT();

  return (
    <div className="p-6 border border-gray-300 rounded-lg bg-white dark:bg-zinc-900">
      <h2 className="text-xl font-bold mb-4">MQTT Status</h2>

      {/* Connection Status */}
      <p className="text-gray-600 dark:text-gray-400">
        {connected ? "🟢 Connected" : "🔴 Disconnected"}
      </p>

      {/* Sensor Data */}
      <div className="mt-4">
        <h3 className="font-semibold text-gray-700 dark:text-gray-300">
          Latest Sensor Data:
        </h3>
        {latestSensorData ? (
          <div className="mt-2 text-gray-600 dark:text-gray-400">
            <p>
              Type:{" "}
              <span className="font-mono">{latestSensorData.sensor_type}</span>
            </p>
            <p>
              Value:{" "}
              <span className="font-mono">
                {latestSensorData.value}
                {latestSensorData.unit}
              </span>
            </p>
            <p>
              Timestamp:{" "}
              <span className="font-mono text-xs">
                {latestSensorData.timestamp}
              </span>
            </p>
          </div>
        ) : (
          <p className="mt-2 text-gray-500 italic">No data received yet</p>
        )}
      </div>
    </div>
  );
}
