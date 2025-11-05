import { generatePagination } from '@/lib/generatePagination';
import React from 'react';

interface PageSelectProps {
  selectedPage: string; // Currently selected page number as string
  handlePageChange: (pageNo: string) => void; // Callback to handle page change
  noOfPages: number; // Total number of pages available
}

const PageSelect: React.FC<PageSelectProps> = ({ selectedPage, handlePageChange, noOfPages }) => {
  // Generate the array of page numbers and ellipsis based on total pages and current page
  const pagesToShow = generatePagination(noOfPages, Number(selectedPage));

  return (
    <div className='py-2'>
      <ul className='flex flex-wrap gap-4'>
        {/* Render each page as a button */}
        {pagesToShow.length > 0 && pagesToShow.map((page) => (
          <li key={page}>
            <button
              onClick={() => {
                handlePageChange(page.toString()); // Trigger page change
              }}
              className={`
                border-2 border-accent
                p-1 text-accent rounded-md
                ${Number(selectedPage) === page ? 'bg-primary text-white hover:text-white border-primary' : ''}
                text-center cursor-pointer 
                ${page === '...' ? '' : 'hover:text-primary hover:border-primary '}
                w-10 h-10
              `}
              disabled={page === '...'} // Disable ellipsis buttons
            >
              {page}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default PageSelect;
