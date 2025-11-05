// Component to display a list of items (strings or numbers) as a comma-separated string

interface DisplayListProps {
  items: (string | number)[]; // array of items to display
}

const DisplayList: React.FC<DisplayListProps> = ({ items }) => {
  // Return null if no items provided
  if (!items || items.length === 0) return null;

  return (
    <p className="text-normal">
      {items.join(", ")} {/* Join items with commas */}
    </p>
  );
}

export default DisplayList;
