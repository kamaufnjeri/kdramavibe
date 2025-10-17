import React from 'react';
import { Kactor } from '@/interfaces';
import ImageWithFallback from '../kdramas/ImageWithFallback';
import Link from 'next/link';

interface KactorCardProps {
  kactor: Kactor;
}



const KactorCard: React.FC<KactorCardProps> = ({ kactor }) => {
  return (
    <Link href={`k-actors/${kactor.slug}`} className="group rounded-2xl overflow-hidden shadow hover:shadow-lg transition h-full">
      
       <ImageWithFallback alt={kactor.name} imageSrc={kactor.image_url} gender={kactor?.gender}/>
    
      <div className="p-3 flex flex-wrap justify-between">
        <h2 className="text-base font-bold group-hover:text-primary">{kactor.name}</h2>
        {kactor.age && (
            
                 <p className="text-sm font-light my-2 self-end">
                    <strong>Age:{" "}</strong>
            {kactor.age}
          </p>
         
        )}
       
      </div>
    </Link>
  );
};

export default KactorCard;
