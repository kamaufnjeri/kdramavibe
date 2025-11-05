import Image from "next/image"; // Next.js optimized Image component

// Loading component displayed globally during page transitions or data fetch
export default function GlobalLoading() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[70vh] text-gray-200">
      {/* Spinner container */}
      <div className="relative w-16 h-16">
        {/* Animated spinning circle */}
        <div
          className="
            absolute inset-0 
            animate-spin 
            rounded-full 
            h-16 
            w-16 
            border-t-4 
            border-pink-600 
            border-b-4 
            mb-4 
            flex items-center justify-center
          "
        ></div>

        {/* Centered logo image */}
        <div className="absolute inset-0 flex items-center justify-center">
          <Image
            src="/images/logo.png" // Logo image
            alt="Kdrama vibe Icon"  // Alt text for accessibility
            width={50}             // Width of the logo
            height={50}            // Height of the logo
          />
        </div>
      </div>
    </div>
  );
}
