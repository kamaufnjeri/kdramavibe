'use client'

import React, { useEffect, useState } from 'react'
import { FaSync } from 'react-icons/fa'
import { KactorsFilter } from '@/interfaces'
import PageSelect from '../kdramas/PageSelect'
import AgesAutoComplete from './AgeAutocomplete'
import GendersSelect from './GenderSelect'
import Pill from '../common/Pill'
import OrderByOptions from './OrderByOptions'

interface KactorFilterSectionProps {
  searchParams: KactorsFilter // initial search parameters
  noOfPages: number // total number of pages for pagination
}

const KactorsFilterSection: React.FC<KactorFilterSectionProps> = ({ searchParams, noOfPages }) => {
  // Local state for filters in form inputs
  const [filters, setFilters] = useState<KactorsFilter>(searchParams)
  // State for pills display of active filters
  const [pillsFilters, setPillsFilters] = useState<KactorsFilter>(searchParams);
  
  useEffect(() => {
    setFilters(searchParams);
    setPillsFilters(searchParams);
  }, [searchParams]);


  const navigateWithReload = (path: string) => {
    window.location.href = path;
  };



  // Reset all filters and redirect to base k-actors page
  const handleFormReset = () => {
    setFilters({
      name: '',
      age: '',
      gender: '',
      ordering: '',
      page: '1'
    })
    setPillsFilters({
      name: '',
      age: '',
      gender: '',
      ordering: '',
      page: '1'
    })
    
    navigateWithReload('/k-actors')
  }

  // Convert filters object to URL query string
  const getQuery = (filtersToUse: KactorsFilter): string => {
    const query = new URLSearchParams({
      ...(filtersToUse?.name ? { name: filtersToUse.name } : {}),
      ...(filtersToUse?.age ? { age: filtersToUse.age } : {}),
      ...(filtersToUse?.gender ? { gender: filtersToUse?.gender.toLowerCase() } : {}),
      ...(filtersToUse?.ordering ? { ordering: filtersToUse.ordering } : {}),
    }).toString()
    return query
  }

  // Handle change of any filter input
  const handleChange = (key: string, value: string) => {
    const updatedFilters = { ...filters, [key]: value }
    setFilters(updatedFilters)
  }

  // Handle Enter key press in input fields
  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    const target = e.target as HTMLInputElement
    const { name, value } = target

    if (e.key === 'Enter') {
      e.preventDefault()
      const updatedFilters = { ...filters, [name]: value }
      setFilters(updatedFilters)
      setPillsFilters(updatedFilters)

      const query = getQuery(updatedFilters)
      navigateWithReload(`/k-actors/?${query}`)
    }
  }

  // Handle page selection changes
  const handlePageChange = (pageNo: string) => {
    const updatedFilters = { ...filters, page: pageNo }
    setFilters(updatedFilters)
    const query = new URLSearchParams({
      ...(updatedFilters?.name ? { name: updatedFilters.name } : {}),
      ...(updatedFilters?.age ? { age: updatedFilters.age } : {}),
      ...(updatedFilters?.gender ? { gender: updatedFilters?.gender.toLowerCase() } : {}),
      ...(updatedFilters?.ordering ? { ordering: updatedFilters.ordering } : {}),
      ...(updatedFilters?.page ? { page: updatedFilters?.page } : {}),
    }).toString()

    navigateWithReload(`/k-actors/?${query}`)
  }

  // Remove individual filter field (used by Pill component)
  const resetFilterField = (key: string, value: string) => {
    const updatedFilters = { ...filters, [key]: value }
    setFilters(updatedFilters)
    setPillsFilters(updatedFilters)
    const query = new URLSearchParams({
      ...(updatedFilters?.name ? { name: updatedFilters.name } : {}),
      ...(updatedFilters?.age ? { genre: updatedFilters.age } : {}),
      ...(updatedFilters?.gender ? { year: updatedFilters?.gender } : {}),
      ...(updatedFilters?.ordering ? { ordering: updatedFilters.ordering } : {}),
      ...(updatedFilters?.page ? { page: updatedFilters?.page } : {}),
    }).toString()
    navigateWithReload(`/k-actors/?${query}`)
  }

  // Handle form submission (Search button)
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setPillsFilters(filters)
    const query = getQuery(filters)
    navigateWithReload(`/k-actors/?${query}`)
  }

  return (
    <div className='w-full px-4 py-4 flex flex-col gap-4'>
      <form className="flex flex-wrap items-start md:items-center lg:items-center" onSubmit={handleSubmit}>
        {/* Name input */}
        <div className='w-full md:w-1/2 lg:w-1/4 p-2'>
          <input
            type="text"
            name='name'
            value={filters.name}
            onChange={(e) => handleChange(e.target.name, e.target.value)}
            onKeyDown={onKeyDown}
            placeholder="Type name..."
            className="
              w-full rounded-xl px-4 py-2
              border-2 border-accent 
              text-input-text
            bg-input-bg
            placeholder:text-pink-500
              focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary
              hover:border-primary transition-colors duration-200
            "
          />
        </div>

        {/* Age and Gender Filters */}
        <AgesAutoComplete selectedAge={filters.age} handleChange={handleChange} />
        <GendersSelect selectedGender={filters.gender} handleChange={handleChange} />

        {/* Search & Reset Buttons */}
        <div className='flex flex-row justify-between gap-3 w-full lg:w-1/4 md:w-1/2 p-2'>
        <button
            type='submit'
            className='cursor-pointer border-accent text-accent hover:text-white hover:bg-primary hover:border-primary rounded-xl px-4 py-2 border-2'
          >
            Apply
          </button>          
          <button type='button' className='border-none cursor-pointer' onClick={handleFormReset}>
            <FaSync className='text-2xl font-bold text-accent hover:text-primary'/>
          </button>
        </div>
      </form>

      {/* Ordering and Pagination */}
      <div className='flex sm:flex-row gap-2 flex-col items-end sm:justify-between'>
        <OrderByOptions selectedOrderBy={filters.ordering} handleChange={handleChange} />
        <PageSelect selectedPage={filters.page} handlePageChange={handlePageChange} noOfPages={noOfPages} />
      </div>

      {/* Display Pills for active filters */}
      <div>
        <ul className='flex flex-wrap gap-2 px-2'>
          {pillsFilters && Object.entries(pillsFilters).map(([key, value]) =>
            (value && !['ordering', 'page'].includes(key)) ? (
              <li key={key}>
                <Pill
                  fieldKey={key} // matches Pill prop
                  value={value}
                  resetFilterField={resetFilterField} // handler for removing pill
                />
              </li>
            ) : null
          )}
        </ul>
      </div>
    </div>
  )
};

export default KactorsFilterSection;