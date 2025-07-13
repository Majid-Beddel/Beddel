"use client";

import { useState } from "react";
import { useDropzone } from "react-dropzone";

export default function Home() {
  const [files, setFiles] = useState([]);
  const [prompt, setPrompt] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [resultUrl, setResultUrl] = useState("");

  const { getRootProps, getInputProps } = useDropzone({
    accept: { "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [] },
    onDrop: acceptedFiles => setFiles(acceptedFiles)
  });

  const handleSubmit = async () => {
    setIsSubmitting(true);
    const formData = new FormData();
    formData.append("user_prompt", prompt);
    files.forEach(file => formData.append("files", file));

    const res = await fetch("http://localhost:8000/process", {
      method: "POST",
      body: formData
    });

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    setResultUrl(url);
    setIsSubmitting(false);
  };

  return (
    <main className="p-8 max-w-xl mx-auto text-center space-y-4">
      <h1 className="text-3xl font-bold">Beddel</h1>
      <textarea
        placeholder="Please describe your changes here"
        className="border rounded w-full p-2"
        rows={4}
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
      />
      <div {...getRootProps()} className="border-dashed border-2 rounded p-8 cursor-pointer">
        <input {...getInputProps()} />
        <p>Drag and drop files here, or click to browse</p>
      </div>
      <div className="space-y-2">
        {files.map(f => (
          <div key={f.name} className="text-sm">{f.name}</div>
        ))}
      </div>
      <button
        onClick={handleSubmit}
        disabled={isSubmitting}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        {isSubmitting ? "Processing..." : "Submit"}
      </button>
      {resultUrl && (
        <div className="mt-4">
          <a href={resultUrl} download="processed.docx" className="text-blue-600 underline">
            Download your processed document
          </a>
        </div>
      )}
    </main>
  );
}
