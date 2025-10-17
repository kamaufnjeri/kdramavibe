export const generatePagination = (noOfPages: number, currentPage: number, delta: number = 2): (number | string)[] => {
    const pages: (number | string)[] = [];
    const startPage = Math.max(1, currentPage - delta) 

    const endPage = Math.min(noOfPages, currentPage + delta)
    if (startPage !== 1) pages.push(1)


    if (startPage > 2 && noOfPages > 2) pages.push("...")
    pages.push(...Array.from({ length: endPage - startPage + 1}, (_, i) => startPage + i));

    if (endPage < noOfPages - 1 && noOfPages > 1) pages.push('...')
    if (endPage !== noOfPages) pages.push(noOfPages);
    
    return pages;
}