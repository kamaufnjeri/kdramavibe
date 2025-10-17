'use client';

import { MAN_PALCEHOLDER, PLACEHOLDER, WOMAN_PLACEHOLDER } from "@/constants";
import Image from "next/image";
import { useState } from "react";


interface ImageWithFallbackProps {
  imageSrc?: string | null;
  alt: string;
  gender?: "female" | "male" | null;
  width?: number;
  height?: number;
  className?: string;
}

const ImageWithFallback: React.FC<ImageWithFallbackProps> = ({
  imageSrc,
  alt,
  gender,
  width = 300,
  height = 400,
  className="object-contain w-full aspect-[3/4] rounded-2xl"

}) => {
  // choose fallback based on gender
  const defaultFallback =
    gender === "female"
      ? WOMAN_PLACEHOLDER
      : gender === "male"
      ? MAN_PALCEHOLDER
      : PLACEHOLDER

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
      onError={() => setImgSrc(defaultFallback)} // fallback when load fails
    />
  );
};

export default ImageWithFallback;
