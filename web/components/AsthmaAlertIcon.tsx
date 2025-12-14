"use client";
import { Popover, PopoverTrigger, PopoverContent } from "@heroui/popover";
import { Button } from "@heroui/button";
import { TriangleAlert } from "lucide-react";
import { useMQTT } from "./MQTTProvider";

export const AsthmaAlertIcon = () => {
  const { temperature, humidity } = useMQTT();

  const isAsthmaAlert =
    temperature !== null &&
    humidity !== null &&
    humidity > 50 &&
    temperature > 27;

  if (!isAsthmaAlert) return null;

  return (
    <Popover
      placement="bottom"
      offset={25}
      crossOffset={80}
      shadow="md"
      backdrop="opaque"
    >
      <PopoverTrigger>
        <Button
          isIconOnly
          color="warning"
          variant="flat"
          size="sm"
          radius="full"
        >
          <TriangleAlert />
        </Button>
      </PopoverTrigger>
      <PopoverContent>
        <div className="pb-3 pt-4 px-4">
          <h1 className="text-xs text-default-600">Asthma Alert</h1>
          <p className="inline-flex items-baseline gap-1 mt-1">
            <span className="text-2xl text-default-900 font-bold">
              {temperature}°C
            </span>
            <span className="text-sm text-default-600">/ {humidity}%</span>
          </p>
          <p className="text-xs text-default-500 mt-2">
            High humidity and temperature may trigger asthma symptoms
          </p>
        </div>
      </PopoverContent>
    </Popover>
  );
};
