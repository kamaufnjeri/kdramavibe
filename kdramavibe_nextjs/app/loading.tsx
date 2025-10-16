import Image from "next/image";

// app/loading.tsx
export default function GlobalLoading() {
  return (
    <div className="flex flex-col items-center justify-center h-full text-gray-200">
=      <div className="relative w-16 h-16">
        <div
          className="absolute inset-0 animate-spin rounded-full h-16 w-16 border-t-4 border-pink-600 border-b-4 mb-4 flex items-center justify-center
      "
        ></div>
        <div className="absolute inset-0 flex items-center justify-center">
          <Image
            src="/images/logo.png"
            alt="Kdrama vibe Icon"
            width={50}
            height={50}
          />
        </div>
      </div>
    </div>
  );
}