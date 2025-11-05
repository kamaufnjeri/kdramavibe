"use client"; // Enable client-side interactivity for this component

import Link from "next/link";
import { useEffect } from "react";
import { FaHome, FaRedo } from "react-icons/fa";

// Define props for the global error component
interface Props {
  error: Error; // The error object that occurred
  reset: () => void; // Function to reset error state and retry
}

/**
 * GlobalError component
 * Displays a user-friendly error page with options to retry or go home.
 *
 * @param {Props} props - The component props.
 * @returns {JSX.Element} The rendered error page.
 */
export default function GlobalError({ error, reset }: Props) {
  // Log the error to the console when it changes
  useEffect(() => {
    console.error(error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] text-gray-200 p-4">
      {/* Main error heading */}
      <h1 className="text-4xl font-bold text-pink-500 mb-4">
        Something went wrong!
      </h1>

      {/* Error description */}
      <p className="mb-4 text-center text-text">
        We encountered an unexpected error.
      </p>

      {/* Display actual error message */}
      <p className="text-accent">{error.message}</p>

      {/* Action buttons: retry and go home */}
      <div className="flex flex-wrap gap-8 items-center justify-center">
        {/* Retry button */}
        <button
          onClick={() => reset()}
          className="
            relative inline-flex items-center justify-center px-6 py-3 
            font-medium text-pink-600 border-2 border-pink-600 
            rounded-md overflow-hidden transition-all duration-300
            group
          "
        >
          {/* Background fill animation */}
          <span
            className="
              absolute inset-0 bg-pink-600 translate-x-[-100%] group-hover:translate-x-0
              transition-transform duration-500 ease-out
              z-0
            "
          ></span>

          {/* Button content */}
          <span className="relative flex items-center gap-2 z-10 text-pink-600 group-hover:text-white">
            <FaRedo />
            Try Again!
          </span>
        </button>

        {/* Go home link */}
        <Link
          href="/"
          className="
            text-lg flex-row gap-4 font-semibold relative inline-flex items-center justify-center 
            rounded-md border-pink-600 border-2 bg-transparent px-6 py-3 text-pink-600 
            transition-all duration-300
            hover:-translate-x-1 hover:-translate-y-1 
            hover:shadow-[6px_6px_0px_rgba(230,0,112,0.8)]
          "
        >
          <FaHome />
          <p>Go Home</p>
        </Link>
      </div>
    </div>
  );
}
