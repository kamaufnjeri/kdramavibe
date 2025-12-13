'use client';

import { ALL_COLORS, FEMALE_COLORS, MALE_COLORS } from "@/constants";
import Image from "next/image";
import { useState } from "react";

interface ImageWithFallbackProps {
  imageSrc?: string | null; // primary image URL
  alt: string; // alt text for accessibility
  gender?: "female" | "male" | null; // gender-based fallback
  width?: number; // optional width
  height?: number; // optional height
  className?: string; // additional classes
}

const ImageWithFallback: React.FC<ImageWithFallbackProps> = ({
  imageSrc,
  alt,
  gender,
  width = 300,
  height = 400,
  className = "object-contain w-full aspect-[3/4] rounded-2xl",
}) => {
  // determine fallback image based on gender
    const [hasError, setHasError] = useState(false);


   const showImage =
    imageSrc &&
    typeof imageSrc === "string" &&
    imageSrc.startsWith("http") &&
    !hasError;

  const colorPool =
    gender === "female"
      ? FEMALE_COLORS
      : gender === "male"
      ? MALE_COLORS
      : ALL_COLORS;

    const getRandomColor = (colors: string[]) =>
      colors[Math.floor(Math.random() * colors.length)];

  return (
   <>
    {showImage ? (
        <Image
          src={imageSrc}
          alt={alt}
        width={width}
        height={height}
        className={`${className} rounded-md`}
          onError={() => setHasError(true)}
        />
      ) : (
        <div className={`${className} flex items-center justify-center p-4 rounded-2xl ${getRandomColor(colorPool)}`}>
          <span className="text-4xl font-semibold">
            {alt}
          </span>
        </div>
      )}
   </>
  );
};

export default ImageWithFallback;
