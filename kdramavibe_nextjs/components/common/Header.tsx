"use client"; // Required for client-side interactivity

import Link from "next/link";
import ThemeToggle from "./ThemeToggle";
import Image from "next/image";
import { NAV_LINKS } from "@/constants";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { FaBars, FaTimes } from "react-icons/fa";

const Header = () => {
  // Get current path to highlight active nav link
  const pathname = usePathname();
  
  // State to toggle mobile menu visibility
  const [showMenu, setShowMenu] = useState<boolean>(false);

  return (
    <header className="px-2 border-b-2 border-gray-300 flex flex-col sm:flex-row gap-2 sm:h-20 items-start sm:items-center justify-between w-full bg-[color:var(--color-background)] transition-all duration-300">
      
      {/* Logo and Hamburger Menu Button */}
      <div className="w-full flex flex-row gap-4 justify-between items-center">
        {/* Site Logo */}
        <Link href="/">
          <Image
            src="/images/logo.png"
            alt="KdramaVibe Logo"
            width={90}
            height={90}
            priority
          />
        </Link>

        {/* Hamburger menu button (visible on small screens) */}
        <button
          className="border-none outline-none sm:hidden block text-2xl cursor-pointer group"
          onClick={() => setShowMenu((prev) => !prev)}
        >
          {showMenu ? (
            <FaTimes className="text-2xl group-hover:text-primary text-text" />
          ) : (
            <FaBars className="text-2xl group-hover:text-primary text-text" />
          )}
        </button>
      </div>

      {/* Navigation Links */}
      <nav
        className={`overflow-hidden sm:smooth-dropdown transition-all duration-300 ease-out sm:overflow-visible sm:h-auto w-full ${
          showMenu
            ? "max-h-96 opacity-100 sm:opacity-100 pointer-events-auto z-10"
            : "max-h-0 opacity-0 sm:opacity-100 sm:pointer-events-auto pointer-events-none lg:z-10 -z-0"
        } flex sm:items-center sm:justify-end flex-row `}
      >
        <ul className="flex flex-col sm:flex-row sm:gap-6 gap-2 items-start sm:items-center px-2 w-full sm:w-auto">
          {/* Map through NAV_LINKS to render navigation items */}
          {NAV_LINKS.map((link, index) => {
            const isActive: boolean = link.href === pathname;
            return (
              <li key={index} className="transition-class">
                <Link
                  href={link.href}
                  className={`text-xl font-semibold transition-colors duration-300 ${
                    isActive
                      ? "text-primary"
                      : "text-text hover:text-primary"
                  }`}
                  onClick={() => setShowMenu(false)} // Close menu when link is clicked
                >
                  {link.name}
                </Link>
              </li>
            );
          })}
        </ul>

        {/* Theme Toggle Button */}
        <ThemeToggle />
      </nav>
    </header>
  );
};

export default Header;
