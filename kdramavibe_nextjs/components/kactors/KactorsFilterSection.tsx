'use client'

import React, { useState } from 'react'
import { FaSync } from 'react-icons/fa'
import { useRouter } from 'next/navigation'
import { KactorsFilter } from '@/interfaces'
import PageSelect from '../kdramas/PageSelect'
import AgesAutoComplete from './AgeAutocomplete'
import GendersSelect from './GenderSelect'


interface KactorFilterSectionProps {
  searchParams: KactorsFilter;
  noOfPages: number
}

const KactorsFilterSection: React.FC<KactorFilterSectionProps> = ({ searchParams, noOfPages }) => {
  const [filters, setFilters] = useState<KactorsFilter>(searchParams);
  const router = useRouter();

  const handleFormReset = () => {
    setFilters({
      name: '',
      age: '',
      gender: '',
      page: '1'
    });
    router.push('/k-actors')
  }

   const getQuery = (filtersToUse: KactorsFilter): string => {
    const query = new URLSearchParams({
      ...(filtersToUse?.name ? { name: filtersToUse.name } : {}),
      ...(filtersToUse?.age ? { age: filtersToUse.age } : {}),
      ...(filtersToUse?.gender ? { gender: filtersToUse?.gender.toLowerCase() } : {}),
    }).toString();
    return query;
  }
  const handleChange = (key: string, value: string) => {
    const updatedFilters = {...filters, [key]: value};
    setFilters(updatedFilters);

    if (key === 'gender') {
      const query = getQuery(updatedFilters);
      router.push(`/k-actors/?${query}`);
    }
    
  }

  const handlePageChange = (pageNo: string) => {
    const updatedFilters = {...filters, page: pageNo};
    setFilters(updatedFilters);
    const query = new URLSearchParams({
      ...(updatedFilters?.name ? { name: updatedFilters.name } : {}),
      ...(updatedFilters?.age ? { age: updatedFilters.age } : {}),
      ...(updatedFilters?.gender ? { gender: updatedFilters?.gender.toLowerCase() } : {}),
      ...(updatedFilters?.page ? { page: updatedFilters?.page } : {}),

    }).toString();

    router.push(`/k-actors/?${query}`);
  }

 

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const query = getQuery(filters);

    router.push(`/k-actors/?${query}`);
  }


  return (
    <div className='w-full p-4 flex flex-col gap-4'>
      <form className="flex flex-wrap items-start md:items-center lg:items-center" onSubmit={handleSubmit}>
        <div className='w-full md:w-1/2 lg:w-1/4 p-2'>
          <input type="text" name='name' 
          value={filters.name}
          onChange={(e) => handleChange(e.target.name, e.target.value)}
      placeholder="Type name..."
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
        <AgesAutoComplete selectedAge={filters.age} handleChange={handleChange}/>
        <GendersSelect selectedGender={filters.gender} handleChange={handleChange}/>
        <div className='flex flex-row justify-between gap-3 w-full lg:w-1/4 md:w-1/2 p-2'>
           <button type='submit' className='cursor-pointer border-accent text-accent hover:text-white hover:bg-primary hover:border-primary rounded-xl px-4 py-2 border-2'>Search</button>
        <button type='button' className='border-none cursor-pointer' onClick={handleFormReset}><FaSync className='text-2xl font-bold text-accent hover:text-primary'/></button>
        </div>
       
      </form>
      <PageSelect selectedPage={filters.page} handlePageChange={handlePageChange} noOfPages={noOfPages}/>
    </div>
  )
}

export default KactorsFilterSection
