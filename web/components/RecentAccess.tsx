"use client";
import { useState, useEffect } from "react";
import { Card, CardHeader, CardBody } from "@heroui/card";
import { Tabs, Tab } from "@heroui/tabs";
import {
  Table,
  TableHeader,
  TableColumn,
  TableBody,
  TableRow,
  TableCell,
} from "@heroui/table";
import { Chip } from "@heroui/chip";
import { Spinner } from "@heroui/spinner";
import { getRfidScans, RfidScanEntry } from "@/lib/api";

type FilterType = "all" | "success" | "failed";

export const RecentAccess = () => {
  const [filter, setFilter] = useState<FilterType>("all");
  const [scans, setScans] = useState<RfidScanEntry[] | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchScans = async () => {
      try {
        const data = await getRfidScans(filter);
        setScans(data);
      } catch (error) {
        console.error("Error fetching RFID scans:", error);
        setScans([]);
      } finally {
        setIsLoading(false);
      }
    };

    fetchScans();
    const interval = setInterval(fetchScans, 5000);

    return () => clearInterval(interval);
  }, [filter]);

  const formatTime = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString("en-AU", {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    });
  };

  const columns = [
    { key: "Status", label: "Status" },
    { key: "User", label: "User" },
    { key: "Time", label: "Time" },
  ];

  return (
    <Card isBlurred className="w-full" radius="lg" shadow="md">
      <CardHeader className="pt-4 pl-4 flex justify-between items-start">
        <h1 className="text-xs text-default-600 pb-5">Recent Access</h1>
        <Tabs
          aria-label="Filter options"
          size="sm"
          selectedKey={filter}
          onSelectionChange={(key) => setFilter(key as FilterType)}
        >
          <Tab key="all" title="All" />
          <Tab key="success" title="Granted" />
          <Tab key="failed" title="Denied" />
        </Tabs>
      </CardHeader>
      <CardBody className="pb-4 pt-3 px-4 max-h-[260px] overflow-y-auto">
        <Table
          aria-label="Recent access logs"
          removeWrapper
          classNames={{
            th: "bg-transparent text-default-500 text-xs font-normal w-1/3 border-b border-default",
            td: "py-3 w-1/3 border-b border-default group-data-[last=true]:border-b-0",
          }}
        >
          <TableHeader columns={columns} className="pl-0">
            {(column) => (
              <TableColumn key={column.key}>{column.label}</TableColumn>
            )}
          </TableHeader>
          <TableBody
            items={scans ?? []}
            isLoading={isLoading}
            loadingContent={<Spinner size="sm" />}
            emptyContent="No access logs found"
          >
            {(scan) => (
              <TableRow key={scan.id}>
                <TableCell>
                  <Chip
                    color={
                      scan.accessResult === "granted" ? "success" : "danger"
                    }
                    variant="flat"
                    size="sm"
                  >
                    {scan.accessResult === "granted" ? "Granted" : "Denied"}
                  </Chip>
                </TableCell>
                <TableCell>
                  <span className="text-sm font-medium">
                    {scan.username || "Unknown"}
                  </span>
                </TableCell>
                <TableCell>
                  <span className="text-sm text-default-600">
                    {formatTime(scan.timestamp)}
                  </span>
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </CardBody>
    </Card>
  );
};
