"use client"; // required for client-side interactivity

import Link from "next/link";
import { useEffect } from "react";
import { FaHome, FaRedo } from "react-icons/fa";

interface Props {
  error: Error;
  reset: () => void;
}

export default function GlobalError({ error, reset }: Props) {

  useEffect(() => {
    console.error(error); // log error to console
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] text-gray-200 p-4">
      <h1 className="text-4xl font-bold text-pink-500 mb-4">
        Something went wrong!
      </h1>
      <p className="mb-4 text-center text-text">
        We encountered an unexpected error.
      </p>
      <p className="text-accent">{error.message}</p>

      <div className="flex flex-wrap gap-8 items-center justify-center">
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

          {/* Content */}
          <span className="relative flex items-center gap-2 z-10 text-pink-600 group-hover:text-white">
            <FaRedo />
            Try Again!
          </span>
        </button>
        <Link
        href="/"
        className="text-lg flex-row gap-4 font-semibold relative inline-flex items-center justify-center rounded-md border-pink-600 border-2 bg-transparent px-6 py-3 text-pink-600 transition-all duration-300
                 hover:-translate-x-1 hover:-translate-y-1 hover:shadow-[6px_6px_0px_rgba(230,0,112,0.8)]"
      >
        <FaHome />
        <p>Go Home</p>
      </Link>
      </div>
    </div>
  );
}