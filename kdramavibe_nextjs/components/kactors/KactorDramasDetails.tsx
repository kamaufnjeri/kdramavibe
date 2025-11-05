import { KactorDramas } from '@/interfaces';
import Link from 'next/link';
import React from 'react';

interface KactorDramasProps {
  kdramas: KactorDramas[]; // Array of dramas for the Kactor
}

const KactorDramasDetails: React.FC<KactorDramasProps> = ({ kdramas }) => {
  // Helper function to capitalize first letter
  const capitalize = (text: string) =>
    text ? text.charAt(0).toUpperCase() + text.slice(1) : '';

  return (
    <div className="rounded-2xl bg-background/80 shadow-lg text-text lg:w-3/4 w-full overflow-hidden">
      
      {/* Header */}
      <div className="bg-primary/80 text-white px-6 py-4">
        <h2 className="font-extrabold text-3xl tracking-wide">Dramas</h2>
      </div>

      {/* Dramas Table */}
      {kdramas.length > 0 ? (
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
              {kdramas.map((kdrama) => (
                <tr
                  key={kdrama.kdrama_slug}
                  className="transition-colors duration-200 hover:bg-primary/10 rounded-lg"
                >
                  {/* Year of the drama */}
                  <td className="px-4 py-3 font-medium text-left">{kdrama.year}</td>

                  {/* Drama title with link */}
                  <td className="px-4 py-3">
                    <Link
                      href={`/k-dramas/${kdrama.kdrama_slug}`}
                      className="text-accent font-bold text-lg hover:underline"
                    >
                      {capitalize(kdrama.kdrama_title)}
                    </Link>
                  </td>

                  {/* Role name or placeholder */}
                  <td className="px-4 py-3 font-normal opacity-80">
                    {kdrama.role_name ? capitalize(kdrama.role_name) : '-'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        // Display when no dramas are available
        <p className="text-center text-gray-500 italic p-4">
          No cast information available.
        </p>
      )}
    </div>
  );
};

export default KactorDramasDetails;
