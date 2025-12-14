import { KactorDramas } from '@/interfaces';
import Link from 'next/link';
import React from 'react';
import ImageWithFallback from '../kdramas/ImageWithFallback';

interface KactorDramasProps {
  kdramas: KactorDramas[]; // array of kdrama cast objects
}

const KactorDramasDetails: React.FC<KactorDramasProps> = ({ kdramas }) => {
  // Capitalize the first letter of a string safely
  const capitalize = (text: string) =>
    text ? text.charAt(0).toUpperCase() + text.slice(1) : '';

  return (
    <div className="rounded-2xl border border-border bg-background/60 shadow-sm 
                    text-text lg:w-3/4 w-full flex flex-col overflow-hidden">
      
      {/* Header */}
      <div className="bg-primary/80 text-white px-4 py-3">
        <h2 className="font-extrabold text-2xl tracking-wide">Kdramas</h2>
      </div>

      {/* Body */}
      <div className="p-6">
        {Array.isArray(kdramas) && kdramas.length > 0 ? (
          <ul className="flex flex-wrap w-full">
            {kdramas.map((kdrama) => (
              <li
                key={kdrama.kdrama_slug}
                className="p-3 w-full sm:w-1/2 lg:w-1/2"
              >
                <div className="border border-border rounded-xl p-4 h-full flex flex-row gap-3 hover:shadow-md transition">
                  {/* Actor Image */}
                  <div className="w-1/3 aspect-[3/4] overflow-hidden rounded-md bg-gray-100">
                    <ImageWithFallback
                      className="object-cover w-full h-full"
                      alt={kdrama.kdrama_title}
                      textSize={'text-md'}
                      imageSrc={kdrama.kdrama_image_url}
                    />
                  </div>

                  {/* Actor Info */}
                  <div className="flex flex-col w-2/3">
                  <div className='w-full flex flex-row justify-between'>
                    <Link
                      href={`/k-dramas/${kdrama.kdrama_slug}`}
                      className="text-accent hover:underline font-semibold text-lg transition"
                    >
                      {capitalize(kdrama.kdrama_title)}
                    </Link>
                      
                        {kdrama.year && (
                      <p className="pt-1 text-sm font-semibold text-right">
                        {kdrama.year}
                      </p>
                    )}
                  </div>
                    
                    {kdrama.role_name && (
                      <p className="pt-1 text-sm">
                        {capitalize(kdrama.role_name)}
                      </p>
                    )}
                  </div>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-center text-gray-500 italic">
            No cast information available.
          </p>
        )}
      </div>
    </div>
  );
};

export default KactorDramasDetails;
