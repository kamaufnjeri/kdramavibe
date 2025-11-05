"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { FaSun, FaMoon } from "react-icons/fa";

export default function ThemeToggle() {
  // Access current theme, setter, and resolved system theme
  const { theme, setTheme, resolvedTheme } = useTheme();
  
  // State to track if component is mounted to avoid hydration issues
  const [mounted, setMounted] = useState(false);

  // Set mounted to true after first render
  useEffect(() => setMounted(true), []);

  // Return null until mounted to prevent SSR mismatch
  if (!mounted) return null;

  // Determine the effective theme (light or dark)
  const current = theme === "system" ? resolvedTheme : theme;

  return (
    <button
      className="group outline-none border-none self-end sm:self-center cursor-pointer m-2 transition-class"
      // Toggle between light and dark themes on click
      onClick={() => setTheme(current === "dark" ? "light" : "dark")}
    >
      {/* Display sun icon if dark mode, moon icon if light mode */}
      {current === "dark" ? (
        <FaSun className="text-2xl group-hover:text-primary text-text" />
      ) : (
        <FaMoon className="text-2xl group-hover:text-primary text-text" />
      )}
    </button>
  );
}
