import React from 'react';
import { Kdrama } from '@/interfaces';
import ImageWithFallback from './ImageWithFallback';
import Link from 'next/link';

interface KdramaCardProps {
  kdrama: Kdrama;
}



const KdramaCard: React.FC<KdramaCardProps> = ({ kdrama }) => {
  return (
    <Link href={`/k-dramas/${kdrama.slug}`} className="group rounded-2xl overflow-hidden shadow hover:shadow-lg transition h-full">
      
       <ImageWithFallback alt={kdrama.title} imageSrc={kdrama.image_url}/>
    
      <div className="p-3">
        <h2 className="text-base font-bold group-hover:text-primary">{kdrama.title}</h2>
        {kdrama.start_year && (
          <p className="text-sm font-light my-2">
            {kdrama.start_year} {(kdrama.end_year && kdrama.end_year !== kdrama.start_year) ? `– ${kdrama.end_year}` : ''}
          </p>
        )}
        {
          kdrama.genres && <ul className='flex flex-wrap gap-2'>
            {kdrama.genres.map((genre) => (
              <li className='bg-secondary p-1 rounded-md' key={genre}>{genre}</li>
            ))}
          </ul>
        }
      </div>
    </Link>
  );
};

export default KdramaCard;
