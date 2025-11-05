import { Kactor } from '@/interfaces'
import React from 'react'
import KactorCard from './KactorCard'

interface KactorsListProps {
  kactors: Kactor[] // Array of Kactor objects to display
}

// Component to render a list/grid of Kactor cards
const KactorsList: React.FC<KactorsListProps> = ({ kactors }) => {
  return (
    <div className='w-full px-4 py-4'>
      <ul className='flex flex-wrap w-full'>
        {kactors &&
          kactors.map((kactor) => (
            <li key={kactor.slug} className='w-full md:w-1/2 lg:w-1/4 p-4'>
              {/* Render individual Kactor card */}
              <KactorCard kactor={kactor} />
            </li>
          ))}
      </ul>
    </div>
  )
}

export default KactorsList
