import { Kdrama } from '@/interfaces'
import React from 'react'
import KdramaCard from './KdramaCard'


interface KdramasListProps {
  kdramas: Kdrama[]
}
const KdramasList: React.FC<KdramasListProps> = ({ kdramas }) => {
  return (
    <div className='w-full px-10 py-4'>
      <ul className='flex flex-wrap w-full '>
      {kdramas && kdramas.map((kdrama) => (
        <li key={kdrama.slug} className=' w-full md:w-1/2 lg:w-1/4 p-4 '>
          <KdramaCard kdrama={kdrama}/>
        </li>
      ))}
      </ul>
    </div>
  )
}

export default KdramasList
