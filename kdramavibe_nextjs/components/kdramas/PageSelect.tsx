import { generatePagination } from '@/lib/generatePagination';
import React from 'react'

interface PageSelectProps {
    selectedPage: string;
    handlePageChange: (pageNo: string) => void;
    noOfPages: number;

}
const PageSelect: React.FC<PageSelectProps> = ({ selectedPage, handlePageChange, noOfPages }) => {
    const pagesToShow = generatePagination(noOfPages, Number(selectedPage));

  return (
    <div className='py-2'>
      <ul className='flex flex-wrap gap-4'>
       
        {pagesToShow.length > 0 && pagesToShow.map((page) => (<li key={page} >
            <button onClick={() => {
                handlePageChange(page.toString());


            }} className={`border-2 border-accent
             p-1 text-accent rounded-md
            ${Number(selectedPage) === page ? 'bg-primary text-white hover:text-white border-primary' : ''}
             text-center cursor-pointer 
             ${page === '...' ? '' : 'hover:text-primary hover:border-primary '}
             w-10 h-10 `}
             disabled={page === '...'}
             >{page}</button>
        </li>))}
        
      </ul>
    </div>
  )
}

export default PageSelect
