import Link from "next/link";
import { FaHome } from "react-icons/fa";

export default function GlobalNotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] text-gray-200 p-4">
      <h1 className="text-6xl font-bold text-pink-500 mb-4">404</h1>
      <h2 className="text-2xl font-semibold mb-4 text-text">Page Not Found</h2>
      <p className="mb-6 text-center max-w-md text-accent">
        The page you are looking for does not exist.
      </p>

      <Link
        href="/"
        className="text-lg flex-row gap-4 font-semibold relative inline-flex items-center justify-center rounded-md border-pink-600 border-2 bg-transparent px-6 py-3 text-pink-600 transition-all duration-300
                 hover:-translate-x-1 hover:-translate-y-1 hover:shadow-[6px_6px_0px_rgba(230,0,112,0.8)]"
      >
        <FaHome />
        <p>Go Home</p>
      </Link>
    </div>
  );
}