import { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import "./App.css";

const API = "http://127.0.0.1:8000";
const COLORS = ["#4f46e5", "#06b6d4", "#f59e0b", "#10b981", "#ef4444", "#8b5cf6", "#ec4899"];

function Card({ title, children }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      {children}
    </div>
  );
}

function BarCard({ title, data }) {
  return (
    <Card title={title}>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#4f46e5" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </Card>
  );
}

function PieCard({ title, data }) {
  return (
    <Card title={title}>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie data={data} dataKey="count" nameKey="name" outerRadius={100} label>
            {data.map((item, index) => (
              <Cell key={item.name} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </Card>
  );
}

export default function App() {
  const [cities, setCities] = useState([]);
  const [categories, setCategories] = useState([]);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      axios.get(API + "/dashboard/city-count"),
      axios.get(API + "/dashboard/category-count"),
      axios.get(API + "/dashboard/source-count"),
    ])
      .then(([cityRes, categoryRes, sourceRes]) => {
        setCities(cityRes.data);
        setCategories(categoryRes.data);
        setSources(sourceRes.data);
      })
      .catch(() => setError("Could not load data. Is the FastAPI server running?"))
      .finally(() => setLoading(false));
  }, []);

  const total = cities.reduce((sum, item) => sum + item.count, 0);

  if (loading) return <p className="message">Loading...</p>;
  if (error) return <p className="message error">{error}</p>;

  return (
    <div className="page">
      <h1>Business Listings Dashboard</h1>
      <p className="subtitle">Total listings: {total}</p>
      <div className="grid">
        <BarCard title="City-wise Business Count" data={cities} />
        <BarCard title="Category-wise Business Count" data={categories} />
        <PieCard title="Source-wise Business Count" data={sources} />
      </div>
    </div>
  );
}