import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Pie } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

function App() {
  const [summary, setSummary] = useState(null);
  const [typeData, setTypeData] = useState(null);
  const [history, setHistory] = useState([]);
  const [status, setStatus] = useState("");
  const [fileInfo, setFileInfo] = useState("");

  // ---------- FETCH HISTORY ----------
  const fetchHistory = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/history/");
      setHistory(res.data);
    } catch (err) {
      console.error("History fetch failed");
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  // ---------- ✅ UPLOAD FILE (THIS WAS MISSING) ----------
  const uploadFile = async (e) => {
    if (!e.target.files[0]) return;

    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    try {
      setStatus("uploading");

      const res = await axios.post(
        "http://127.0.0.1:8000/api/upload/",
        formData
      );

      const now = new Date().toLocaleString();

      setSummary(res.data);
      setTypeData(res.data.type_distribution);
      setFileInfo(`File: ${file.name} • Uploaded at: ${now}`);
      setStatus("success");

      fetchHistory();
    } catch (err) {
      console.error(err.response?.data || err.message);
      setStatus("error");
    }
  };

  // ---------- DOWNLOAD PDF ----------
  const downloadPDF = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/api/report/pdf/",
        { responseType: "blob" }
      );

      const blob = new Blob([res.data], { type: "application/pdf" });
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "equipment_report.pdf";
      a.click();

      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error("PDF download failed");
    }
  };

  // ---------- CLEAR ----------
  const clearAll = () => {
    setSummary(null);
    setTypeData(null);
    setStatus("");
    setFileInfo("");
  };

  return (
    <div className="app">
      <div className="glass-card fade-in">

        {/* HEADER */}
        <div className="header">
          <h1>Chemical Equipment Dashboard</h1>

          {summary && (
            <div className="header-actions">
              <button className="pdf-btn" onClick={downloadPDF}>
                Download PDF
              </button>

              <button className="clear-btn" onClick={clearAll}>
                Clear
              </button>
            </div>
          )}
        </div>

        <p className="subtitle">
          Upload CSV file to analyze chemical equipment parameters
        </p>

        <input
          type="file"
          className="file-input"
          onChange={uploadFile}
        />

        {/* STATUS */}
        {status && (
          <div className={`status ${status}`}>
            {status === "uploading" && "Uploading..."}
            {status === "success" && "Uploaded Successfully ✓"}
            {status === "error" && "Upload Failed"}
          </div>
        )}

        {fileInfo && <div className="file-info">{fileInfo}</div>}

        {/* MAIN CONTENT */}
        {summary && (
          <>
            <div className="content fade-in">

              {/* LEFT */}
              <div className="summary">
  <div className="result-box">
    <span>Total Equipment</span>
    <strong>{summary.total_count}</strong>
  </div>

  <div className="result-box">
    <span>Avg Flowrate</span>
    <strong>{summary.avg_flowrate.toFixed(2)}</strong>
  </div>

  <div className="result-box">
    <span>Avg Pressure</span>
    <strong>{summary.avg_pressure.toFixed(2)}</strong>
  </div>

  <div className="result-box">
    <span>Avg Temperature</span>
    <strong>{summary.avg_temperature.toFixed(2)}</strong>
  </div>
</div>


              {/* RIGHT */}
              {typeData && (
                <div className="chart-box">
                  <h3>Equipment Distribution</h3>

                  <div className="chart-wrapper">
                    <Pie
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                      }}
                      data={{
                        labels: Object.keys(typeData),
                        datasets: [
                          {
                            data: Object.values(typeData),
                            backgroundColor: [
                              "#a855f7",
                              "#6366f1",
                              "#22d3ee",
                              "#f472b6",
                            ],
                            borderWidth: 0,
                          },
                        ],
                      }}
                    />
                  </div>
                </div>
              )}
            </div>

            {/* HISTORY */}
            {history.length > 0 && (
              <div className="history-box fade-in">
                <h3>Recent Uploads</h3>

                {history.map((item, i) => (
                  <div key={i} className="history-item">
                    <span>{item.filename}</span>
                    <span>{item.total_count} items</span>
                  </div>
                ))}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

export default App;
