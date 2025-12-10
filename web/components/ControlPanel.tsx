"use client";
import { Card, CardHeader, CardBody } from "@heroui/card";
import { DoorClosedLocked, DoorOpen, Wind, Grid2x2 } from "lucide-react";
import { useMQTT } from "./MQTTProvider";
import { ControlButton } from "./ControlButton";

export const ControlPanel = () => {
  const { doorStatus, windowStatus, fanStatus, publishMessage } = useMQTT();

  return (
    <Card isBlurred className="w-full" radius="lg" shadow="md">
      <CardHeader className="pt-4 pl-4">
        <h1 className="text-xs text-default-600">Device Controls</h1>
      </CardHeader>
      <CardBody className="pb-4 pt-3 px-4">
        <div className="flex gap-13 justify-center items-center">
          <ControlButton
            device="door"
            deviceState={doorStatus?.state || null}
            icon={
              doorStatus?.state === "open" ? (
                <DoorOpen size={25} />
              ) : (
                <DoorClosedLocked size={25} />
              )
            }
            label="Door"
            onPublish={publishMessage}
          />
          <ControlButton
            device="window"
            deviceState={windowStatus?.state || null}
            icon={<Grid2x2 size={25} />}
            label="Window"
            onPublish={publishMessage}
          />
          <ControlButton
            device="fan"
            deviceState={fanStatus?.state || null}
            icon={<Wind size={25} />}
            label="Fan"
            onPublish={publishMessage}
          />
        </div>
      </CardBody>
    </Card>
  );
};
