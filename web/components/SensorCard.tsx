import { Card, CardHeader, CardBody, CardFooter } from "@heroui/card";
import { StatusIcon } from "./StatusIcon";

export const SensorCard = ({
  title,
  value,
  valueType,
  icon,
  status,
}: {
  title: string;
  value: string;
  valueType: string;
  icon: React.ReactNode;
  status: "loading" | "normal" | "warning" | "danger";
}) => {
  return (
    <Card isBlurred className="max-w-m min-w-[150px]" radius="lg" shadow="md">
      <CardHeader className="pt-4 pl-4">
        <StatusIcon icon={icon} status={status} />
      </CardHeader>
      <CardBody className="pb-3 pt-2 px-4 flex-col items-start">
        <h1 className="text-xs text-default-600 mt-2">{title}</h1>
        <p className="inline-flex items-baseline gap-1 mt-1">
          <span className="text-2xl text-default-900 font-bold">{value}</span>
          <span className="text-sm text-default-600">{valueType}</span>
        </p>
      </CardBody>
    </Card>
  );
};
