"use client";

import { useMQTT } from "./MQTTProvider";

export default function MQTTFanToggle() {
  const { fanStatus, publishMessage } = useMQTT();

  const toggleFan = () => {
    const newState = fanStatus?.state === "on" ? "off" : "on";

    publishMessage("devices/esp32_main/control/fan", {
      state: newState,
      timestamp: new Date().toISOString(),
    });
  };

  return (
    <div className="p-6 border border-gray-300 rounded-lg bg-white dark:bg-zinc-900">
      <h2 className="text-xl font-bold mb-4">Fan Control</h2>

      <button
        className={`px-6 py-3 rounded-lg font-semibold transition-colors ${
          fanStatus?.state === "on"
            ? "bg-red-500 hover:bg-red-600 text-white"
            : "bg-green-500 hover:bg-green-600 text-white"
        }`}
        onClick={toggleFan}
      >
        {fanStatus?.state === "on" ? "🌀 Turn OFF" : "💨 Turn ON"}
      </button>

      <p className="mt-3 text-gray-600 dark:text-gray-400">
        Current State:{" "}
        <span
          className={`font-mono font-semibold ${
            fanStatus?.state === "on" ? "text-green-600" : "text-gray-500"
          }`}
        >
          {fanStatus?.state || "unknown"}
        </span>
      </p>
    </div>
  );
}
