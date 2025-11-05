import { Kdrama } from '@/interfaces'
import React from 'react'
import KdramaCard from './KdramaCard'

interface KdramasListProps {
  kdramas: Kdrama[]; // Array of Kdrama objects to display
}

const KdramasList: React.FC<KdramasListProps> = ({ kdramas }) => {
  return (
    <div className='w-full px-10 py-4'>
      {/* List of Kdrama cards */}
      <ul className='flex flex-wrap w-full'>
        {kdramas && kdramas.map((kdrama) => (
          <li
            key={kdrama.slug} // Unique key for each item
            className='w-full md:w-1/2 lg:w-1/4 p-4'
          >
            <KdramaCard kdrama={kdrama} /> {/* Render individual card */}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default KdramasList
