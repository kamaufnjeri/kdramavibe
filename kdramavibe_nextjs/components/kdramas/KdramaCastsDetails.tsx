import { KdramaCasts } from '@/interfaces';
import Link from 'next/link';
import React from 'react';

interface KdramaCastsProps {
  kactors: KdramaCasts[];
}

const KdramaCastsDetails: React.FC<KdramaCastsProps> = ({ kactors }) => {
  // Capitalize the first letter of a string safely
  const capitalize = (text: string) =>
    text ? text.charAt(0).toUpperCase() + text.slice(1) : '';

  return (
    <div className="rounded-2xl border border-border bg-background/60 shadow-sm 
                    text-text lg:w-3/4 w-full flex flex-col overflow-hidden">
      
      {/* Header */}
      <div className="bg-primary/80 text-white px-4 py-3">
        <h2 className="font-extrabold text-2xl tracking-wide">Casts</h2>
      </div>

      {/* Body */}
      <div className="p-6">
        {Array.isArray(kactors) && kactors.length > 0 ? (
          <ul className="flex flex-wrap w-full">
            {kactors.map((kactor) => (
              <li
                key={kactor.kactor_slug}
                className="p-3 w-full sm:w-1/2 lg:w-1/3"
              >
                <div className="border border-border rounded-xl p-4 h-full flex flex-col hover:shadow-md transition">
                  <Link
                    href={`/k-actors/${kactor.kactor_slug}`}
                    className="text-accent hover:underline font-semibold text-lg transition"
                  >
                    {capitalize(kactor.kactor_name)}
                  </Link>

                  {kactor.role_name && (
                    <p className="pt-1 text-sm text-gray-500">
                      {capitalize(kactor.role_name)}
                    </p>
                  )}
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-center text-gray-500 italic">
            No cast information available.
          </p>
        )}
      </div>
    </div>
  );
};

export default KdramaCastsDetails;
