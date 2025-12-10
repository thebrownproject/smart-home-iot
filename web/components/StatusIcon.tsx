import { Button } from "@heroui/button";

type StatusType = "loading" | "normal" | "warning" | "danger";
type ColorType = "default" | "success" | "warning" | "danger";

type StatusIconProps = {
  icon: React.ReactNode;
  status: StatusType;
  variant?: "flat" | "bordered";
  size?: "sm" | "md" | "lg";
};

export const StatusIcon = ({
  icon,
  status,
  variant = "bordered",
  size = "lg",
}: StatusIconProps) => {
  const colorMap: Record<StatusType, ColorType> = {
    loading: "default",
    normal: "success",
    warning: "warning",
    danger: "danger",
  };

  return (
    <Button
      isIconOnly
      color={colorMap[status]}
      variant={variant}
      size="sm"
      radius="full"
      isLoading={status === "loading"}
    >
      {status !== "loading" && icon}
    </Button>
  );
};
