import React, { useEffect, useState } from "react";
import ChatApp from "./components/ChatApp/ChatApp";
import { Viewer, Worker } from "@react-pdf-viewer/core";
import { defaultLayoutPlugin } from "@react-pdf-viewer/default-layout";
import Header from "./components/Header";
import Landing from "./Landing";

import "@react-pdf-viewer/core/lib/styles/index.css";
import "@react-pdf-viewer/default-layout/lib/styles/index.css";

import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    // {
    //   text: "Hi. I'm your AI assistant ... Let me know how can i help you",
    //   sender: "bot",
    // },
  ]);
  const [summary, setSummary] = useState([]);
  const [toogleSummary, setToogleSummary] = useState(false);
  const [isSummaryLoading, setIsSummaryLoading] = useState(false);
  const [isSummaryGenerating, setIsSummaryGenerating] = useState(false);
  const [inputText, setInputText] = useState("");
  const [pdfFile, setPdfFile] = useState(null);
  const [viewPdf, setViewPdf] = useState(null);

  console.log({ pdfFile, viewPdf });
  const plugin = defaultLayoutPlugin();

  const addSummaryItem = React.useCallback((item) => {
    setSummary((prev) => {
      console.log("prev", prev);
      console.log("item", item);
      return [...prev, item];
    });
  }, []);

  const handleStreamSummary = React.useCallback(
    async (fileName) => {
      setIsSummaryLoading(true);
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/documents/stream-summary`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            files: [fileName],
          }),
        }
      );

      if (!response.body) return;

      setIsSummaryGenerating(true);
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        let lines = buffer.split("\n");
        buffer = lines.pop(); // last line may be incomplete

        for (const line of lines) {
          if (line.trim()) {
            const data = JSON.parse(line);
            addSummaryItem(data); // Update your state/UI with each streamed answer
            // Example: setSummary(prev => [...prev, data]);
          }
        }
      }
      setIsSummaryGenerating(false);
      setIsSummaryLoading(false);
    },
    [addSummaryItem]
  );

  // const fetchSummary = async (fileName) => {
  //   try {
  //     setIsSummaryLoading(true);
  //     const response = await fetch(
  //       `${process.env.REACT_APP_API_URL}/documents/summary`,
  //       {
  //         method: "POST",
  //         body: JSON.stringify({
  //           files: [fileName],
  //         }),
  //         headers: {
  //           Accept: "application/json",
  //           "content-type": "application/json",
  //         },
  //       }
  //     );
  //     const res = await response.json();

  //     setSummary(res);
  //     setIsSummaryLoading(false);
  //   } catch (e) {
  //     setIsSummaryLoading(false);
  //     console.log("error", e);
  //   }
  // };

  useEffect(() => {
    if (toogleSummary && pdfFile) {
      // fetchSummary(pdfFile.name);
      handleStreamSummary(pdfFile.name);
    }
  }, [toogleSummary, handleStreamSummary, pdfFile]);

  return (
    <div className="root-App">
      <Header
        pdfFile={pdfFile}
        setPdfFile={setPdfFile}
        setViewPdf={setViewPdf}
        setSummary={setSummary}
        setMessages={setMessages}
        setToogleSummary={setToogleSummary}
      />
      <div className="App">
        {pdfFile ? (
          <>
            <div className="pdf-viewer">
              <Worker
                workerUrl={`https://unpkg.com/pdfjs-dist@3.11.174/build/pdf.worker.min.js`}
              >
                {viewPdf && <Viewer fileUrl={viewPdf} plugins={[plugin]} />}
                {!viewPdf && <>No PDF uploaded yet</>}
              </Worker>
            </div>
            <div className="chat-block">
              <ChatApp
                key={(pdfFile && pdfFile.name) || ""}
                pdfFile={pdfFile}
                messages={messages}
                setMessages={setMessages}
                inputText={inputText}
                setInputText={setInputText}
                summary={summary}
                isSummaryLoading={isSummaryLoading}
                isSummaryGenerating={isSummaryGenerating}
                toogleSummary={toogleSummary}
                setToogleSummary={setToogleSummary}
              />
            </div>
          </>
        ) : (
          <Landing />
        )}
      </div>
    </div>
  );
}

export default App;
