import { Button } from "@heroui/button";

type StatusType = "loading" | "normal" | "warning" | "danger";
type ColorType = "default" | "success" | "warning" | "danger";

type SensorIconProps = {
  icon: React.ReactNode;
  status: StatusType;
  size?: "sm" | "md" | "lg";
};

export const SensorIcon = ({ icon, status, size = "lg" }: SensorIconProps) => {
  const colorMap: Record<StatusType, ColorType> = {
    loading: "default",
    normal: "success", // Green
    warning: "warning", // Orange/Yellow
    danger: "danger", // Red
  };

  return (
    <Button
      isIconOnly
      color={colorMap[status]}
      variant="bordered"
      size="sm"
      radius="full"
      isLoading={status === "loading"}
    >
      {status !== "loading" && icon}
    </Button>
  );
};
