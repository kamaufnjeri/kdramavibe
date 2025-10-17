"use client";

import { useTheme } from "next-themes";
import { useEffect, useState } from "react";
import { FaSun, FaMoon } from "react-icons/fa";

export default function ThemeToggle() {
  const { theme, setTheme, resolvedTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);
  if (!mounted) return null;

  const current = theme === "system" ? resolvedTheme : theme;

  return (
     <button
      className="group outline-none border-none self-end sm:self-center cursor-pointer m-2 transition-class"
      onClick={() => setTheme(current === "dark" ? "light" : "dark")}
    >
      {current === "dark" ? (
        <FaSun className="text-2xl group-hover:text-primary text-text" />
      ) : (
        <FaMoon className="text-2xl group-hover:text-primary text-text" />
      )}
    </button>
  );
}
