/**
 * Generates an array of page numbers for pagination, including ellipses ("...") when needed.
 * 
 * @param noOfPages - Total number of pages available.
 * @param currentPage - Current active page number (1-based index).
 * @param delta - Number of pages to show around the current page (default 2).
 * @returns An array of numbers and/or strings representing pages to display.
 */

export const generatePagination = (
  noOfPages: number, 
  currentPage: number, 
  delta: number = 2
): (number | string)[] => {
  const pages: (number | string)[] = [];

  // Calculate the start and end page numbers for the pagination window
  const startPage = Math.max(1, currentPage - delta);
  const endPage = Math.min(noOfPages, currentPage + delta);

  // Always include the first page if startPage is not 1
  if (startPage !== 1) pages.push(1);

  // Add ellipsis if there's a gap between first page and startPage
  if (startPage > 2 && noOfPages > 2) pages.push("...");

  // Add the pages in the window between startPage and endPage
  pages.push(...Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i));

  // Add ellipsis if there's a gap between endPage and last page
  if (endPage < noOfPages - 1 && noOfPages > 1) pages.push("...");

  // Always include the last page if endPage is not the last page
  if (endPage !== noOfPages) pages.push(noOfPages);

  return pages;
};

