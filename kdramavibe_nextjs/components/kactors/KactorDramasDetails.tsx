import { KactorDramas } from '@/interfaces';
import Link from 'next/link';
import React from 'react';

interface KactorDramasProps {
  kdramas: KactorDramas[];
}

const KactorDramasDetails: React.FC<KactorDramasProps> = ({ kdramas }) => {
  const capitalize = (text: string) =>
    text ? text.charAt(0).toUpperCase() + text.slice(1) : '';

  // Sort kdramas: PRESENT first, then descending by year
  const sortedDramas = [...kdramas].sort((a, b) => {
    if (a.year?.includes('PRESENT')) return -1;
    if (b.year?.includes('PRESENT')) return 1;

    // Extract first year from strings like "2016–2017"
    const getYearNum = (year: string) => parseInt(year.split('–')[0], 10) || 0;
    return getYearNum(b.year || '') - getYearNum(a.year || '');
  });

  return (
    <div className="rounded-2xl bg-background/80 shadow-lg text-text lg:w-3/4 w-full overflow-hidden">
      {/* Header */}
      <div className="bg-primary/80 text-white px-6 py-4">
        <h2 className="font-extrabold text-3xl tracking-wide">Dramas</h2>
      </div>

      {/* Table */}
      {sortedDramas.length > 0 ? (
        <div className="overflow-x-auto p-4">
          <table className="min-w-full text-left table-auto">
            <thead>
              <tr className="text-gray-400 uppercase text-sm">
                <th className="px-4 py-3 w-2/12">Year</th>
                <th className="px-4 py-3 w-5/12">Title</th>
                <th className="px-4 py-3 w-5/12">Role or Details</th>
              </tr>
            </thead>
            <tbody>
              {sortedDramas.map((kdrama) => (
                <tr
                  key={kdrama.kdrama_slug}
                  className="transition-colors duration-200 hover:bg-primary/10 rounded-lg"
                >
                  <td className="px-4 py-3 font-medium text-left">{kdrama.year}</td>
                  <td className="px-4 py-3">
                    <Link
                      href={`/k-dramas/${kdrama.kdrama_slug}`}
                      className="text-accent font-bold text-lg hover:underline"
                    >
                      {capitalize(kdrama.kdrama_title)}
                    </Link>
                  </td>
                  <td className="px-4 py-3 font-normal opacity-80">
                    {kdrama.role_name ? capitalize(kdrama.role_name) : '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-center text-gray-500 italic p-4">
          No cast information available.
        </p>
      )}
    </div>
  );
};

export default KactorDramasDetails;
