import React from "react";
import CircularProgress from "@mui/material/CircularProgress";

// Import styles
import "@react-pdf-viewer/core/lib/styles/index.css";
import "@react-pdf-viewer/default-layout/lib/styles/index.css";

import "./index.css";

export default function SideBar({
  summary,
  isSummaryLoading,
  isSummaryGenerating,
}) {
  function stringToColor(string) {
    let hash = 0;
    let i;

    /* eslint-disable no-bitwise */
    for (i = 0; i < string.length; i += 1) {
      hash = string.charCodeAt(i) + ((hash << 5) - hash);
    }

    let color = "#";

    for (i = 0; i < 3; i += 1) {
      const value = (hash >> (i * 8)) & 0xff;
      color += `00${value.toString(16)}`.slice(-2);
    }
    /* eslint-enable no-bitwise */

    return color;
  }

  function stringAvatar(name) {
    return {
      sx: {
        bgcolor: stringToColor(name),
      },
      children: `${name.split(" ")[0][0]}${name.split(" ")[1][0]}`,
    };
  }

  return (
    <div className="side-container">
      <div className="summary">
        <div className="summary-container">
          {Array.isArray(summary) && summary.length > 0 ? (
            <>
              {summary?.map((section) => (
                <div>
                  {section?.title && (
                    <h3 className="summary-subheading">{section.title}</h3>
                  )}
                  {/* <h2 className="summary-heading">{section.section}</h2> */}
                  {section?.response && (
                    <p style={{ textAlign: "left" }}>
                      {section?.response.result}
                    </p>
                  )}
                </div>
              ))}
            </>
          ) : (
            <></>
          )}
          {isSummaryGenerating && (
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: 8,
                minHeight: 32,
              }}
            >
              <CircularProgress size={18} />
              <span style={{ fontStyle: "italic", color: "#888" }}>
                Extracting more information...
              </span>
            </div>
          )}
        </div>
        {/* {isSummaryLoading && (
          <div className="summary-loader">
            <CircularProgress />
            <div>
              {!isSummaryLoading
                ? "Getting Error while fetching summary ..."
                : "Loading Summary ...."}
            </div>
          </div>
        )} */}
        {/* Export Button */}
        {Array.isArray(summary) &&
          summary.length > 0 &&
          !isSummaryGenerating && (
            <div
              style={{
                position: "absolute",
                right: "16px",
                top: "16px",
                textAlign: "center",
              }}
            >
              <button
                onClick={async () => {
                  try {
                    const response = await fetch(
                      `${process.env.REACT_APP_API_URL}/documents/export-csv/`,
                      {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(
                          summary.map((section) => ({
                            title: section.title || "",
                            content: section.response
                              ? section.response.result
                              : "",
                          }))
                        ),
                      }
                    );
                    if (!response.ok) throw new Error("Failed to export CSV");
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement("a");
                    a.href = url;
                    a.download = "export.csv";
                    document.body.appendChild(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                  } catch (err) {
                    alert("Failed to export CSV");
                  }
                }}
                style={{
                  padding: "8px 16px",
                  background: "#1976d2",
                  color: "#fff",
                  border: "none",
                  borderRadius: 4,
                  cursor: "pointer",
                  fontWeight: 600,
                }}
              >
                Export as CSV
              </button>
            </div>
          )}
      </div>
    </div>
  );
}
