import React from 'react';
import { Kdrama } from '@/interfaces';
import ImageWithFallback from './ImageWithFallback';
import Link from 'next/link';
import { FaEye, FaStar } from 'react-icons/fa';

interface KdramaCardProps {
  kdrama: Kdrama; // kdrama object to display in card
}

const KdramaCard: React.FC<KdramaCardProps> = ({ kdrama }) => {
  return (
    <div className="group rounded-2xl overflow-hidden shadow-md hover:shadow-2xl transition h-full">
      {/* Thumbnail image linking to kdrama details */}
      <Link href={`/k-dramas/${kdrama.slug}`}>
        <ImageWithFallback 
          alt={kdrama.title} 
          imageSrc={kdrama.image_url || kdrama.dramabeans_image_url} 
        />
      </Link>

      <div className="p-3">
        {/* Title linking to kdrama details */}
        <Link href={`/k-dramas/${kdrama.slug}`}>
          <h2 className="text-base font-bold hover:text-primary">{kdrama.title}</h2>
        </Link>

        {/* Year range */}
        {kdrama.start_year && (
          <p className="text-sm font-light my-2">
            {kdrama.start_year} {(kdrama.end_year && kdrama.end_year !== kdrama.start_year) ? `– ${kdrama.end_year}` : ''}
          </p>
        )}

        {/* Genres */}
        {kdrama.genres && (
          <ul className="flex flex-wrap gap-2">
            {kdrama.genres.map((genre) => (
              <li className="bg-secondary p-1 rounded-md" key={genre}>
                {genre}
              </li>
            ))}
          </ul>
        )}

        {/* Ratings and votes */}
        {(kdrama.rating || kdrama.no_of_votes) && (
          <div className="flex flex-wrap justify-between gap-1 items-center border border-accent/30 rounded-xl px-3 py-2 mt-2">
            <p className="text-sm text-purple-300 italic font-semibold tracking-wide">
              By <span className="text-accent not-italic">Dramabeans</span>
            </p>

            <div className="flex items-center gap-4">
              {/* Rating */}
              {kdrama.rating && (
                <span className="inline-flex items-center gap-1 text-yellow-400 font-semibold text-sm">
                  <FaStar className="text-yellow-400" size={14} />
                  <span>{kdrama.rating}</span>
                </span>
              )}

              {/* Number of votes */}
              {kdrama.no_of_votes && (
                <span className="inline-flex items-center gap-1 text-sm font-medium">
                  <FaEye className="text-gray-400" size={14} />
                  <span>{parseInt(kdrama.no_of_votes).toLocaleString()}</span>
                </span>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default KdramaCard;
