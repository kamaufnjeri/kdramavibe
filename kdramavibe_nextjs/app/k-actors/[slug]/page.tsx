// Import the KactorDetails component
import KactorDetails from "@/components/kactors/KactorDetails";
// Import the function to fetch a single Kactor by slug
import getSingleKactor from "@/lib/getSingleKactor";

// Define the props type for this page
interface PageProps {
  params: {
    slug: string;
  };
}

/**
 * SingleKactorPage component
 * Fetches a single Kactor by slug and renders the KactorDetails component.
 *
 * @param {PageProps} params - The page parameters containing the slug.
 * @returns {Promise<JSX.Element>} The rendered Kactor page.
 */
export default async function SingleKactorPage({ params }: PageProps) {
  const { slug } = params; // Destructure slug from params

  // Fetch the Kactor data from API or backend
  const kactor = await getSingleKactor(slug);

  return (
    // Container div to center the KactorDetails component
    <div className="flex justify-center m-4 p-4">
      <KactorDetails kactor={kactor} />
    </div>
  );
}
