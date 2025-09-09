import { useState } from "react";
import { AiOutlineClose } from "react-icons/ai";
import { useNavigate } from "react-router-dom";

const SearchPlan = () => {
  const [uuid, setUuid] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleClose = () => {
    navigate("/create-plan");
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const res = await fetch(`http://13.250.98.246:5599/get-plan/${uuid}`);
      if (!res.ok) throw new Error("Plan not found");
      navigate(`/view-plan/${uuid}`);
    } catch (err: any) {
      setError(err.message || "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center">
      <div className="bg-white p-6 rounded shadow-md w-[300px] relative">
        <button
          onClick={handleClose}
          className="absolute top-2 right-2 text-gray-500 hover:text-red-500"
        >
          <AiOutlineClose size={20} />
        </button>
        <h2 className="text-lg font-bold text-center mb-4">Enter Plan UUID</h2>
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <input
            type="text"
            value={uuid}
            onChange={(e) => setUuid(e.target.value)}
            className="border px-3 py-2 rounded text-sm"
            placeholder="UUID..."
            required
          />
          <button
            type="submit"
            className="bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
            disabled={loading}
          >
            {loading ? "Loading..." : "Submit"}
          </button>
          {error && (
            <p className="text-sm text-red-500 text-center">{error}</p>
          )}
        </form>
      </div>
    </div>
  );
};

export default SearchPlan;