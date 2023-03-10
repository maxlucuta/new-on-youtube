import spinner from "./assets/loadingBlocks.gif";

function Spinner() {
  return (
    <div>
      <img
        src={spinner}
        style={{ width: '100px', margin: 'auto', display: 'block'}}
        alt="Loading..."
      />
    </div>
  );
};

export default Spinner;