'use client';

import { ALL_COLORS, FEMALE_COLORS, MALE_COLORS } from "@/constants";
import Image from "next/image";
import { useState } from "react";

interface ImageWithFallbackProps {
  imageSrc?: string | null; // primary image URL
  alt: string; // alt text for accessibility
  textSize?: string | null;
  containerStyles?: string | null;
  gender?: "female" | "male" | null; // gender-based fallback
  width?: number; // optional width
  height?: number; // optional height
  className?: string; // additional classes
}

const ImageWithFallback: React.FC<ImageWithFallbackProps> = ({
  imageSrc,
  alt,
  gender,
  textSize,
  containerStyles,
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

  const getRandomColorPair = (colors: { bg: string; text: string }[]) =>
      colors[Math.floor(Math.random() * colors.length)];


 

  const colorPool =
    gender === "female"
      ? FEMALE_COLORS
      : gender === "male"
      ? MALE_COLORS
      : ALL_COLORS;

    

    const { bg, text } = getRandomColorPair(colorPool);

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
        <div className={`${className} ${containerStyles} flex items-center justify-center p-4 ${bg} ${text}`}>
          <span className={`${textSize ? textSize : "text-4xl"} font-semibold`}>
            {alt}
          </span>
        </div>
      )}
   </>
  );
};

export default ImageWithFallback;
