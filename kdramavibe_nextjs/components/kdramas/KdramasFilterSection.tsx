'use client'

import React, { useEffect, useState } from 'react'
import GenresAutoComplete from './GenresAutoComplete'
import YearsSelect from './YearsSelect'
import { FaSync } from 'react-icons/fa'
import { KdramasFilter } from '@/interfaces'
import PageSelect from './PageSelect'
import Pill from '../common/Pill'
import OrderByOptions from './OrderByOptions'

interface KdramaFilterSectionProps {
  searchParams: KdramasFilter; // initial filters from URL or props
  noOfPages: number; // total pages for pagination
}

const KdramasFilterSection: React.FC<KdramaFilterSectionProps> = ({ searchParams, noOfPages }) => {
  // State to manage current filter inputs
  const [filters, setFilters] = useState<KdramasFilter>(searchParams);
  // State to manage pills (active filters display)
  const [pillsFilters, setPillsFilters] = useState<KdramasFilter>(searchParams);

  useEffect(() => {
    setFilters(searchParams);
    setPillsFilters(searchParams);
  }, [searchParams]);

  const navigateWithReload = (path: string) => {
    window.location.href = path;

  };

  // Reset all filters to defaults
  const handleFormReset = () => {
    setFilters({
      title: '',
      genre: '',
      year: '',
      ordering: '',
      page: '1'
    });
    setPillsFilters({
      title: '',
      genre: '',
      year: '',
      ordering: '',
      page: '1'
    });
    navigateWithReload('/'); // navigate to home with no filters
  }

  // Convert filters object to query string
  const getQuery = (filtersToUse: KdramasFilter): string => {
    const query = new URLSearchParams({
      ...(filtersToUse?.title ? { title: filtersToUse.title } : {}),
      ...(filtersToUse?.genre ? { genre: filtersToUse.genre } : {}),
      ...(filtersToUse?.year ? { year: filtersToUse.year } : {}),
      ...(filtersToUse?.ordering ? { ordering: filtersToUse.ordering } : {}),
    }).toString();
    return query;
  }

  // Handle input changes and update filters state
  const handleChange = (key: string, value: string) => {
    const updatedFilters = { ...filters, [key]: value };
    setFilters(updatedFilters);
  }

  // Handle Enter key submission for text inputs
  const onKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    const target = e.target as HTMLInputElement;
    const { name, value } = target;

    if (e.key === 'Enter') {
      e.preventDefault(); // prevent form submission

      const updatedFilters = { ...filters, [name]: value };
      setFilters(updatedFilters);
      setPillsFilters(updatedFilters);

      const query = getQuery(updatedFilters);
      navigateWithReload(`/?${query}`);
    }
  };

  // Handle pagination
  const handlePageChange = (pageNo: string) => {
    const updatedFilters = { ...filters, page: pageNo };
    setFilters(updatedFilters);
    setPillsFilters(updatedFilters);

    const query = new URLSearchParams({
      ...(updatedFilters?.title ? { title: updatedFilters.title } : {}),
      ...(updatedFilters?.genre ? { genre: updatedFilters.genre } : {}),
      ...(updatedFilters?.year ? { year: updatedFilters.year } : {}),
      ...(updatedFilters?.ordering ? { ordering: updatedFilters.ordering } : {}),
      ...(updatedFilters?.page ? { page: updatedFilters?.page } : {}),
    }).toString();

    navigateWithReload(`/?${query}`);
  }

  // Reset a single filter field via pill click
  const resetFilterField = (key: string, value: string) => {
    const updatedFilters = { ...filters, [key]: value };
    setFilters(updatedFilters);
    setPillsFilters(updatedFilters);

    const query = new URLSearchParams({
      ...(updatedFilters?.title ? { title: updatedFilters.title } : {}),
      ...(updatedFilters?.genre ? { genre: updatedFilters.genre } : {}),
      ...(updatedFilters?.year ? { year: updatedFilters.year } : {}),
      ...(updatedFilters?.ordering ? { ordering: updatedFilters.ordering } : {}),
      ...(updatedFilters?.page ? { page: updatedFilters?.page } : {}),
    }).toString();

    navigateWithReload(`/?${query}`);
  };

  // Handle form submission (Apply button)
  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setPillsFilters(filters);

    const query = getQuery(filters);
    navigateWithReload(`/?${query}`);
  }

  return (
    <div className='w-full p-4 flex flex-col gap-4'>
      {/* Filter Form */}
      <form className="flex flex-wrap items-start md:items-center lg:items-center" onSubmit={handleSubmit}>
        {/* Title Input */}
        <div className='w-full md:w-1/2 lg:w-1/4 p-2'>
          <input
            type="text"
            name='title'
            value={filters.title}
            onChange={(e) => handleChange(e.target.name, e.target.value)}
            onKeyDown={onKeyDown}
            placeholder="Type title..."
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

        {/* Genre & Year Select */}
        <GenresAutoComplete selectedGenre={filters.genre} handleChange={handleChange} />
        <YearsSelect selectedYear={filters.year} handleChange={handleChange} />

        {/* Submit & Reset Buttons */}
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

      {/* Order & Pagination */}
      <div className='flex flex-wrap justify-between items-end w-full'>
        <OrderByOptions selectedOrderBy={filters.ordering} handleChange={handleChange}/>
        <PageSelect selectedPage={filters.page} handlePageChange={handlePageChange} noOfPages={noOfPages}/>
      </div>

      {/* Active Filter Pills */}
      <div>
        <ul className='flex flex-wrap gap-3 p-2'>
          {pillsFilters && Object.entries(pillsFilters).map(([key, value]) =>
            (value && !['ordering', 'page'].includes(key)) ? (
              <li key={key}>
                <Pill
                  fieldKey={key}        // key for Pill component
                  value={value}
                  resetFilterField={resetFilterField} // handler to remove pill
                />
              </li>
            ) : null
          )}
        </ul>
      </div>
    </div>
  )
}

export default KdramasFilterSection
