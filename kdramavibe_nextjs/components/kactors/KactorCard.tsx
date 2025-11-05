import React from 'react';
import { Kactor } from '@/interfaces';
import ImageWithFallback from '../kdramas/ImageWithFallback';
import Link from 'next/link';
import { FaEye } from 'react-icons/fa';

interface KactorCardProps {
  kactor: Kactor; // Kactor object to display
}

const KactorCard: React.FC<KactorCardProps> = ({ kactor }) => {
  return (
    <div className="rounded-2xl overflow-hidden shadow-md hover:shadow-2xl transition h-full">
      
      {/* Kactor image linking to their page */}
      <Link href={`k-actors/${kactor.slug}`}>
        <ImageWithFallback 
          alt={kactor.name} 
          imageSrc={kactor.image_url || kactor.dramabeans_image_url} 
          gender={kactor?.gender} 
        />
      </Link>
      
      <div className="p-3 flex flex-col gap-1 justify-between">
        {/* Kactor name linking to their page */}
        <Link href={`k-actors/${kactor.slug}`}>
          <h2 className="text-base font-bold hover:text-primary">{kactor.name}</h2>
        </Link>

        {/* Display age if available */}
        {kactor.age && (
          <p className="text-sm font-light self-end">
            <strong>Age:{" "}</strong>
            {kactor.age}
          </p>
        )}

        {/* Display votes from Dramabeans if available */}
        {kactor.no_of_votes && (
          <div className="flex flex-wrap justify-between gap-1 items-center border border-accent/30 rounded-xl px-3 py-2 mt-2">
            <p className="text-sm text-purple-300 italic font-semibold tracking-wide">
              By <span className="text-accent not-italic">Dramabeans</span>
            </p>

            {kactor.no_of_votes && (
              <span className="inline-flex items-center gap-1 text-sm font-medium">
                <FaEye className="text-gray-400" size={14} />
                <span>{parseInt(kactor.no_of_votes).toLocaleString()}</span>
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default KactorCard;
