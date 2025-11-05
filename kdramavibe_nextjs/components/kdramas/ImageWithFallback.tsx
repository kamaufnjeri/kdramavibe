'use client';

import { MAN_PALCEHOLDER, PLACEHOLDER, WOMAN_PLACEHOLDER } from "@/constants";
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
  const defaultFallback =
    gender === "female"
      ? WOMAN_PLACEHOLDER
      : gender === "male"
      ? MAN_PALCEHOLDER
      : PLACEHOLDER;

  // state to track current image source
  const [imgSrc, setImgSrc] = useState(
    typeof imageSrc === "string" && imageSrc.startsWith("http")
      ? imageSrc
      : defaultFallback
  );

  return (
    <Image
      src={imgSrc}
      alt={alt}
      width={width}
      height={height}
      className={className}
      onError={() => setImgSrc(defaultFallback)} // fallback if image fails to load
    />
  );
};

export default ImageWithFallback;
