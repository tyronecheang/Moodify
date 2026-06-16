import { useEffect } from "react";

function App() {
  useEffect(() => {
    const testFlask = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/");
        const data = await response.json();
        console.log(data);
      } catch (err) {
        console.error("Error fetching Flask:", err);
      }
    };

    testFlask();
  }, []);

  return <div>Testing Flask API...</div>;
}

export default App;
