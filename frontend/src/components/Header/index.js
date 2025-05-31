import React, { useState, useEffect } from "react";
import DeloitteLogo from "../../Group.png";
import { styled } from "@mui/material/styles";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import SpeedDial from "@mui/material/SpeedDial";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import CircularProgress from "@mui/material/CircularProgress";

import "./index.css";

const VisuallyHiddenInput = styled("input")({
  clip: "rect(0 0 0 0)",
  clipPath: "inset(50%)",
  height: 1,
  overflow: "hidden",
  position: "absolute",
  bottom: 0,
  left: 0,
  whiteSpace: "nowrap",
  width: 1,
});

const StyledSpeedDial = styled(SpeedDial)(({ theme }) => ({
  position: "absolute",
  "&.MuiSpeedDial-directionUp, &.MuiSpeedDial-directionLeft": {
    bottom: theme.spacing(2),
    right: theme.spacing(2),
  },
  "&.MuiSpeedDial-directionDown, &.MuiSpeedDial-directionRight": {
    top: theme.spacing(2),
    left: theme.spacing(2),
  },
}));

const Header = ({
  pdfFile,
  setPdfFile,
  setViewPdf,
  setSummary,
  setMessages,
  setToogleSummary,
}) => {
  const [fileStack, setFileStack] = useState([]);
  const [isUploadLoading, setIsUploadLoading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [hidden, setHidden] = useState(false);
  const fileType = ["application/pdf"];

  const loadFiles = async () => {
    try {
      const response = await fetch(
        `${process.env.REACT_APP_API_URL}/documents/getfiles/`,
        {
          method: "GET",
          headers: {
            Accept: "application/json",
            "content-type": "application/json",
          },
        }
      );
      const res = await response.json();
      if (res && res.files && res.files.length) {
        // setPdfFile(res.files[0]);
        // setViewPdf(`data:application/pdf;base64,${res.files[0].result}`);
        setFileStack(
          res.files.map((item) => ({
            file: {
              name: item.name,
              file: { name: item.name },
              result: `data:application/pdf;base64,${item.result}`,
            },
          }))
        );
      }
      console.log(res);
    } catch (e) {
      console.log("error", e);
    }
  };

  const handleUploadFileChange = async (e) => {
    try {
      let selectedFile = e.target.files[0];
      if (selectedFile) {
        if (selectedFile && fileType.includes(selectedFile.type)) {
          setIsUploadLoading(true);
          const formData = new FormData();
          formData.append("file", selectedFile);
          console.log("aaaaa", formData);
          const response = await fetch(
            `${process.env.REACT_APP_API_URL}/documents/uploadfile/`,
            {
              method: "POST",
              body: formData,
            }
          );

          let reader = new FileReader();
          reader.readAsDataURL(selectedFile);
          reader.onload = (r) => {
            setPdfFile(selectedFile);
            setViewPdf(r.target.result);
            setToogleSummary(false);
            setMessages([]);
            setSummary([]);
            setFileStack((prev) => [
              ...prev,
              { file: selectedFile, result: r.target.result },
            ]);
          };
          setIsUploadLoading(false);
        } else {
          setPdfFile(null);
          setViewPdf(null);
        }
      } else {
        console.log("please select file");
      }
    } catch (e) {
      setIsUploadLoading(false);
      console.log("error", e);
    }
  };

  const handleFileChange = async (e) => {
    const fileName = e.target.value;
    if (fileName) {
      const newFile = fileStack.find((file) => file.file.name === fileName);
      setPdfFile(newFile?.file?.file || newFile?.file);
      newFile && setViewPdf(newFile?.file?.result || newFile?.result);
      setToogleSummary(false);
      setMessages([]);
      setSummary([]);
    }
  };

  useEffect(() => {
    loadFiles();
  }, []);

  return (
    <div className="root-header">
      <div className="app-name-container">
        <img src={DeloitteLogo} alt="logo" />
        <span className="app-name">IntelliExtractAI</span>
      </div>
      <div style={{ position: "absolute", left: "380px" }}>
        <Button
          className="upload"
          component="label"
          variant="contained"
          startIcon={
            isUploadLoading ? (
              <CircularProgress style={{ color: "#fff" }} size="1.2rem" />
            ) : (
              <CloudUploadIcon />
            )
          }
          // startIcon={<CloudUploadIcon />}
        >
          Upload File
          <VisuallyHiddenInput type="file" onChange={handleUploadFileChange} />
        </Button>
      </div>
      <div style={{ position: "absolute", right: "32px" }}>
        <span className="head-text">Select Source File for Extraction:</span>
        <select
          className="file-list-container"
          name="file"
          onChange={handleFileChange}
          value={(pdfFile && pdfFile.name) || null}
        >
          <option className="file-list" value={null}>
            Select File
          </option>
          {fileStack.map((file) => (
            <option className="file-list" value={file.file.name}>
              {file.file.name}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
};

export default Header;
