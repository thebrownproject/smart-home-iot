"use client";
import {
  Navbar as HeroUINavbar,
  NavbarContent,
  NavbarBrand,
  NavbarItem,
} from "@heroui/navbar";
import { StatusIcon } from "@/components/StatusIcon";
import { HouseWifi } from "lucide-react";
import NextLink from "next/link";

import { ThemeSwitch } from "@/components/theme-switch";
import { useMQTT } from "@/components/MQTTProvider";

export const Navbar = () => {
  const { smartHomeStatus } = useMQTT();

  return (
    <HeroUINavbar maxWidth="xl" position="sticky">
      <NavbarContent className="basis-1/5 sm:basis-full" justify="start">
        <NavbarBrand as="li" className="gap-3 max-w-fit">
          <NextLink className="flex justify-start items-center gap-2" href="/">
            <StatusIcon
              status={
                smartHomeStatus === null
                  ? "loading"
                  : smartHomeStatus
                    ? "normal"
                    : "danger"
              }
              icon={<HouseWifi />}
              variant="flat"
            />
          </NextLink>
          <p className="text-3xl font-bold text-inherit">Zap</p>
        </NavbarBrand>
      </NavbarContent>

      <NavbarContent className="basis-1 pl-4" justify="end">
        <NavbarItem className="mt-1">
          <ThemeSwitch />
        </NavbarItem>
      </NavbarContent>
    </HeroUINavbar>
  );
};
