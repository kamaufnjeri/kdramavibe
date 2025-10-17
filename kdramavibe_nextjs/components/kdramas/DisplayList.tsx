interface DisplayListProps {
    items: (string | number)[];
}

const DisplayList:React.FC<DisplayListProps> = ({ items }) => {
  if (!items || items.length === 0) return null;

  return (
    <p className="text-normal">
      {items.join(", ")}
    </p>
  );
}

export default DisplayList;
