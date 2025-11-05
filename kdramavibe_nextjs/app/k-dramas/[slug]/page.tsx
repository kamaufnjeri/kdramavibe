// Import Kdrama detail component
import KdramaDetails from "@/components/kdramas/KdramaDetails";
// Import function to fetch single Kdrama data
import getSingleKdrama from "@/lib/getSingleKdrama";

// Define props for the page
interface PageProps {
  params: {
    slug: string; // The slug identifier for the Kdrama
  };
}

/**
 * SingleKdramaPage component
 * Fetches a single Kdrama based on the slug and renders the details.
 *
 * @param {PageProps} params - The route parameters containing the Kdrama slug.
 * @returns {Promise<JSX.Element>} The rendered page with Kdrama details.
 */
export default async function SingleKdramaPage({ params }: PageProps) {
  const { slug } = params; // Destructure slug from params

  // Fetch the Kdrama data by slug
  const kdrama = await getSingleKdrama(slug);

  return (
    <div className="flex justify-center m-4 p-4">
      {/* Render the Kdrama details component */}
      <KdramaDetails kdrama={kdrama} />
    </div>
  );
}
