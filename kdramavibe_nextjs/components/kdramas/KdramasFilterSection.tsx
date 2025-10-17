'use client'

import React, { useState } from 'react'
import GenresAutoComplete from './GenresAutoComplete'
import YearsSelect from './YearsSelect'
import { FaSync } from 'react-icons/fa'
import { useRouter } from 'next/navigation'
import { KdramasFilter } from '@/interfaces'
import PageSelect from './PageSelect'


interface KdramaFilterSectionProps {
  searchParams: KdramasFilter;
  noOfPages: number
}

const KdramasFilterSection: React.FC<KdramaFilterSectionProps> = ({ searchParams, noOfPages }) => {
  const [filters, setFilters] = useState<KdramasFilter>(searchParams);
  const router = useRouter();

  const handleFormReset = () => {
    setFilters({
      title: '',
      genre: '',
      year: '',
      page: '1'
    });
    router.push('/')
  }

   const getQuery = (filtersToUse: KdramasFilter): string => {
    const query = new URLSearchParams({
      ...(filtersToUse?.title ? { title: filtersToUse.title } : {}),
      ...(filtersToUse?.genre ? { genre: filtersToUse.genre } : {}),
      ...(filtersToUse?.year ? { year: filtersToUse?.year } : {}),
    }).toString();
    return query;
  }
  const handleChange = (key: string, value: string) => {
    const updatedFilters = {...filters, [key]: value};
    setFilters(updatedFilters)
    
  }

  const handlePageChange = (pageNo: string) => {
    const updatedFilters = {...filters, page: pageNo};
    setFilters(updatedFilters);
    const query = new URLSearchParams({
      ...(updatedFilters?.title ? { title: updatedFilters.title } : {}),
      ...(updatedFilters?.genre ? { genre: updatedFilters.genre } : {}),
      ...(updatedFilters?.year ? { year: updatedFilters?.year } : {}),
      ...(updatedFilters?.page ? { page: updatedFilters?.page } : {}),

    }).toString();

    router.push(`/?${query}`);
  }

 

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const query = getQuery(filters);

    router.push(`/?${query}`);
  }


  return (
    <div className='w-full p-4 flex flex-col gap-4'>
      <form className="flex flex-wrap items-start md:items-center lg:items-center" onSubmit={handleSubmit}>
        <div className='w-full md:w-1/2 lg:w-1/4 p-2'>
          <input type="text" name='title' 
          value={filters.title}
          onChange={(e) => handleChange(e.target.name, e.target.value)}
      placeholder="Type title..."
        className="
          w-full rounded-xl px-4 py-2
          border-2 border-accent 
          text-pink-200 
          bg-[#1a001f]
        placeholder:text-pink-400
          focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary
          hover:border-primary transition-colors duration-200
        "
          /> 
     </div>
        <GenresAutoComplete selectedGenre={filters.genre} handleChange={handleChange}/>
        <YearsSelect selectedYear={filters.year} handleChange={handleChange}/>
        <div className='flex flex-row justify-between gap-3 w-full lg:w-1/4 md:w-1/2 p-2'>
           <button type='submit' className='cursor-pointer border-accent text-accent hover:text-white hover:bg-primary hover:border-primary rounded-xl px-4 py-2 border-2'>Search</button>
        <button type='button' className='border-none cursor-pointer' onClick={handleFormReset}><FaSync className='text-2xl font-bold text-accent hover:text-primary'/></button>
        </div>
       
      </form>
      <PageSelect selectedPage={filters.page} handlePageChange={handlePageChange} noOfPages={noOfPages}/>
    </div>
  )
}

export default KdramasFilterSection
