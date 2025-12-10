"use client";
import { useState, useEffect, useRef } from "react";
import { Button } from "@heroui/button";
import { useMQTT } from "./MQTTProvider";

type DeviceType = "door" | "window" | "fan";
type DeviceState = "open" | "closed" | "close" | "on" | "off" | null;

type ControlButtonProps = {
  device: DeviceType;
  deviceState: DeviceState;
  icon: React.ReactNode;
  label: string;
  onPublish: (topic: string, message: object) => void;
};

export const ControlButton = ({
  device,
  deviceState,
  icon,
  label,
  onPublish,
}: ControlButtonProps) => {
  const [isPending, setIsPending] = useState(false);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const previousStateRef = useRef<DeviceState>(deviceState);
  const { smartHomeStatus } = useMQTT();

  const isOffline = !smartHomeStatus;
  const isLoading = smartHomeStatus === null;

  const getNextState = (currentState: DeviceState) => {
    if (device === "fan") {
      return currentState === "on" ? "off" : "on";
    }
    return currentState === "open" ? "close" : "open";
  };

  const getButtonColor = () => {
    if (isPending || isLoading || isOffline) return "default";
    if (device === "fan") {
      return deviceState === "on" ? "success" : "danger";
    }
    return deviceState === "open" ? "success" : "danger";
  };

  const handleClick = () => {
    previousStateRef.current = deviceState;
    setIsPending(true);
    onPublish(`devices/esp32_main/control/${device}`, {
      state: getNextState(deviceState),
    });

    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => {
      setIsPending(false);
      timeoutRef.current = null;
    }, 5000);
  };

  useEffect(() => {
    if (isPending && deviceState !== previousStateRef.current) {
      setIsPending(false);
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
        timeoutRef.current = null;
      }
    }
  }, [deviceState, isPending]);

  useEffect(() => {
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, []);

  return (
    <div className="flex flex-col items-center gap-1">
      <Button
        isIconOnly
        color={getButtonColor()}
        variant="flat"
        size="lg"
        radius="full"
        isLoading={isPending || isLoading || isOffline}
        isDisabled={isOffline}
        onPress={handleClick}
      >
        {!isPending && !isLoading && !isOffline && icon}
      </Button>
      <span className="text-xs text-default-600 mt-1">{label}</span>
    </div>
  );
};
