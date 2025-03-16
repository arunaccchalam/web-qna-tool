import { useState } from "react";
import { Button, Input, Card, CardContent } from "@/components/ui";

export default function QnAApp() {
  const [urls, setUrls] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchContent = async () => {
    setLoading(true);
    const urlList = urls.split(/[\s,]+/).filter((url) => url);
    const response = await fetch("http://127.0.0.1:5000/fetch", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ urls: urlList })
    });
    const data = await response.json();
    setLoading(false);
    alert(data.message || "Content fetched!");
  };

  const askQuestion = async () => {
    setLoading(true);
    const response = await fetch("http://127.0.0.1:5000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });
    const data = await response.json();
    setAnswer(data.answer || "No answer found.");
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center p-6 space-y-4">
      <h1 className="text-2xl font-bold">Web Q&A Tool</h1>
      <Input
        placeholder="Enter URLs (comma-separated)"
        value={urls}
        onChange={(e) => setUrls(e.target.value)}
        className="w-full max-w-lg"
      />
      <Button onClick={fetchContent} disabled={loading}>
        {loading ? "Fetching..." : "Fetch Content"}
      </Button>
      <Input
        placeholder="Ask a question"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="w-full max-w-lg"
      />
      <Button onClick={askQuestion} disabled={loading}>
        {loading ? "Processing..." : "Ask Question"}
      </Button>
      {answer && (
        <Card className="w-full max-w-lg">
          <CardContent className="p-4">
            <p className="font-semibold">Answer:</p>
            <p>{answer}</p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
